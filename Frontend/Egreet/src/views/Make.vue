<template>
    <div class="screen">
        <header>
            <NavigationBar>
                <template #middle>
                    <div class="btn-group" role="group">
                        <button type="button" class="btn me-3 align-items-center d-flex py-0" @click="addText">
                            <i class="bi bi-textarea-t px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Text</span>
                        </button>
                        <button type="button" class="btn me-3 align-items-center d-flex py-0"
                            @click="openShapesSidebar">
                            <i class="bi bi-plus-square-dotted px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Shape</span>
                        </button>
                        <!-- <button type="button" class="btn me-3 align-items-center d-flex py-0" @click="openStickerSidebar">
                            <i class="bi bi-sticky px-2 my-0" style="font-size: 1.5rem"/>
                            <span>Add Sticker</span>
                        </button> -->
                        <button type="button" class="btn align-items-center d-flex py-0" @click="fileInput?.click()">
                            <i class="bi bi-image px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Image</span>
                        </button>
                        <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;"
                            accept="image/*" />
                    </div>
                </template>
                <template #end>
                    <button type="button" class="btn btn-danger" @click="downloadImage()">
                        Download
                    </button>
                </template>
            </NavigationBar>
        </header>
        <div style="position:relative">
            <main class="main-container" ref="main-container">
                <div :style="{ display: currentPage === 'front' ? 'block' : 'none' }" class="canvas-container"
                    id="canvas-container-front" ref="canvas-container-front"></div>
                <div :style="{ display: currentPage === 'inside' ? 'block' : 'none' }" class="canvas-container"
                    id="canvas-container-inside" ref="canvas-container-inside"></div>
                <div :style="{ display: currentPage === 'back' ? 'block' : 'none' }" class="canvas-container"
                    id="canvas-container-back" ref="canvas-container-back"></div>
            </main>
            <SideBar ref="sidebar">
                <div ref="sidebarSlot"></div>
            </SideBar>
        </div>
        <footer>
            <div class="btn-group" role="group">
                <button @click="switchPage('front')" :class="{ active: currentPage === 'front' }">
                    <div style="transform: scale(1.5, 2.5)"><i class="bi bi-wallet2 px-2 my-0" /></div>
                </button>
                <button @click="switchPage('inside')" :class="{ active: currentPage === 'inside' }">
                    <div style="transform: scale(2.5, 3)"><i class="bi bi-postcard px-2 my-0" /></div>
                </button>
                <button @click="switchPage('back')" :class="{ active: currentPage === 'back' }">
                    <div style="transform: scale(-1.5, 2.5)"><i class="bi bi-wallet2 px-2 my-0" /></div>
                </button>
            </div>
        </footer>
    </div>
</template>

<script setup lang="ts">
import { createVNode, nextTick, onMounted, ref, render, useTemplateRef } from 'vue';
import NavigationBar from '@/components/NavigationBar.vue';
import SideBar from '@/components/SideBar.vue';
import ShapeOptions from '@/components/ShapeOptions.vue';
import ShapeCreate from '@/components/ShapeCreate.vue';
import Konva from 'konva';

