<template>
    <div class="container">
        <div class="row row-cols-2 g-4 mt-4">
            <div v-for="shape in shapes" class="col">
                <button :key="shape.name" @click="selectShape(shape.name)">
                    <i class="bi " :class="shape.image" style="font-size: 3rem;" />
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
    { name: "Triangle", image: "bi-triangle" },
    { name: "Heart", image: "bi-heart" },
    { name: "Polygon", image: "bi-hexagon" },
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
                strokeWidth: 3,
            });
            break;
        case "Circle":
            konvaShape = new Konva.Circle({
                radius: 50,
                fill: "#FFFFFF",
                stroke: "#000000",
                strokeWidth: 3,
            });
            break;
        case "Star":
            konvaShape = new Konva.Star({
                numPoints: 5,
                innerRadius: 20,
                outerRadius: 50,
                fill: "#FFFFFF",
                stroke: "#000000",
                strokeWidth: 3,
            });
            break;
        case "Triangle":
            konvaShape = new Konva.Shape({
                width: 100,
                height: 100,
                sceneFunc: function (context, shape) {
                    const width = shape.width();
                    const height = shape.height();
                    context.beginPath();
                    context.moveTo(0, height);
                    context.lineTo(width, height);
                    context.lineTo(width / 2, 0);
                    context.lineTo(0, height);
                    context.closePath();
                    context.fillStrokeShape(shape);
                },
                fill: "#FFFFFF",
                stroke: "#000000",
                strokeWidth: 3,
            });
            konvaShape.className = "Triangle";            
            break;
        case "Heart":
            konvaShape = new Konva.Shape({
                width: 100,
                height: 100,
                innerRadius: 30,
                bottomSharpness: 50,
                sceneFunc: function (context, shape) {
                    const width = shape.width();
                    const height = shape.height();
                    context.beginPath();
                    context.moveTo(width / 2, height);
                    context.bezierCurveTo(
                        -width / 2,
                        height - shape.getAttr("bottomSharpness"),
                        width / 4,
                        -height / 2,
                        width / 2,
                        shape.getAttr("innerRadius")
                    );
                    context.bezierCurveTo(
                        (width * 3) / 4,
                        -height / 2,
                        width * 1.5,
                        height - shape.getAttr("bottomSharpness"),
                        width / 2,
                        height
                    );
                    context.closePath();
                    context.fillStrokeShape(shape);
                },
                fill: "#FFFFFF",
                stroke: "#000000",
                strokeWidth: 3,
            });
            konvaShape.className = "Heart";
            break;
        case "Polygon":
            konvaShape = new Konva.RegularPolygon({
                radius: 50,
                sides: 6,
                fill: "#FFFFFF",
                stroke: "#000000",
                strokeWidth: 3,
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