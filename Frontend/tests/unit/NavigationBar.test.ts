import { expect, test } from 'vitest';
import { mount } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import NavigationBar from '@/components/NavigationBar.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", component: { template: '<div>Home</div>' } },
        { path: "/make", component: { template: '<div>Make</div>' } },
        { path: "/card/:id", component: { template: '<div>Card</div>' } },
    ]
});

test("Shows logo and shortcuts", async () => {
    expect(NavigationBar).toBeTruthy();

    const wrapper = mount(NavigationBar, {
        global: {
            plugins: [router]
        }
    });

    await router.isReady();
    expect(wrapper.text()).toContain("Cardigan");
    expect(wrapper.find("img").exists()).toBeTruthy();
    expect(wrapper.find("a[href='/']").exists()).toBeTruthy();
    expect(wrapper.find("a[href='/make']").exists()).toBeTruthy();
});

test("Adding middle and end slots", async () => {
    const wrapper = mount(NavigationBar, {
        global: {
            plugins: [router]
        },
        slots: {
            middle: '<div class="middle">Middle</div>',
            end: '<div class="end">End</div>'
        }
    });

    await router.isReady();
        
    expect(wrapper.find(".middle").exists()).toBeTruthy();
    expect(wrapper.find(".end").exists()).toBeTruthy();
});

