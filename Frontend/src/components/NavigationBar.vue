<template>
    <nav class="navbar navbar-bg">
        <div class="container-fluid nav-container" ref="container">
            <div class="d-flex nav-start" ref="navStart">
                <img class="logo" src="/cardigan.png" alt="logo">
                <router-link to="/" class="navbar-brand on-navbar">Cardigan</router-link>
                <div class="vr" :class="{ 'hidden-nav': isExtraSmallAndEndFilled }"></div>
                <ul class="navbar-nav me-auto d-flex flex-row" :class="{ 'hidden-nav': isExtraSmallAndEndFilled }">
                    <li class="nav-item px-3">
                        <router-link to="/" class="nav-link on-navbar"
                            :class="{ active: route.path === '/' }">Home</router-link>
                    </li>
                    <li class="nav-item px-2">
                        <router-link to="/make" class="nav-link on-navbar"
                            :class="{ active: route.path === '/make' }">Make</router-link>
                    </li>
                </ul>
            </div>
            <div class="nav-middle" ref="middle">
                <slot name="middle"></slot>
            </div>
            <div class="nav-end" ref="end">
                <slot name="end"></slot>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const end = ref<HTMLElement | null>(null);
const middle = ref<HTMLElement | null>(null);
const navStart = ref<HTMLElement | null>(null);
const container = ref<HTMLElement | null>(null);
const endSlotFilled = ref(false);
const isExtraSmallAndEndFilled = ref(false);

var startWidth = 0;
var middleWidth = 0;
var endWidth = 0;

const checkLayout = () => {
    nextTick(() => {
        if (!container.value || !navStart.value || !middle.value || !end.value) return;
        
        endWidth = end.value!.offsetWidth;
        const containerWidth = container.value.offsetWidth;
        const totalContentWidth = startWidth + middleWidth + endWidth + 50;
        container.value.classList.toggle('stacked-layout', totalContentWidth > containerWidth);
        
        const stackedContentWidth = startWidth + endWidth + 30;
        isExtraSmallAndEndFilled.value = endSlotFilled.value && stackedContentWidth > containerWidth;
    });
};

onMounted(() => {
    startWidth = navStart.value!.offsetWidth;
    middleWidth = middle.value!.offsetWidth;
    endWidth = end.value!.offsetWidth;
    
    checkEndSlotFilled();
    checkLayout();
    window.addEventListener('resize', checkLayout);
});

const checkEndSlotFilled = () => {
    nextTick(() => { 
        const endSlotElement = end.value?.hasChildNodes() ?? false;
        endSlotFilled.value = endSlotElement;
    });
};

</script>

<style scoped>
.on-navbar {
    color: #0B090A;
}

.navbar-brand {
    font-weight: 600;
    color: #BA181B;
    font-size: 1.25em;
    font-family: sans-serif;
}

.navbar-btn {
    background-color: #b1a7a6;
}

.nav-link.active {
    color: #BA181B;
    /* font-weight: 500; */
}

.navbar-bg {
    background-color: #FFFFFF;
}

.logo {
    width: 35px;
    height: 35px;
    align-self: center;
    margin: auto 8px;
}

.hidden-nav {
    display: none !important;
}

.nav-container {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
}

.nav-container.stacked-layout {
    justify-content: space-between;
}

.stacked-layout .nav-middle {
    order: 4;
    width: 100%;
    display: flex;
    justify-content: center;
    margin-left: 0;
}

.stacked-layout .nav-start,
.stacked-layout .nav-end {
    flex: 0 1 auto;
}
</style>