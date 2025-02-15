<script setup lang="ts">
import { useRoute } from 'vue-router';
import NavigationBar from '@/components/NavigationBar.vue';
import SlotMachineText from '@/components/SlotMachineText.vue';

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
            <div>
                <h1 class="banner-title">
                    Want to leave someone feeling <span class="emphasis">
                        <SlotMachineText :words="words" />
                    </span>

                </h1>
                <span class="banner-subtitle"> Send them an electronic gift card! </span>
            </div>
            <img src="/cards.png" alt="cards">
        </div>

        <button type="button" class="btn btn-danger" @click="() => $router.push('/make')">Make your next gift
            card</button>

        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Who are we?</h5>
                <p class="card-text">At E-cards we are disrupting the greeting card business and taking on big card to
                    bring to you a completely free* greeting card exchange service.</p>
                <p class="tiny" style="text-align: center">*By using this website you agree to us using all your data to
                    train AGI in preparation for the great summoning.</p>
                <p class="tiniTiny" style="text-align: center">*Also by using this website you agree to giving your soul
                    to our lord and destroyer Cthulhu</p>
            </div>
        </div>

    </main>
</template>

<style scoped>
.btn {
    font-size: 2rem;
    margin: 20px auto;
}

.main-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    height: calc(100vh - 56px);
    max-width: 1200px;
    margin: auto;
    padding: 0px 50px;
}

.banner-title {
    font-size: 4rem;
}

.banner-subtitle {
    font-size: 1.5rem;
    font-weight: 400;
    padding: 100px 20px;
}

.emphasis {
    color: #e5383b;
}

.banner {
    display: flex;
    flex-direction: column;
    text-align: center;
    align-items: center;
    padding: 50px 0px;
}

.banner img {
    max-width: 512px;
    max-height: 375px;
}

.tiny {
    font-size: 0.5em;
}

.tiniTiny {
    font-size: 0.1em;
}

.card {
    background-color: #F5F3F4;
    margin: 50px auto;
}


@media (min-width: 768px) {
    .banner {
        flex-direction: row;
        align-items: center;
    }

    .banner img {
        width: 50%;
    }

    .banner h1 {
        margin-right: 30px;
    }
}
</style>