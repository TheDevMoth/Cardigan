<template>
    <div :class="['sidebar', { expanded: isExpanded }]">
        <button class="collapseButton" :onclick="retractSidebar"><i class="bi bi-arrow-left" style="font-size: 1.5rem; color: #161A1D"/></button>
        <div class="content">
            <slot></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const isExpanded = ref(false);

function toggleSidebar() {
    isExpanded.value = !isExpanded;
}
function expandSidebar() {
    isExpanded.value = true;
}
function retractSidebar() {
    console.log("ret");
    
    isExpanded.value = false;
}

defineExpose({
    toggleSidebar,
    expandSidebar,
    retractSidebar,
});
</script>

<style scoped>
.sidebar {
    position: absolute;
    left: 0;
    top: 0;
    width: 0px;
    height: 100%;
    transition: width 0.3s;
    overflow: hidden;
    background-color: white;
    z-index: 1000;
}

.sidebar.expanded {
    width: 400px;
    border: 0px;
    border-right: 1px;
    border-top: 1px;
    border-color: #D3D3D3;
    border-style: solid;
}

.content {
    padding: 10px;
}

.collapseButton {
    border: 0px;
    background-color: transparent;
    position: absolute;
    right: 16px;
    top: 10px
}
</style>