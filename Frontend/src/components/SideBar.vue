<template>
    <button class="btn expander" @click="unHideSidebar" :class="{hidden: !sidebarUsed}">
      <i class="bi bi-arrow-right" style="font-size: 1.5rem; color: #161A1D"/>
    </button>
    <div :class="['sidebar', { expanded: isExpanded }]">
        <button class="collapseButton" :onclick="hideSidebar"><i class="bi bi-arrow-left" style="font-size: 1.5rem; color: #161A1D"/></button>
        <div class="content">
            <slot></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const isExpanded = ref(false);
const hidden = ref(false);
const sidebarUsed = ref(false);

function expandSidebar() {
    if (!hidden.value) isExpanded.value = true;
    
    sidebarUsed.value = true;
}
function forceExpandSidebar() {
    isExpanded.value = true;
    sidebarUsed.value = true;
}
function retractSidebar() {
    sidebarUsed.value = false;
    isExpanded.value = false;
    
}
function hideSidebar() {
    isExpanded.value = false;
    hidden.value = true;
}
function unHideSidebar() {
    isExpanded.value = true;
    hidden.value = false;
}
defineExpose({
    expandSidebar,
    retractSidebar,
    forceExpandSidebar
});
</script>

<style scoped>
.expander {
    position: absolute;
    left: 0;
    top: 0;
    padding: 6px 12px;
    margin-top: 6px;
    border: 1px solid #dbd5d4;
    border-left: 0px;
    background: white;
    cursor: pointer;
    border-radius: 0 12px 12px 0;
    transition: left 0.3s;
}
.hidden {
    left: -50px
}
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