<template>
    <div :style="{ display: isCurrentPage ? 'block' : 'none' }" class="canvas-container" ref="canvas-container"></div>
</template>

<script setup lang="ts">
import { onMounted, ref, useTemplateRef } from 'vue';
import Konva from 'konva';
import * as Guides from '@/scripts/Guides';
import { clamp } from '@/scripts/Utils';

const isCurrentPage = ref(false);
const container = useTemplateRef("canvas-container");

var lineGuideStops: ReturnType<typeof Guides.getLineGuideStops>;
var stage: Konva.Stage;
var layer: Konva.Layer;
var tr: Konva.Transformer;

const props = defineProps<{ page: string }>();

const emit = defineEmits<{
    openOptions: [node: Konva.Shape],
    closeOptions: [],
    updatePastePoint: [x: number, y: number],
}>();
defineExpose({
    deleteSelected, 
    addNode,
    select,
    deselect,
    selectThisCanvas,
    deselectThisCanvas,
    fitStageIntoParentContainer,
    copy,
    paste,
    toBlob,
    toImage,
    addImage,
    stage: () => stage,
    layer: () => layer,
    tr: () => tr,
    page: () => props.page,
});

const pageSizes: { [key: string]: { width: number; height: number } } = {
    "front": { width: 1414 / 2, height: 1000 },
    "inside": { width: 1414, height: 1000 },
    "back": { width: 1414 / 2, height: 1000 },
}

function deleteSelected() {
    if (tr.nodes().length > 0) emit("closeOptions");
    tr.nodes().forEach((item) => item.destroy());
    tr.nodes([]);
    layer.batchDraw();
}
function addNode(node: Konva.Shape) {
    
    // position the node at the middle
    node.x(stage.width() / stage.scaleX() / 2);
    node.y(stage.height() / stage.scaleY() / 2);
    // set up listeners
    node.on('mouseover', function () {
        document.body.style.cursor = 'pointer';
    });
    node.on('mouseout', function () {
        document.body.style.cursor = 'default';
    });
    node.on('dragmove', () => {
        node.x(clamp(node.x(), -node.width(), stage.width() / stage.scaleX() + node.height()));
        node.y(clamp(node.y(), -node.height(), stage.height() / stage.scaleY() + node.height()));
    });

    layer.add(node);
    emit("openOptions", node);
    select([node]);
    tr.setZIndex(layer.children.length - 1);

    lineGuideStops = Guides.getLineGuideStops([node], stage, layer, props.page == "inside");
}

