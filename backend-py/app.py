"""Flask 服务器 + WebSocket：API 路由 + 实时推送监控数据"""
import time
import json
import platform
import threading
import psutil
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sock import Sock
from db import init_db, get_all, get_by_id, create, update as db_update, delete as db_delete

app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': 'http://localhost:5173'}})
sock = Sock(app)

init_db()

# ========== 请求日志 & 计数 ==========
request_logs = []
total_requests = 0
start_time = time.time()
ws_clients = []  # 所有连接的监控客户端


def broadcast(data):
    """向所有 WebSocket 客户端推送消息"""
    msg = json.dumps(data)
    for client in ws_clients[:]:
        try:
            client.send(msg)
        except Exception:
            ws_clients.remove(client)


def get_health_data():
    """获取系统健康数据"""
    mem = psutil.virtual_memory()
    return {
        'status': 'ok',
        'uptime': int(time.time() - start_time),
        'memory': {
            'total': round(mem.total / 1024 / 1024),
            'used': round(mem.used / 1024 / 1024),
            'percent': mem.percent,
        },
        'cpu': {
            'model': platform.processor() or 'unknown',
            'cores': psutil.cpu_count(),
            'load': round(psutil.cpu_percent(interval=0), 1),
        },
    }


@app.after_request
def log_request(response):
    global total_requests
    total_requests += 1
    log = {
        'method': request.method,
        'path': request.path,
        'status': response.status_code,
        'time': time.strftime('%H:%M:%S'),
    }
    request_logs.insert(0, log)
    if len(request_logs) > 50:
        del request_logs[50:]

    # 有新请求时，立刻通过 WebSocket 推送
    broadcast({'type': 'log', 'log': log, 'totalRequests': total_requests})
    return response


# ========== Todo API 路由 ==========

@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    return jsonify(get_all())


@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def api_get_todo(todo_id):
    todo = get_by_id(todo_id)
    if not todo:
        return jsonify({'error': '未找到'}), 404
    return jsonify(todo)


@app.route('/api/todos', methods=['POST'])
def api_create_todo():
    data = request.get_json()
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({'error': '内容不能为空'}), 400
    todo = create(text, data.get('done', False))
    return jsonify(todo), 201


@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def api_update_todo(todo_id):
    data = request.get_json()
    todo = db_update(todo_id, text=data.get('text'), done=data.get('done'))
    if not todo:
        return jsonify({'error': '未找到'}), 404
    return jsonify(todo)


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def api_delete_todo(todo_id):
    if not db_delete(todo_id):
        return jsonify({'error': '未找到'}), 404
    return jsonify({'success': True})


# ========== 监控 HTTP API（保留，用于初始加载）==========

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify(get_health_data())


@app.route('/api/stats', methods=['GET'])
def api_stats():
    return jsonify({
        'totalRequests': total_requests,
        'recentLogs': request_logs[:20],
    })


# ========== WebSocket：实时推送监控数据 ==========

@sock.route('/ws')
def ws_connection(ws):
    print('监控客户端已连接 (WebSocket)')
    ws_clients.append(ws)

    # 连接时先发一次当前状态
    ws.send(json.dumps({
        'type': 'init',
        'health': get_health_data(),
        'stats': {'totalRequests': total_requests, 'recentLogs': request_logs[:20]},
    }))

    try:
        while True:
            ws.receive()  # 保持连接
    except Exception:
        pass
    finally:
        ws_clients.remove(ws)
        print('监控客户端已断开')


# 后台线程：每 5 秒推送系统资源
def push_health():
    while True:
        time.sleep(5)
        if ws_clients:
            broadcast({'type': 'health', 'health': get_health_data()})


threading.Thread(target=push_health, daemon=True).start()


if __name__ == '__main__':
    print('Python 后端已启动 → http://localhost:3002')
    print('WebSocket 监控 → ws://localhost:3002/ws')
    app.run(port=3002, debug=True)
