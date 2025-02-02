<template>
    <div class="p-4 bg-gray-100 rounded-lg shadow-md const-width">
        <h3 class="text-lg font-semibold mb-3">{{ shapeType }} Properties</h3>
        <form @input="updateShape" @keydown.enter.prevent="">
            <div class="container px-0">
                <div class="row gy-2 gx-4">
                    <div v-if="hasProperty('fill')" class="col-md-6">
                        <label class="form-label">Fill Color:</label>
                        <input v-model="fill" type="color" class="form-control form-control-color" />
                    </div>
                    <div v-if="hasProperty('stroke')" class="col-md-6">
                        <label class="form-label">Stroke Color:</label>
                        <input v-model="stroke" type="color" class="form-control form-control-color" />
                    </div>
                    <div v-if="hasProperty('strokeWidth')" class="col-md-6">
                        <label class="form-label">Stroke Width:</label>
                        <input v-model.number="strokeWidth" type="number" min="0" class="form-control" />
                    </div>
                    <div v-if="hasProperty('opacity')" class="col-md-6">
                        <label class="form-label">Opacity:</label>
                        <input v-model.number="opacity" type="range" min="0" max="1" step="0.01" class="form-range" />
                    </div>
                    <div v-if="hasProperty('text')" class="col-12">
                        <label class="form-label">Text:</label>
                        <textarea v-model="text" class="form-control" rows="3"></textarea>
                    </div>
                    <div v-if="hasProperty('fontSize')" class="col-md-6">
                        <label class="form-label">Font Size:</label>
                        <input v-model.number="fontSize" type="number" min="1" class="form-control" />
                    </div>
                    <div v-if="hasProperty('fontFamily')" class="col-md-6">
                        <label class="form-label">Font Family:</label>
                        <select v-model="fontFamily" class="form-select">
                            <option value="Arial">Arial</option>
                            <option value="Times New Roman">Times New Roman</option>
                            <option value="Verdana">Verdana</option>
                            <option value="Courier New">Courier New</option>
                        </select>
                    </div>
                    <div v-if="hasProperty('numPoints')" class="col-md-6">
                        <label class="form-label">Num Points:</label>
                        <input v-model.number="numPoints" type="number" min="1" class="form-control" />
                    </div>
                    <div v-if="hasProperty('innerRadius')" class="col-md-6">
                        <label class="form-label">Inner Radius:</label>
                        <input v-model.number="innerRadius" type="number" min="0" class="form-control" />
                    </div>
                    <div v-if="hasProperty('outerRadius')" class="col-md-6">
                        <label class="form-label">Outer Radius:</label>
                        <input v-model.number="outerRadius" type="number" min="0" class="form-control" />
                    </div>
                    <div class="col-12">
                        <button @click="$emit('delete')" class="mt-2 btn btn-danger w-100">Delete</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, computed } from 'vue';
import Konva from 'konva';

const props = defineProps<{ shape: Konva.Shape }>();
const emit = defineEmits(["delete"]);

const shapeType = computed(() => props.shape.getClassName());

const properties: Record<string, string[]> = {
    Rect: ['stroke', 'strokeWidth', 'fill', 'cornerRadius', 'opacity'],
    Circle: ['stroke', 'strokeWidth', 'fill', 'opacity'],
    Image: ['opacity'],
    Text: ['text', 'fontSize', 'fontFamily', 'fill', 'opacity'],
    Star: ['stroke', 'strokeWidth', 'fill', 'opacity', 'numPoints', 'innerRadius', 'outerRadius']
};

const hasProperty = (prop: string) => properties[shapeType.value]?.includes(prop);

const fill = ref(props.shape.fill() || '#000000');
const stroke = ref(props.shape.stroke() || '#000000');
const strokeWidth = ref(props.shape.strokeWidth() || 1);
const opacity = ref(props.shape.opacity() || 1);
const text = ref((props.shape as Konva.Text).text?.() || '');
const fontSize = ref((props.shape as Konva.Text).fontSize?.() || 16);
const fontFamily = ref((props.shape as Konva.Text).fontFamily?.() || 'Arial');
const numPoints = ref((props.shape as Konva.Star).numPoints?.() || 5);
const innerRadius = ref((props.shape as Konva.Star).innerRadius?.() || 10);
const outerRadius = ref((props.shape as Konva.Star).outerRadius?.() || 20);

const updateShape = () => {
    if (hasProperty('fill')) props.shape.fill(fill.value);
    if (hasProperty('stroke')) props.shape.stroke(stroke.value);
    if (hasProperty('strokeWidth')) props.shape.strokeWidth(strokeWidth.value);
    if (hasProperty('opacity')) props.shape.opacity(opacity.value);
    if (hasProperty('text')) (props.shape as Konva.Text).text(text.value);
    if (hasProperty('fontSize')) (props.shape as Konva.Text).fontSize(fontSize.value);
    if (hasProperty('fontFamily')) (props.shape as Konva.Text).fontFamily(fontFamily.value);
    if (hasProperty('numPoints')) (props.shape as Konva.Star).numPoints(numPoints.value);
    if (hasProperty('innerRadius')) (props.shape as Konva.Star).innerRadius(innerRadius.value);
    if (hasProperty('outerRadius')) (props.shape as Konva.Star).outerRadius(outerRadius.value);
    props.shape.getLayer()?.batchDraw();
};

watch([fill, stroke, strokeWidth, opacity, text, fontSize, fontFamily, numPoints, innerRadius, outerRadius], () => {
    updateShape();
});

watch(() => props.shape, (newShape) => {
    fill.value = newShape.fill() || '#000000';
    stroke.value = newShape.stroke() || '#000000';
    strokeWidth.value = newShape.strokeWidth() || 1;
    opacity.value = newShape.opacity() || 1;
    text.value = (newShape as Konva.Text).text?.() || '';
    fontSize.value = (newShape as Konva.Text).fontSize?.() || 16;
    fontFamily.value = (newShape as Konva.Text).fontFamily?.() || 'Arial';
    numPoints.value = (newShape as Konva.Star).numPoints?.() || 5;
    innerRadius.value = (newShape as Konva.Star).innerRadius?.() || 10;
    outerRadius.value = (newShape as Konva.Star).outerRadius?.() || 20;
}, { deep: true });
</script>

<style scoped>
.const-width {
    width: 360px;
}
</style>