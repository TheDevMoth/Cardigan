<template>
    <header>
        <NavigationBar />
    </header>
    <div class="background">
        <div class="postcard-container" :style="{ width: containerWidth + 'px', height: containerHeight + 'px' }">
            <div class="postcard" :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }">
                <div class="front" :style="imageStyle(frontImage)" @click="right()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
                <div class="inside-right" :style="imageStyle(insideRightImage)" @click="right()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
                <div class="inside-left" :style="imageStyle(insideLeftImage)" @click="left()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
                <div class="back" :style="imageStyle(backImage)" @click="left()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
            </div>
        </div>
        <footer>
            <div class="btn-group" role="group">
                <button @click="left()" class="btn btn-danger">
                    <i class="bi bi-arrow-left px-2 my-0" style="font-size: 2rem;"/>
                </button>
                <button @click="right()" class="btn btn-danger">
                    <i class="bi bi-arrow-right px-2 my-0" style="font-size: 2rem;"/>
                </button>
            </div>
        </footer>
    </div>
</template>

<script setup>
import NavigationBar from '@/components/NavigationBar.vue';
import { ref, onMounted } from 'vue';

const frontImage = ref('/front.png');
const insideRightImage = ref('/insideRight.png');
const insideLeftImage = ref('/insideLeft.png');
const backImage = ref('/back.png');

const onFront = ref(true);
const onInside = ref(false);
const onBack = ref(false);

const containerWidth = ref(0);
const containerHeight = ref(0);

const lastActionTime = ref(0);
const COOLDOWN_DURATION = 1200;

onMounted(() => {
    adjustContainerSize();
    window.addEventListener('resize', adjustContainerSize);
});

const adjustContainerSize = () => {
    const maxWidth = window.innerWidth * 0.6;
    const maxHeight = window.innerHeight * 0.9;

    const aspectRatio = 707 / 1000;

    if (maxWidth / maxHeight > aspectRatio) {
        containerHeight.value = maxHeight;
        containerWidth.value = maxHeight * aspectRatio;
    } else {
        containerWidth.value = maxWidth;
        containerHeight.value = maxWidth / aspectRatio;
    }
};

function left() {
    const currentTime = Date.now();
    if (currentTime - lastActionTime.value < COOLDOWN_DURATION) return;
    
    lastActionTime.value = currentTime;
    
    if (onFront.value) return;
    else if (onInside.value) {
        onFront.value = true;
        onInside.value = false;
    } else if (onBack.value) {
        onInside.value = true;
        onBack.value = false;
    }
}

function right() {
    const currentTime = Date.now();
    if (currentTime - lastActionTime.value < COOLDOWN_DURATION) return;
    
    lastActionTime.value = currentTime;
    
    if (onBack.value) return;
    else if (onInside.value) {
        onBack.value = true;
        onInside.value = false;
    } else if (onFront.value) {
        onInside.value = true;
        onFront.value = false;
    }
}


const imageStyle = (image) => {
    return {
        backgroundImage: `url(${image})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
    };
};

</script>

<style scoped>
.background {
    background-color: #F5F3F4;
    height: calc(100vh - 56px);
}

.postcard-container {
    display: flex;
    justify-content: center;
    align-items: center;
    perspective: 2000px;
    margin: 0px auto;
}

.postcard {
    position: relative;
    width: 80%;
    height: 80%;
    transform-style: preserve-3d;
    transition: transform 1s ease;
}

.postcard>div {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
}

footer {
    width: 100%;
    display: flex;
    align-items:center;
    justify-content: center;
}

footer .btn-group button {
    padding: 16px 16px;
    border: 1px solid;
    cursor: pointer;
}

footer .btn-group button:first-child {
    border-radius: 20px 0 0 20px; 
}

footer .btn-group button:last-child {
    border-radius: 0 20px 20px 0; 
}

/* Animation classes */
.front,
.inside-left,
.inside-right,
.back {
    transition: transform 2s ease;
}

.front,
.inside-left,
.inside-right,
.back {
    transform: translateZ(1px);
}

.front.on-front {
    transform: rotateY(0deg) translateX(50%) translateZ(0px);
}

.inside-left.on-front {
    transform: rotateY(180deg);
}

.inside-right.on-front {
    transform: rotateY(0deg) translateX(50%) translateZ(-1px);
}

.back.on-front {
    transform: rotateY(180deg) translateX(-50%);
}

.front.on-inside {
    transform: rotateY(-180deg) translateX(50%);
}

.inside-left.on-inside {
    transform: rotateY(0deg) translateX(-50%);
}

.inside-right.on-inside {
    transform: rotateY(0deg) translateX(50%) translateZ(0px);
}

.back.on-inside {
    transform: rotateY(180deg) translateX(-50%);
}

.front.on-back {
    transform: rotateY(-180deg) translateX(50%);
}

.inside-left.on-back {
    transform: rotateY(0deg) translateX(-50%) translateZ(-1px);
}

.inside-right.on-back {
    transform: rotateY(-180deg) translateX(50%);
}

.back.on-back {
    transform: rotateY(0deg) translateX(-50%) translateZ(0px);
}
</style>