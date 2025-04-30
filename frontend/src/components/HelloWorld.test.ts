import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HelloWorld from './HelloWorld.vue'

describe('HelloWorld Component', () => {
  it('renders the correct message', () => {
    const msg = 'Hello Vitest'
    const wrapper = mount(HelloWorld, {
      props: {
        msg
      }
    })
    expect(wrapper.text()).toContain(msg)
  })

  it('increments count when button is clicked', async () => {
    const wrapper = mount(HelloWorld, {
      props: {
        msg: 'Hello'
      }
    })
    
    // Initial count should be 0
    expect(wrapper.text()).toContain('count is 0')
    
    // Find the button and click it
    const button = wrapper.find('button')
    await button.trigger('click')
    
    // Count should be incremented
    expect(wrapper.text()).toContain('count is 1')
  })
})
