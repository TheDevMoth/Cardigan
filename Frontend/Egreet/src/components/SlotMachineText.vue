<template>
    <span class="slot-machine-recipe">
      <span 
        class="slot-machine-recipe__mask"
        :style="{ width: `${maxWordWidth}px` }"
        ref="maskBox"
      >
        <span 
          class="slot-machine-recipe__items_container" 
          :style="{ top: `${topOffset}px`, transition: transitionEnabled ? 'top 0.5s ease' : 'none' }"
          ref="wordbox"
        >
          <span 
            v-for="(word, index) in repeatedWordlist" 
            :key="index" 
            class="slot-machine-recipe__item"
            ref="(el) => wordItems[index] = el"
          >
            {{ word }}
          </span>
        </span>
      </span>
    </span>
  </template>
  
<script setup lang="ts">
  import { ref, computed, onMounted, onBeforeUnmount, nextTick} from 'vue';
  
  const props = defineProps<{ words: string[] }>();
  
  const topOffset = ref<number>(0);
  const wordHeight = 5 * 16;
  const interval = ref<number | null>(null);
  const wordbox = ref<HTMLElement | null>(null);
  const maskBox = ref<HTMLElement | null>(null);
  const wordItems = ref<HTMLElement[]>([]);
  const transitionEnabled = ref<boolean>(true);
  const maxWordWidth = ref<number>(500);
  
  const repeatedWordlist = computed<string[]>(() => [...props.words, ...props.words]);
  
  function randomSlotIndex(max: number): number {
    return Math.floor(Math.random() * max) + max;
  }
  
  function animate(): void {
    const wordIndex = randomSlotIndex(props.words.length);
    topOffset.value = -wordIndex * wordHeight;
  
    setTimeout(() => {
      rotateContents(wordIndex);
    }, 500);
  }
  
  function rotateContents(wordIndex: number): void {
    if (wordbox.value) {
      transitionEnabled.value = false;
      for (let i = 0; i < wordIndex; i++) {
        const firstChild = wordbox.value.firstElementChild as HTMLElement;
        if (firstChild) {
          wordbox.value.appendChild(firstChild);
        }
      }
      topOffset.value = 0;
      
      setTimeout(() => {
        transitionEnabled.value = true;
      }, 50);
    }
  }
  
  function updateMaxWordWidth(): void {
    if (wordbox.value) {
      const children = wordbox.value.childNodes;        
      let maxWidth = 0;
      children.forEach((child: any) => {
        if (child.offsetWidth > maxWidth) {
          maxWidth = child.offsetWidth;
        }
      });
      maxWordWidth.value = maxWidth;
    }
  }
  
  onMounted(() => {
    nextTick(() => {
      updateMaxWordWidth();
    });
    window.addEventListener('resize', updateMaxWordWidth);
    interval.value = window.setInterval(animate, 5000);
  });
  
  onBeforeUnmount(() => {
    if (interval.value !== null) {
      clearInterval(interval.value);
    }
    window.removeEventListener('resize', updateMaxWordWidth);
  });
</script>
  
<style>
  .slot-machine-recipe {
    display: inline-block;
    vertical-align: middle;
  }

  .slot-machine-recipe__mask {
    display: inline-block;
    height: 5rem;
    overflow: hidden; 
    position: relative;
    text-align: start;
    vertical-align: middle;
  }

  .slot-machine-recipe__items_container {
    position: absolute;
    width: 100%;
    text-align: start;
    display: flex;
    flex-direction: column;
  }

  .slot-machine-recipe__item {
    display: block;
    min-height: 5rem;
    max-height: 5rem;
    width: min-content;
    margin: 0px auto;
    padding: 0px;
    background-size: contain;
    white-space: nowrap;
    line-height: 3.5rem;
  }
</style>