<template>
    <div class="container">
        <div class="row row-cols-2 g-4 mt-4">
            <div v-for="shape in shapes" class="col">
                <button :key="shape.name" @click="selectShape(shape.name)">
                    <i class="bi " :class="shape.image" style="font-size: 3rem;"/>
                    <span>{{ shape.name }}</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Konva from "konva";

const shapes = ref([
    { name: "Rectangle", image: "bi-square" },
    { name: "Circle", image: "bi-circle" },
    { name: "Star", image: "bi-star" },
]);

const emit = defineEmits<{ "shape-selected": [shape: Konva.Shape] }>();

const selectShape = (shape: string) => {
    let konvaShape: Konva.Shape | null = null;
    switch (shape) {
        case "Rectangle":
            konvaShape = new Konva.Rect({
                width: 100,
                height: 50,
                fill: "#FFFFFF",
                stroke: "#000000",
                strokeWidth: 2,
            });
            break;
        case "Circle":
            konvaShape = new Konva.Circle({
                radius: 50,
                fill: "#FFFFFF",
                stroke: "#000000",
                strokeWidth: 2,
            });
            break;
        case "Star":
            konvaShape = new Konva.Star({
                numPoints: 5,
                innerRadius: 20,
                outerRadius: 50,
                fill: "#FFFFFF",
                stroke: "#000000",
                strokeWidth: 2,
            });
            break;
    }
    if (konvaShape) emit("shape-selected", konvaShape);
};
</script>

<style scoped>
.shape-selector {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
}

button {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
    border: none;
    background-color: white;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    width: 100%;
}

button:hover {
    background-color: #f0f0f0;
}

.shape-image {
    width: 50px;
    height: 50px;
    margin-bottom: 5px;
}
</style>