function clamp(value: number, min: number, max: number): number {
    return Math.min(Math.max(min, value), max);
}
function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
        const file = input.files[0];
        const reader = new FileReader();
        reader.onload = function (e) {
            const img = new Image();
            img.onload = function () {
                addImage(img);
                if (input) input.value = '';
            };
            img.onerror = function () {
                console.error('Error loading image');
                if (input) input.value = '';
            };
            img.src = e.target?.result as string;
        };
        reader.onerror = function () {
            console.error('Error reading file');
            if (input) input.value = '';
        };
        reader.readAsDataURL(file);
    }
}
function addImage(img: HTMLImageElement) {
    const landscape = img.width > img.height;
    const maxWidth = Math.min(img.width, pageSizes[currentPage.value].width);
    const maxHeight = Math.min(img.height, pageSizes[currentPage.value].height);
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
function openOptionsSidebar(selectedItem: any) {
    if (sidebarSlot.value && sidebarSlot.value.hasChildNodes()) {
        render(null, sidebarSlot.value);
    }
    if (!(selectedItem instanceof Konva.Shape)) {
        console.error("You some how selected a non Knova shape");
        return;
    }
    const shapeOptionsVNode = createVNode(ShapeOptions, { shape: selectedItem });

    shapeOptionsVNode.props = {
        shape: selectedItem,
        onDelete: deleteSelected
    };

    if (sidebarSlot.value) {
        render(shapeOptionsVNode, sidebarSlot.value);
    } else console.error("sidebar slot is not there");

    sidebar.value?.expandSidebar();
}
function closeSidebar() {
    sidebar.value?.retractSidebar();
    if (sidebarSlot.value) {
        render(null, sidebarSlot.value);
    }
}
function deleteSelected() {
    closeSidebar();
    tr.nodes().forEach((item) => item.destroy());
    tr.nodes([]);
    layer.batchDraw();
}
function addNode(node: Konva.Shape) {
    node.x(stage.width() / stage.scaleX() / 2);
    node.y(stage.height() / stage.scaleY() / 2);
    node.on('mouseover', function () {
        document.body.style.cursor = 'pointer';
    });
    node.on('mouseout', function () {
        document.body.style.cursor = 'default';
    });
    node.on('dragmove', () => {
        node.x(clamp(node.x(), -node.width(), stage.width() / stage.scaleX()));
        node.y(clamp(node.y(), -node.height(), stage.height() / stage.scaleY()));
    });
    layer.add(node);
    openOptionsSidebar(node);
    node.setDraggable(true);
    tr.nodes().forEach(element => {
        element.setDraggable(false);
    });
    tr.nodes([node]);
    tr.resizeEnabled(!(node instanceof Konva.Text));
    tr.setZIndex(layer.children.length - 1);
    lineGuideStops = getLineGuideStops([node]);
}
function addText() {
    var text = new Konva.Text({
        text: 'Sample Text',
        fontSize: 30,
        fontFamily: 'Calibri',
        fill: '#000000',
    });
    addNode(text);
}
function openShapesSidebar() {
    const shapeCreateVNode = createVNode(ShapeCreate);

    shapeCreateVNode.props = {
        onShapeSelected: addNode
    };

    if (sidebarSlot.value) {
        render(shapeCreateVNode, sidebarSlot.value);
    } else console.error("sidebar slot is not there");

    sidebar.value?.expandSidebar()
}

function createStage(page: string): Konva.Stage {
    var size = pageSizes[page];
    const newStage = new Konva.Stage({
        container: `canvas-container-${page}`,
        width: Math.min(size.width),
        height: Math.min(size.height)
    });
    const bgLayer = new Konva.Layer();
    bgLayer.add(new Konva.Rect({
        fill: '#FFFFFF',
        x: 0,
        y: 0,
        width: size.width,
        height: size.height
    }))
    if (page == "inside") {
        bgLayer.add(new Konva.Line({
            points: [size.width / 2, 0, size.width / 2, size.height],
            stroke: '#D3D3D3',
            strokeWidth: 1
        }));
    }
    newStage.add(bgLayer);
    const drawLayer = new Konva.Layer();
    newStage.add(drawLayer);
    const transformer = new Konva.Transformer();
    transformer.flipEnabled(true);
    transformer.rotationSnaps([0, 45, 90, 135, 180, 225, 270, 315]);
    transformer.rotationSnapTolerance(3);

    drawLayer.add(transformer);

    // selection handling 
    newStage.on('click tap', function (e) {
        // Remove all selections
        if (e.target instanceof Konva.Stage || e.target.getLayer() === bgLayer) {
            transformer.nodes().forEach(element => {
                element.setDraggable(false);
            });
            closeSidebar();
            transformer.nodes([]);
            transformer.resizeEnabled(true);
            return;
        }
        if (e.target.getLayer() !== layer) {
            return;
        }
        // Select or unselect elements
        const metaPressed = e.evt.ctrlKey || e.evt.metaKey;
        const isSelected = transformer.nodes().indexOf(e.target) >= 0;

        if (!metaPressed && !isSelected) {
            openOptionsSidebar(e.target);
            e.target.setDraggable(true);
            transformer.nodes().forEach(element => {
                element.setDraggable(false);
            });
            transformer.nodes([e.target]);
            transformer.resizeEnabled(!(e.target instanceof Konva.Text));
            lineGuideStops = getLineGuideStops(transformer.nodes() as Konva.Shape[]);

        } else if (metaPressed && isSelected) {
            const nodes = transformer.nodes().slice();
            nodes.splice(nodes.indexOf(e.target), 1);
            if (nodes.length == 0) closeSidebar();
            e.target.setDraggable(false);
            transformer.nodes(nodes);
            transformer.resizeEnabled(!nodes.some(node => node instanceof Konva.Text));
            lineGuideStops = getLineGuideStops(transformer.nodes() as Konva.Shape[]);
        } else if (metaPressed && !isSelected) {
            e.target.setDraggable(true);
            const nodes = transformer.nodes().concat([e.target]);
            if (nodes.length == 1) openOptionsSidebar(e.target);
            else closeSidebar();
            transformer.nodes(nodes);
            if (e.target instanceof Konva.Text) transformer.resizeEnabled(false);
            lineGuideStops = getLineGuideStops(transformer.nodes() as Konva.Shape[]);
        }
    });
    
    drawLayer.on('dragmove', function (e) {
        if (!(e.target instanceof Konva.Shape)) return;

        // clear all previous lines on the screen
        drawLayer.find('.guid-line').forEach((l) => l.destroy());
        
        var itemBounds = getObjectSnappingEdges(tr.nodes() as Konva.Shape[], e.target);
        var guides = getGuides(lineGuideStops, itemBounds);

        if (!guides.length) return;
        drawGuides(guides);

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

    drawLayer.on('dragend', function (e) {
        drawLayer.find('.guid-line').forEach((l) => l.destroy());
    });

    bgLayer.draw();
    drawLayer.draw();
    return newStage;
}
function switchPage(page: string) {
    if (tr) {
        tr.nodes().forEach(element => {
            element.setDraggable(false);
        });
        closeSidebar();
        tr.nodes([]);
        tr.resizeEnabled(true);
    }
    currentPage.value = page;
    stage = stageMap.get(page)!;
    layer = stage.getLayers()[1];
    tr = layer.getChildren().find((child) => child instanceof Konva.Transformer) as Konva.Transformer;

    nextTick(() => {
        fitStageIntoParentContainer();
    });
}
function fitStageIntoParentContainer() {
    if (!mainContainer.value) return;
    var container = mainContainer.value;

    var containerWidth = container.offsetWidth - 50;
    var containerHeight = container.offsetHeight - 50;

    var scaleX = containerWidth / pageSizes[currentPage.value].width;
    var scaleY = containerHeight / pageSizes[currentPage.value].height;

    var scale = Math.min(scaleX, scaleY, 1);

    stage.width(pageSizes[currentPage.value].width * scale);
    stage.height(pageSizes[currentPage.value].height * scale);

    stage.scaleX(scale);
    stage.scaleY(scale);
}
function downloadImage() {
    const dataURL = stage.toDataURL({ pixelRatio: 1 });
    const link = document.createElement('a');
    link.href = dataURL;
    link.download = `${currentPage.value}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function getLineGuideStops(skipShapes: Konva.Shape[]) {
    // snap to stage
    var vertical = [0, stage.width() / 2, stage.width()];
    var horizontal = [0, stage.height() / 2, stage.height()];

    if (currentPage.value == "inside") vertical.push(stage.width() / 4, stage.width() * 3 / 4);

    // snap over edges and center of each object on the canvas
    layer.children.forEach((guideItem) => {
        if (!(guideItem instanceof Konva.Shape)) return;
        if (skipShapes.includes(guideItem)) {
            return;
        }
        var box = guideItem.getClientRect();

        vertical.push(box.x, box.x + box.width, box.x + box.width / 2);
        horizontal.push(box.y, box.y + box.height, box.y + box.height / 2);
    });
    return {
        vertical: vertical,
        horizontal: horizontal,
    };
}
function getObjectSnappingEdges(nodes: Konva.Shape[], absNode: Konva.Shape) {
    let minX = Infinity;
    let minY = Infinity;
    let maxX = -Infinity;
    let maxY = -Infinity;
    
    const absPos = absNode.absolutePosition();
    
    nodes.forEach(node => {
        const box = node.getClientRect();
        minX = Math.min(minX, box.x);
        minY = Math.min(minY, box.y);
        maxX = Math.max(maxX, box.x + box.width);
        maxY = Math.max(maxY, box.y + box.height);
    });
    
    const width = maxX - minX;
    const height = maxY - minY;
    
    return {
        vertical: [
            {
                guide: Math.round(minX),
                offset: Math.round(absPos.x - minX),
                snap: 'start',
            },
            {
                guide: Math.round(minX + width / 2),
                offset: Math.round(absPos.x - minX - width / 2),
                snap: 'center',
            },
            {
                guide: Math.round(maxX),
                offset: Math.round(absPos.x - minX - width),
                snap: 'end',
            },
        ],
        horizontal: [
            {
                guide: Math.round(minY),
                offset: Math.round(absPos.y - minY),
                snap: 'start',
            },
            {
                guide: Math.round(minY + height / 2),
                offset: Math.round(absPos.y - minY - height / 2),
                snap: 'center',
            },
            {
                guide: Math.round(maxY),
                offset: Math.round(absPos.y - minY - height),
                snap: 'end',
            },
        ],
    };
}
function getGuides(lineGuideStops: ReturnType<typeof getLineGuideStops>, itemBounds: ReturnType<typeof getObjectSnappingEdges>) {
    var resultV: { lineGuide: any; diff: number; snap: any; offset: any; }[] = [];
    var resultH: { lineGuide: any; diff: number; snap: any; offset: any; }[] = [];

    lineGuideStops.vertical.forEach((lineGuide) => {
        itemBounds.vertical.forEach((itemBound) => {
            var diff = Math.abs(lineGuide - itemBound.guide);
            if (diff < GUIDELINE_OFFSET) {
                resultV.push({
                    lineGuide: lineGuide,
                    diff: diff,
                    snap: itemBound.snap,
                    offset: itemBound.offset,
                });
            }
        });
    });

    lineGuideStops.horizontal.forEach((lineGuide) => {
        itemBounds.horizontal.forEach((itemBound) => {
            var diff = Math.abs(lineGuide - itemBound.guide);
            if (diff < GUIDELINE_OFFSET) {
                resultH.push({
                    lineGuide: lineGuide,
                    diff: diff,
                    snap: itemBound.snap,
                    offset: itemBound.offset,
                });
            }
        });
    });

    var guides = [];

    // find closest snap
    var minV = resultV.sort((a, b) => a.diff - b.diff)[0];
    var minH = resultH.sort((a, b) => a.diff - b.diff)[0];
    if (minV) {
        guides.push({
            lineGuide: minV.lineGuide,
            offset: minV.offset,
            orientation: 'V',
            snap: minV.snap,
        });
    }
    if (minH) {
        guides.push({
            lineGuide: minH.lineGuide,
            offset: minH.offset,
            orientation: 'H',
            snap: minH.snap,
        });
    }
    return guides;
}
function drawGuides(guides: ReturnType<typeof getGuides>) {
    guides.forEach((lg) => {
        if (lg.orientation === 'H') {
            var line = new Konva.Line({
                points: [-6000, 0, 6000, 0],
                stroke: 'rgb(0, 161, 255)',
                strokeWidth: 1,
                name: 'guid-line',
                dash: [4, 6],
            });
            layer.add(line);
            line.absolutePosition({
                x: 0,
                y: lg.lineGuide,
            });
        } else if (lg.orientation === 'V') {
            var line = new Konva.Line({
                points: [0, -6000, 0, 6000],
                stroke: 'rgb(0, 161, 255)',
                strokeWidth: 1,
                name: 'guid-line',
                dash: [4, 6],
            });
            layer.add(line);
            line.absolutePosition({
                x: lg.lineGuide,
                y: 0,
            });
        }
    });
}

const pageSizes: { [key: string]: { width: number; height: number } } = {
    "front": { width: 1414 / 2, height: 1000 },
    "inside": { width: 1414, height: 1000 },
    "back": { width: 1414 / 2, height: 1000 },
}

const currentPage = ref("front");
const settingUp = ref(true);
const stageMap = new Map<string, Konva.Stage>();
const fileInput = useTemplateRef("fileInput");
const sidebar = useTemplateRef("sidebar");
const sidebarSlot = useTemplateRef("sidebarSlot");
const mainContainer = useTemplateRef("main-container");
const GUIDELINE_OFFSET = 5;
var lineGuideStops: ReturnType<typeof getLineGuideStops>;
var stage: Konva.Stage;
var layer: Konva.Layer;
var tr: Konva.Transformer;

onMounted(() => {
    stageMap.set("front", createStage("front"));
    stageMap.set("inside", createStage("inside"));
    stageMap.set("back", createStage("back"));
    switchPage('front');

    fitStageIntoParentContainer();
    window.addEventListener('resize', fitStageIntoParentContainer);

    settingUp.value = false;
});
</script>

<style scoped>
.screen {
    height: 100vh;
    background-color: #F5F3F4;
}

.main-container {
    background-color: #F5F3F4;
    width: 100%;
    display: flex;
    height: calc(100vh - 96px);
    justify-content: center;
    align-items: center;
}

@media (min-width: 996px) {
    .main-container {
        height: calc(100vh - 56px);
    }
}

.canvas-container {
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
}

footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    display: flex;
    align-items: end;
}

footer .btn-group {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    border-radius: 12px 12px 0 0;
    overflow: hidden;
}

footer .btn-group button {
    padding: 24px 32px;
    border: 1px solid #dbd5d4;
    border-bottom: 0px;
    background: white;
    cursor: pointer;
    border-radius: 0;
}

footer .btn-group button:first-child {
    border-radius: 12px 0 0 0;
}

footer .btn-group button:last-child {
    border-radius: 0 12px 0 0;
}

footer .btn-group button.active {
    background: #E5383B;
    color: white;
    border-color: #BA181B;
}
</style>