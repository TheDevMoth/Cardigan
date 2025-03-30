<template>
    <header>
        <NavigationBar />
    </header>
    <div class="background">
        <div class="postcard-container">
            <div v-if="imagesRetrieved && cardType == CardType.Openable" class="postcard"
                :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }">
                <div class="front" :style="imageStyle(frontImage)" @click="right()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
                <div class="inside-right" :style="imageStyle(backInsideImage)" @click="right()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
                <div class="inside-left" :style="imageStyle(frontInsideImage)" @click="left()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
                <div class="back" :style="imageStyle(backImage)" @click="left()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
            </div>
            <div v-else-if="imagesRetrieved && cardType == CardType.TwoSided" class="postcard">
                <div class="front" :style="imageStyle(frontImage)" @click="flip()"
                    :class="{ 'on-back-2': onBack, 'on-front-2': onFront }"></div>
                <div class="back" :style="imageStyle(backImage)" @click="flip()"
                    :class="{ 'on-back-2': onBack, 'on-front-2': onFront }"></div>
            </div>
            <div v-else-if="imagesRetrieved && cardType == CardType.OneSided" class="postcard">
                <div class="front" :style="imageStyle(frontImage)" :class="{ 'on-front-1': onFront }"></div>
            </div>
            <div v-else>
                <div v-if="couldNotRetrieve">
                    <h1>{{ error }}</h1>
                </div>
                <div v-else class="loading-container">
                    <h1 class="my-4 mx-2">Please, wait while we retrieve your card..</h1>
                    <br class="m-2">
                    <img class="spinning-logo" src="/cardigan.png" alt="logo">
                </div>
            </div>
        </div>
        <footer>
            <div v-if="imagesRetrieved && cardType == CardType.Openable">
                <div class="btn-group" role="group">
                    <button @click="left()" class="btn btn-danger">
                        <i class="bi bi-arrow-left px-2 my-0" style="font-size: 2rem;" />
                    </button>
                    <button @click="right()" class="btn btn-danger">
                        <i class="bi bi-arrow-right px-2 my-0" style="font-size: 2rem;" />
                    </button>
                </div>
            </div>
            <div v-if="imagesRetrieved && cardType == CardType.TwoSided">
                <button @click="flip()" class="btn btn-danger footer-btn">
                    <i class="bi bi-phone-flip px-2 my-0" style="font-size: 2rem;" />
                </button>
            </div>
        </footer>
    </div>
</template>

<script setup lang="ts">
import NavigationBar from '@/components/NavigationBar.vue';
import { API_BASE_URL, CardType } from '@/scripts/Constants';
import { clamp } from '@/scripts/Utils';
import axios from 'axios';
import { ref, onMounted, type Ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useHead } from '@vueuse/head'

useHead({
    title: 'Cardigan: Create & Share Personalized Greeting Cards',
    meta: [
        { name: 'description', content: 'Open to view a personalized digital card. Discover a heartfelt message and unique design created just for you.' },
        { property: 'og:title', content: "You've received a Cardigan greeting!" },
        { property: 'og:description', content: 'Open to view a personalized digital card. Discover a heartfelt message and unique design created just for you.' },
        { property: 'og:image', content: 'https://www.cardigan.publicvm.com/cardigan.png' },
        { property: 'og:url', content: 'https://www.cardigan.publicvm.com' }
    ]
})

const route = useRoute()
const cardId = route.params.id
const cardType: Ref<CardType | null> = ref(null);

const frontImage = ref("");
const backInsideImage = ref("");
const frontInsideImage = ref("");
const backImage = ref("");

const imagesRetrieved = ref(false);
const onFront = ref(true);
const onInside = ref(false);
const onBack = ref(false);

const containerWidth = ref(0);
const containerHeight = ref(0);

const lastActionTime = ref(0);
const COOLDOWN_DURATION = 1200;

const couldNotRetrieve = ref(false);
const error = ref("");

var audio: HTMLAudioElement | null;

onMounted(async () => {
    adjustContainerSize();
    window.addEventListener('resize', adjustContainerSize);

    try {
        const result = await axios.get(`${API_BASE_URL}/card/${cardId}`);

        // Store image URLs
        frontImage.value = result.data["front"];

        const imageUrls = [frontImage.value];

        if (result.data["front_inside"] != null) {
            frontInsideImage.value = result.data["front_inside"];
            backInsideImage.value = result.data["back_inside"];
            backImage.value = result.data["back"];
            imageUrls.push(frontInsideImage.value, backInsideImage.value, backImage.value);

            if (result.data["audio"])
                audio = new Audio(result.data["audio"]);

            cardType.value = CardType.Openable;
        } else if (result.data["back"] != null) {
            backImage.value = result.data["back"];
            imageUrls.push(backImage.value);
            cardType.value = CardType.TwoSided;
        } else {
            cardType.value = CardType.OneSided;
        }

        // Ensure all images are loaded
        await Promise.all(imageUrls.map(loadImage));

        imagesRetrieved.value = true;
        adjustContainerSize();
    } catch (e) {
        couldNotRetrieve.value = true;
        error.value = (e as Error).toString();
    }
});

