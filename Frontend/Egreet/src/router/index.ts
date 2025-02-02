import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Make from "../views/Make.vue";

const routes = [
    { path: "/", component: Home },
    { path: "/make", component: Make },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
