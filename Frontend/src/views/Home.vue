<script setup lang="ts">
import { useRoute } from 'vue-router';
import NavigationBar from '@/components/NavigationBar.vue';
import SlotMachineText from '@/components/SlotMachineText.vue';
import CookieConcent from '@/components/CookieConcent.vue';

const route = useRoute();

function shuffleArray(array: Array<any>) {
    for (let i = array.length - 1; i >= 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

const words = [
    "Happy",
    "Grateful",
    "Loved",
    "Excited",
    "Appreciated",
    "Inspired",
    "Special",
    "Warm",
    "Surprised",
    "Blessed",
    "Motivated",
    "Joyful",
    "Cherished",
    "Comforted",
    "Uplifted",
    "Encouraged",
    "Giddy",
    "Dizzy",
    "Adored",
    "Seen",
    "Pure joy",
    "Smitten",
    "Skibidi",
    "Sad"
];
shuffleArray(words);

</script>

<template>
    <header>
        <NavigationBar />
    </header>

    <main class="main-container">
        <div class="banner">
            <div class="banner-content">
                <h1 class="banner-title">
                    Want to leave someone feeling <span class="emphasis">
                        <SlotMachineText :words="words" />
                    </span>

                </h1>
                <span class="banner-subtitle"> Send them a greeting card! </span>
            </div>
            <img src="/cards.png" alt="cards" class="banner-image">
        </div>

        <button type="button" class="btn btn-danger" @click="() => $router.push('/make')">Make a card today</button>

        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Who are we?</h5>
                <p class="card-text">
                    Born from the ashes of boring, bland, and utterly uninspired greeting cards, Cardigan ascended like a phoenix
                    of personalized greeting cards. We are disrupting the greeting card business and taking on big card to
                    bring to you a completely free* greeting card exchange service.</p>
                <p class="tiny" style="text-align: center">*By using this website you agree to us using all your data to
                    train AGI in preparation for the great summoning.</p>
                <p class="tiniTiny" style="text-align: center">*Also by using this website you agree to giving your soul
                    to our lord and destroyer Cthulhu</p>
            </div>
        </div>

    </main>
    <CookieConcent />
</template>

<style scoped>
.btn {
    font-size: 1.2rem;
    margin: 20px auto;
}

.main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: calc(100vh - 56px);
    width: 100%;
    margin: 0 auto;
    padding: 0 20px;
    box-sizing: border-box;
}

@media (min-width: 1200px) {
    .main-container {
        max-width: 1200px;
    }
}

.banner {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    padding: 20px;
    box-sizing: border-box;
    text-align: center;
}

.banner-title {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

.banner-subtitle {
    font-size: 1.2rem;
    font-weight: 400;
}

.banner-image {
    max-width: 90%;
    height: auto;
}

@media (min-width: 576px) {
    .banner-title {
        font-size: 3rem;
    }

    .banner-subtitle {
        font-size: 1.5rem;
    }

    .btn {
        font-size: 1.5rem;
    }

    .banner-image {
        max-width: 80%;
    }
}

@media (min-width: 768px) {
    .banner {
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }

    .banner-title {
        font-size: 3.5rem;
    }

    .banner-subtitle {
        font-size: 1.7rem;
    }

    .banner-image {
        max-width: 50%;
    }

    .banner-content {
        margin-right: 0;
        /* Remove margin on small screens */
        margin-bottom: 20px;
        /* Add margin below text */
    }
}

.banner-content {
    flex: 1;
    /* Allow text to take up available space */
    margin-right: 20px;
    /* Space between text and image */
}

.emphasis {
    color: #e5383b;
}

.tiny {
    font-size: 0.5em;
    text-align: center;
}

.tiniTiny {
    font-size: 0.1em;
    text-align: center;
}

.card {
    background-color: #F5F3F4;
    margin: 20px auto;
    width: 100%;
    box-sizing: border-box;
}

.card-body {
    padding: 20px;
}
</style>