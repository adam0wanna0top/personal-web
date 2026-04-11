import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'

describe('App.vue', () => {
  it('renders the title', () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          TodoList: true,
          TodoListApi: true,
          Monitor: true,
        },
      },
    })
    expect(wrapper.find('h1').text()).toContain('Vue 3 + TypeScript')
  })

  it('shows greeting when name is entered', async () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          TodoList: true,
          TodoListApi: true,
          Monitor: true,
        },
      },
    })
    const input = wrapper.find('input[placeholder="输入你的名字"]')
    await input.setValue('Test')
    expect(wrapper.text()).toContain('你好，Test')
  })

  it('counter increments and resets', async () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          TodoList: true,
          TodoListApi: true,
          Monitor: true,
        },
      },
    })
    const buttons = wrapper.findAll('button')
    // +1 button
    await buttons[1].trigger('click')
    expect(wrapper.text()).toContain('当前计数：1')
    // reset button
    await buttons[2].trigger('click')
    expect(wrapper.text()).toContain('当前计数：0')
  })
})
