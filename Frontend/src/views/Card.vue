<template>
    <header>
        <NavigationBar />
    </header>
    <div class="background">
        <div class="postcard-container" :style="{ width: containerWidth + 'px', height: containerHeight + 'px' }">
            <div v-if="imagesRetrieved && cardType==CardType.Openable" class="postcard" :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }">
                <div class="front" :style="imageStyle(frontImage)" @click="right()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
                <div class="inside-right" :style="imageStyle(backInsideImage)" @click="right()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
                <div class="inside-left" :style="imageStyle(frontInsideImage)" @click="left()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
                <div class="back" :style="imageStyle(backImage)" @click="left()"
                    :class="{ 'on-back': onBack, 'on-inside': onInside, 'on-front': onFront }"></div>
            </div>
            <div v-else-if="imagesRetrieved && cardType==CardType.TwoSided" class="postcard">
                <div class="front" :style="imageStyle(frontImage)" @click="flip()"
                    :class="{ 'on-back-2': onBack, 'on-front-2': onFront }"></div>
                <div class="back" :style="imageStyle(backImage)" @click="flip()"
                    :class="{ 'on-back-2': onBack, 'on-front-2': onFront }"></div>
            </div>
            <div v-else-if="imagesRetrieved && cardType==CardType.OneSided" class="postcard">
                <div class="front" :style="imageStyle(frontImage)"
                    :class="{'on-front-1': onFront }"></div>
            </div>
            <div v-else >
                <div v-if="couldNotRetrieve">
                    <h1>{{ error }}</h1>
                </div>
                <div v-else>
                    <h1>Please, wait while we retrieve your card..</h1>
                </div>
            </div>
        </div>
        <footer>
            <div v-if="imagesRetrieved && cardType==CardType.Openable">
                <div class="btn-group" role="group">
                    <button @click="left()" class="btn btn-danger">
                        <i class="bi bi-arrow-left px-2 my-0" style="font-size: 2rem;"/>
                    </button>
                    <button @click="right()" class="btn btn-danger">
                        <i class="bi bi-arrow-right px-2 my-0" style="font-size: 2rem;"/>
                    </button>
                </div>
            </div>
            <div v-if="imagesRetrieved && cardType==CardType.TwoSided">
                <button @click="flip()" class="btn btn-danger footer-btn">
                    <i class="bi bi-phone-flip px-2 my-0" style="font-size: 2rem;"/>
                </button>
            </div>
        </footer>
    </div>
</template>

<script setup lang="ts">
import NavigationBar from '@/components/NavigationBar.vue';
import { API_BASE_URL, CardType } from '@/scripts/Constants';
import axios from 'axios';
import { ref, onMounted, type Ref } from 'vue';
import { useRoute } from 'vue-router';

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

onMounted(async () => {
    adjustContainerSize();
    window.addEventListener('resize', adjustContainerSize);
    
    await axios.get(`${API_BASE_URL}/card/${cardId}`).then((result) => {
        
        frontImage.value = result.data["front"];

        if (result.data["front_inside"] != null) {
            frontInsideImage.value = result.data["front_inside"];
            backInsideImage.value = result.data["back_inside"];
            backImage.value = result.data["back"];
            cardType.value = CardType.Openable;
        } else if (result.data["back"] != null){
            backImage.value = result.data["back"];
            cardType.value = CardType.TwoSided;
        } else {
            cardType.value = CardType.OneSided;
        }
        imagesRetrieved.value = true;
        
    }).catch((reason) => {
        couldNotRetrieve.value = true;
        error.value = reason;
    });
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
        display: 'block'
    };
    if (cardType.value != CardType.Openable && (image == "backInsideImage" || image == "frontInsideImage")){
        styles.display = "none";
    } else if (cardType.value == CardType.OneSided && image == "backImage"){
        styles.display = "none"
    }
    return styles;
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

.footer-btn {
    padding: 16px 16px;
    border: 1px solid;
    cursor: pointer;
    border-radius: 20px 20px 0 0;
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