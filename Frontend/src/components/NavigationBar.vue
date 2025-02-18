<template>
    <nav class="navbar navbar-bg">
        <div class="container-fluid d-flex flex-md-row" ref="mainline">
            <div class="d-flex">
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
            <div class="d-flex pe-lg-3" ref="middle">
                <slot name="middle"></slot>
            </div>
            <div class="d-flex" ref="end">
                <slot name="end"></slot>
            </div>
        </div>
        <div class="d-flex flex-row w-100 justify-content-center" ref="newline"></div>
    </nav>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, watch, useTemplateRef, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const breakpoint = ref(window.innerWidth > 992);
const newline = useTemplateRef("newline");
const middle = useTemplateRef("middle");
const mainline = useTemplateRef("mainline");
const end = useTemplateRef("end");
const endSlotFilled = ref(false);
const isExtraSmallAndEndFilled = ref(false);

function moveMiddle() {
    if (!(middle.value && newline.value && mainline.value)) return;
    if (breakpoint.value) {
        mainline.value.insertBefore(middle.value, end.value);
    } else {
        newline.value.appendChild(middle.value);
    }
}

onMounted(() => {
    nextTick(() => {
        window.addEventListener('resize', () => {
            breakpoint.value = window.innerWidth > 992;
            isExtraSmallAndEndFilled.value = window.innerWidth <= 550 && endSlotFilled.value;
        });
        isExtraSmallAndEndFilled.value = window.innerWidth <= 550 && endSlotFilled.value;
        moveMiddle();
        checkEndSlotFilled();
    });
});

watch(breakpoint, (newVal) => {
    moveMiddle();
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

</style>