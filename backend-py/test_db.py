"""db.py 单元测试：使用内存 SQLite，每次测试独立的临时数据库"""
import pytest
import db as db_module


@pytest.fixture
def db_path(tmp_path):
    """每个测试用独立的临时数据库文件"""
    return str(tmp_path / 'test.db')


@pytest.fixture
def populated_db(db_path):
    """预填充数据的数据库"""
    db_module.init_db(db_path)
    db_module.create('Task 1', db_path=db_path)
    db_module.create('Task 2', done=True, db_path=db_path)
    return db_path


def test_create(db_path):
    db_module.init_db(db_path)
    todo = db_module.create('Buy milk', db_path=db_path)
    assert todo['text'] == 'Buy milk'
    assert todo['done'] is False
    assert todo['id'] is not None


def test_create_with_done(db_path):
    db_module.init_db(db_path)
    todo = db_module.create('Done task', done=True, db_path=db_path)
    assert todo['done'] is True


def test_get_all(populated_db):
    todos = db_module.get_all(db_path=populated_db)
    assert len(todos) == 2
    # ORDER BY id DESC
    assert todos[0]['text'] == 'Task 2'


def test_get_by_id(populated_db):
    todos = db_module.get_all(db_path=populated_db)
    found = db_module.get_by_id(todos[0]['id'], db_path=populated_db)
    assert found is not None
    assert found['text'] == todos[0]['text']


def test_get_by_id_not_found(db_path):
    db_module.init_db(db_path)
    assert db_module.get_by_id(99999, db_path=db_path) is None


def test_update(populated_db):
    todos = db_module.get_all(db_path=populated_db)
    updated = db_module.update(todos[0]['id'], text='Updated', done=True, db_path=populated_db)
    assert updated['text'] == 'Updated'
    assert updated['done'] is True


def test_partial_update(populated_db):
    todos = db_module.get_all(db_path=populated_db)
    original_text = todos[0]['text']
    db_module.update(todos[0]['id'], done=True, db_path=populated_db)
    found = db_module.get_by_id(todos[0]['id'], db_path=populated_db)
    assert found['text'] == original_text
    assert found['done'] is True


def test_update_not_found(db_path):
    db_module.init_db(db_path)
    assert db_module.update(99999, text='Nope', db_path=db_path) is None


def test_delete(populated_db):
    todos = db_module.get_all(db_path=populated_db)
    assert db_module.delete(todos[0]['id'], db_path=populated_db) is True
    assert db_module.get_by_id(todos[0]['id'], db_path=populated_db) is None


def test_delete_not_found(db_path):
    db_module.init_db(db_path)
    assert db_module.delete(99999, db_path=db_path) is False
