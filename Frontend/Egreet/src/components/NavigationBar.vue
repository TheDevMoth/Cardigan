<template>
    <nav class="navbar navbar-expand-lg navbar-bg">
        <div class="container-fluid">
            <a class="navbar-brand on-navbar" href="#">E-Cards</a>
            <button class="navbar-toggler navbar-btn" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon "></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link on-navbar" :class="{ active: route.path === '/' }" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link on-navbar" :class="{ active: route.path === '/make' }" href="/make">Make</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';

const route = useRoute();
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

/* .navbar-bg {
      background-color: #f5f3f4;
  } */
.nav-link.active {
    color: #BA181B;
    /* font-weight: 500; */
}
</style>