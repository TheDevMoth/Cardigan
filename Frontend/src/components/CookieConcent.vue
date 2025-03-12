<template>
    <div v-if="isVisible" class="cookie-consent">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                    <i class="bi bi-cookie"></i> Cookie Notice
                </h5>
                <button type="button" class="btn-close" aria-label="Close" @click="dismissNotification"></button>
            </div>
            <div class="card-body">
                <p v-if="!showCookie" class="card-text">This website does not use cookies!</p>
                <p v-else class="card-text">Okay, you can have one cookie 🍪</p>
                <div v-if="!showCookie" class="d-flex gap-2">
                    <button class="btn btn-danger" @click="dismissNotification">I understand</button>
                    <button class="btn btn-outline-secondary" @click="giveCookie">But I want cookies</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const isVisible = ref(localStorage.getItem('cookieAlertDismissed') !== 'true');
const showCookie = ref(false);

const dismissNotification = () => {
    isVisible.value = false;
    localStorage.setItem('cookieAlertDismissed', 'true');
};

const giveCookie = () => {
    showCookie.value = true;
    document.cookie = "cookie=🍪; path=/; max-age=86400";
    localStorage.setItem('cookieAlertDismissed', 'true');
};
</script>

<style scoped>
.cookie-consent {
    position: fixed;
    z-index: 1000;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 1rem;
}

@media (min-width: 576px) {
    .cookie-consent {
        width: 360px;
        bottom: 20px;
        right: 20px;
        left: auto;
    }
}

.card {
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>