function createStage(page: string): Konva.Stage {
    container.value!.id = `canvas-container-${page}`;
    
    var size = pageSizes[page];
    stage = new Konva.Stage({
        container: container.value!.id,
        width: Math.min(size.width),
        height: Math.min(size.height)
    });
    // set up layers
    const bgLayer = new Konva.Layer();
    bgLayer.add(new Konva.Rect({
        fill: '#FFFFFF',
        x: 0,
        y: 0,
        width: size.width,
        height: size.height
    }))
    if (page == "inside") { // middle bend line
        bgLayer.add(new Konva.Line({
            points: [size.width / 2, 0, size.width / 2, size.height],
            stroke: '#D3D3D3',
            strokeWidth: 1
        }));
    }
    stage.add(bgLayer);
    layer = new Konva.Layer();
    stage.add(layer);

    //set up transformer
    tr = new Konva.Transformer();
    tr.flipEnabled(true);
    tr.rotationSnaps([0, 45, 90, 135, 180, 225, 270, 315]);
    tr.rotationSnapTolerance(3);
    layer.add(tr);

    // selection handling 
    stage.on('click tap', function (e) {
        // Remove all selections
        if (e.target instanceof Konva.Stage || e.target.getLayer() === bgLayer) {
            deselect()
            emit("closeOptions");
            const point = stage.getPointerPosition();
            if (point) {
                emit("updatePastePoint", point.x, point.y);
            }
            return;
        }
        if (e.target.getLayer() !== layer) {
            return;
        }
        // Select or unselect elements
        const metaPressed = e.evt.ctrlKey || e.evt.metaKey;
        const isSelected = tr.nodes().indexOf(e.target) >= 0;

        // select only the element
        if (!metaPressed && !isSelected) {
            emit("openOptions", e.target);
            select([e.target])
            lineGuideStops = Guides.getLineGuideStops(tr.nodes() as Konva.Shape[], stage, layer, page == "inside");
        // deselect only the element
        } else if (metaPressed && isSelected) {
            const nodes = tr.nodes().slice();
            nodes.splice(nodes.indexOf(e.target), 1);
            e.target.setDraggable(false);
            tr.nodes(nodes);
            if (nodes.length == 0) emit("closeOptions");
            lineGuideStops = Guides.getLineGuideStops(tr.nodes() as Konva.Shape[], stage, layer, page == "inside");
        // add element to selection
        } else if (metaPressed && !isSelected) {
            e.target.setDraggable(true);
            const nodes = tr.nodes().concat([e.target]);
            if (nodes.length == 1) {
                emit("openOptions", e.target);
            } else emit("closeOptions");
            tr.nodes(nodes);
            lineGuideStops = Guides.getLineGuideStops(tr.nodes() as Konva.Shape[], stage, layer, page == "inside");
        }
    });
    // guide lines on moving a selected shape
    layer.on('dragmove', function (e) {
        if (!(e.target instanceof Konva.Shape)) return;

        // clear all previous lines on the screen
        layer.find('.guid-line').forEach((l) => l.destroy());

        var itemBounds = Guides.getObjectSnappingEdges(tr.nodes() as Konva.Shape[], e.target);
        var guides = Guides.getGuides(lineGuideStops, itemBounds);

        if (!guides.length) return;
        Guides.drawGuides(guides, layer);

        var absPos = e.target.absolutePosition();
        guides.forEach((lg) => {
            switch (lg.orientation) {
                case 'V': {
                    absPos.x = lg.lineGuide + lg.offset;
                    break;
                }
                case 'H': {
                    absPos.y = lg.lineGuide + lg.offset;
                    break;
                }
            }
        });

        e.target.absolutePosition(absPos);
    });

    layer.on('dragend', function (e) {
        layer.find('.guid-line').forEach((l) => l.destroy());
    });

    bgLayer.draw();
    layer.draw();
    return stage;
}
function select(nodes: Konva.Shape[]){
    tr.nodes().forEach(element => {
        element.setDraggable(false);
    });
    tr.nodes(nodes);
    nodes.forEach(node => node.setDraggable(true));
    if (nodes.length == 1) emit("openOptions", nodes[0]);
}
function deselect(){
    select([]);
}
function selectThisCanvas(){
    isCurrentPage.value = true;
}
function deselectThisCanvas(){
    isCurrentPage.value = false;
    deselect();
}
function fitStageIntoParentContainer(scale: number){
    
    stage.width(pageSizes[props.page].width * scale);
    stage.height(pageSizes[props.page].height * scale);

    stage.scaleX(scale);
    stage.scaleY(scale);
}
function copy(){
    
    var copiedShapes = tr.nodes();
    var midpoint = { x: 10, y: 10 };
    copiedShapes.forEach((shape) => {
        midpoint.x += shape.x();
        midpoint.y += shape.y();
    });
    midpoint.x /= copiedShapes.length;
    midpoint.y /= copiedShapes.length;
    return {
        copiedShapes: copiedShapes,
        pastePoint: midpoint
    }
}
function paste(copiedShapes: Konva.Node[], pastePoint: {x:number,y:number}){
    
    var midpoint = { x: 0, y: 0 };
    copiedShapes.forEach((shape) => {
        midpoint.x += shape.x();
        midpoint.y += shape.y();
    });
    midpoint.x /= copiedShapes.length;
    midpoint.y /= copiedShapes.length;
    const newSelect: Konva.Shape[] = [];
    copiedShapes.forEach((shape) => {
        var clone = shape.clone();
        clone.x(pastePoint.x + shape.x() - midpoint.x);
        clone.y(pastePoint.y + shape.y() - midpoint.y);
        layer.add(clone);
        newSelect.push(clone);
    });
    tr.setZIndex(layer.children.length - 1);
    select(newSelect);
    pastePoint.x += 10;
    pastePoint.y += 10;
    return {
        copiedShapes: newSelect,
        pastePoint : pastePoint
    }
}
function toImage() {

    const ogWidth = stage.width();
    const ogHeight = stage.height();
    const ogScale = stage.scale();

    stage.width(pageSizes[props.page].width)
        .height(pageSizes[props.page].height)
        .scale({ x: 1, y: 1 });
    stage.batchDraw();

    const result = stage.toDataURL({
        pixelRatio: 1,
        mimeType: 'image/png',
        quality: 1
    });

    stage.width(ogWidth)
        .height(ogHeight)
        .scale(ogScale);
    stage.batchDraw();

    return result;
}
async function toBlob() {

    const ogWidth = stage.width();
    const ogHeight = stage.height();
    const ogScale = stage.scale();

    stage.width(pageSizes[props.page].width)
        .height(pageSizes[props.page].height)
        .scale({ x: 1, y: 1 });
    stage.batchDraw();

    const result = await stage.toBlob({
        pixelRatio: 1,
        mimeType: 'image/png',
        quality: 1
    });

    stage.width(ogWidth)
        .height(ogHeight)
        .scale(ogScale);
    stage.batchDraw();

    return result;
}
function addImage(img: HTMLImageElement) {
    const landscape = img.width > img.height;
    const maxWidth = Math.min(img.width, pageSizes[props.page].width);
    const maxHeight = Math.min(img.height, pageSizes[props.page].height);
    const scaleX = maxWidth / img.width;
    const scaleY = maxHeight / img.height;
    const scale = Math.min(scaleX, scaleY);

    const imageNode = new Konva.Image({
        image: img,
        width: img.width * scale,
        height: img.height * scale,
    });

    var newScale = 1;
    if (imageNode.width() > stage.width() / stage.scaleX() / 2 && landscape) {
        newScale = (stage.width() / stage.scaleX() / 2) / imageNode.width();
    } else if (imageNode.height() > stage.height() / stage.scaleY() / 2 && !landscape) {
        newScale = (stage.height() / stage.scaleY() / 2) / imageNode.height();
    }
    imageNode.scaleY(newScale);
    imageNode.scaleX(newScale);
    addNode(imageNode);
}
onMounted(() => {
    createStage(props.page);
});
</script>

<style scoped>

.canvas-container {
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 70px;
}

</style>
