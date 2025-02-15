<template>
    <nav class="navbar navbar-bg">
        <div class="container-fluid d-flex flex-md-row" ref="mainline">
            <div class="d-flex">
                <a class="navbar-brand on-navbar" href="#">E-Cards</a>
                <div class="vr"></div>
                <ul class="navbar-nav me-auto d-flex flex-row">
                    <li class="nav-item px-4">
                        <a class="nav-link on-navbar" :class="{ active: route.path === '/' }" href="/">Home</a>
                    </li>
                    <li class="nav-item px-3">
                        <a class="nav-link on-navbar" :class="{ active: route.path === '/make' }" href="/make">Make</a>
                    </li>
                </ul>
            </div>
            <div class="d-flex pe-lg-5" pe-5 ref="middle">
                <slot name="middle"></slot>
            </div>
            <div class="d-flex" ref="end">
                <slot name="end"></slot>
            </div>
        </div>
        <div class="d-flex flex-row w-100 justify-content-center" ref="newline">
            
        </div>
    </nav>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, watch, useTemplateRef } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const breakpoint = ref(window.innerWidth > 992);
const newline = useTemplateRef("newline");
const middle = useTemplateRef("middle");
const mainline = useTemplateRef("mainline");
const end = useTemplateRef("end");

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
        });
        
        moveMiddle();
    });
});
watch(breakpoint, (newVal) => {
    moveMiddle();
});
</script>

<style scoped>
.on-navbar {
    color: #0B090A;
}

.navbar-brand {
    font-weight: 600;
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
</style>