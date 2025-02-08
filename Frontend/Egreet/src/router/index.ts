import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Make from "../views/Make.vue";
import Card from "../views/Card.vue";

const routes = [
    { path: "/", component: Home },
    { path: "/make", component: Make },
    { path: "/card", component: Card },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