const leftPosition = computed(() => {
    const baseLeft = (cardType.value === CardType.Openable) ?
        containerWidth.value * 0.6 : containerWidth.value * 0.05;

    if (cardType.value === CardType.Openable)
        return window.innerWidth >= 1555 ? `calc(${baseLeft}px + 50vw - 778px)` : `calc(${baseLeft}px)`;
    else
        return window.innerWidth >= 788 ? `calc(${baseLeft}px + 50vw - 389px)` : `calc(${baseLeft}px)`;

});

function adjustContainerSize() {
    var maxWidth = window.innerWidth * 0.9;
    var maxHeight = window.innerHeight - 120;
    if (cardType.value == CardType.Openable)
        maxWidth *= 0.5;
    maxHeight = clamp(maxHeight, 0, 1000);
    maxWidth = clamp(maxWidth, 0, 707);

    const aspectRatio = 707 / 1000;

    if (maxWidth / maxHeight <= aspectRatio) {
        containerWidth.value = maxWidth;
        containerHeight.value = maxWidth / aspectRatio;
    } else {
        containerHeight.value = maxHeight;
        containerWidth.value = maxHeight * aspectRatio;
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
        stopAudio();
    } else if (onBack.value) {
        onInside.value = true;
        onBack.value = false;
        playAudio();
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
        stopAudio();
    } else if (onFront.value) {
        onInside.value = true;
        onFront.value = false;
        playAudio();
    }
}

function flip() {
    const currentTime = Date.now();
    if (currentTime - lastActionTime.value < COOLDOWN_DURATION) return;
    lastActionTime.value = currentTime;

    if (onFront.value) {
        onBack.value = true;
        onFront.value = false;
    } else {
        onBack.value = false;
        onFront.value = true;
    }
}

function imageStyle(image: String) {
    var styles = {
        backgroundImage: `url(${image})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        display: 'block',
        width: containerWidth.value + 'px',
        height: containerHeight.value + 'px',
    };
    return styles;
};

function loadImage(url: string) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = url;
        img.onload = resolve;
        img.onerror = reject;
    });
}

function playAudio() {
    if (!audio) return;
    audio.currentTime = 0;
    audio.play();
}
function stopAudio() {
    if (!audio) return;
    setTimeout(() => {
        audio!.pause();
        audio!.currentTime = 0;
    }, 1200);
}

</script>

<style scoped>
.background {
    background-color: #F5F3F4;
    height: calc(100vh - 56px);
    padding-top: 10px;
}

.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.spinning-logo {
    width: 80px;
    height: 80px;
    animation: spin 1.5s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.postcard-container {
    display: flex;
    justify-content: center;
    align-items: center;
    perspective: 2000px;
}

.postcard {
    position: relative;
    transform-style: preserve-3d;
    transition: transform 1s ease;
    width: 100%;
    height: 100%;
}

.postcard>div {
    position: absolute;
    top: calc(43vh - v-bind(containerHeight/2 + 'px'));
    left: calc(50% - v-bind(containerWidth/2 + 'px'));
    backface-visibility: hidden;
}

footer {
    width: 100%;
    position: absolute;
    bottom: 0px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.footer-btn {
    padding: 0.5rem 1rem;
    border: 1px solid;
    cursor: pointer;
    border-radius: 20px 20px 0 0;
}

footer .btn-group button {
    padding: 0.5rem 1rem;
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

/* openable cards */
.front.on-front {
    transform: rotateY(0deg) translateX(50%) translateZ(0px);
}

.inside-left.on-front {
    transform: rotateY(180deg) translateX(-50%);
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

/* two sided cards */

.front.on-front-2 {
    transform: rotateY(0deg) translateZ(1px);
}

.front.on-back-2 {
    transform: rotateY(-180deg) translateZ(0px);
}

.back.on-front-2 {
    transform: rotateY(180deg) translateZ(0px);
}

.back.on-back-2 {
    transform: rotateY(0deg) translateZ(1px);
}

/* one sided cards */
.front.on-front-1 {
    transform: rotateY(0deg) translateZ(1px);
}
</style>