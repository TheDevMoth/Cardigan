<template>
    <div class="screen">
        <header>
            <NavigationBar>
                <template #middle>
                    <div class="btn-group" role="group">
                        <button type="button" class="btn me-sm-4 me-lg-2 me-xl-4 px-1 align-items-center d-flex py-0" @click="addText">
                            <i class="bi bi-textarea-t px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Text</span>
                        </button>
                        <button type="button" class="btn me-sm-4 me-lg-2 me-xl-4 px-1 align-items-center d-flex py-0"
                            @click="openShapesSidebar">
                            <i class="bi bi-plus-square-dotted px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Shape</span>
                        </button>
                        <button type="button" class="btn me-sm-4 me-lg-2 me-xl-4 px-1 align-items-center d-flex py-0"
                            @click="openEmojiSidebar">
                            <i class="bi bi-emoji-wink px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Emoji</span>
                        </button>
                        <button type="button" class="btn align-items-center d-flex py-0 px-1" @click="fileInput?.click()">
                            <i class="bi bi-image px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Image</span>
                        </button>
                        <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;"
                            accept="image/*" />
                    </div>
                </template>
                <template #end>
                    <button type="button" class="btn btn-danger ps-3 rounded-4" data-bs-toggle="modal"
                        data-bs-target="#doneModal">
                        Done!
                        <i class="bi bi-chevron-right"></i>
                    </button>
                </template>
            </NavigationBar>
        </header>

        <!-- Modal -->
        <div class="modal fade" id="doneModal" tabindex="-1" aria-labelledby="doneModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="doneModalLabel">Share Options</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body p-0">
                        <div class="list-group">
                            <button type="button" class="list-group-item list-group-item-action py-3" data-bs-target="#shareModal" data-bs-toggle="modal" @click="shareCard">
                                Share as Cardigan card (url)
                            </button>
                            <button type="button" class="list-group-item list-group-item-action py-3"
                                @click="downloadImages">
                                Download as Images
                            </button>
                            <button type="button" class="list-group-item list-group-item-action py-3" @click="downloadPDF">
                                Download as PDF
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="shareModal" data-bs-backdrop="static" aria-hidden="true" aria-labelledby="shareModalLabel" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="shareModalLabel">{{ resultsReceived ? "Here is the link to your card" : "Your card is being created" }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeShareModal"></button>
                </div>
                <div class="modal-body">
                    <span v-if="resultsReceived">
                        {{ results }}
                    </span>
                    <div v-else>
                        This is supposed to be a loading bar...
                    </div>
                </div>
            </div>
        </div>
        </div>
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
import EmojiCreate from '@/components/EmojiCreate.vue';
import Konva from 'konva';
import * as Guides from '@/scripts/Guides';
import { clamp } from '@/scripts/Utils';
import type { Vector2d } from 'konva/lib/types';
import jsPDF from 'jspdf';
import axios from 'axios';
import { API_BASE_URL } from '@/scripts/Constants';

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

function openShapesSidebar() {
    const shapeCreateVNode = createVNode(ShapeCreate);

    shapeCreateVNode.props = {
        onShapeSelected: addNode
    };

    if (sidebarSlot.value) {
        render(shapeCreateVNode, sidebarSlot.value);
    } else console.error("sidebar slot is not there");

    sidebar.value?.forceExpandSidebar()
}

function openEmojiSidebar() {
    const emojiCreateVNode = createVNode(EmojiCreate);

    emojiCreateVNode.props = {
        onEmojiSelected: addNode
    };

    if (sidebarSlot.value) {
        render(emojiCreateVNode, sidebarSlot.value);
    } else console.error("sidebar slot is not there");

    sidebar.value?.forceExpandSidebar()
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
        node.x(clamp(node.x(), -node.width(), stage.width() / stage.scaleX() + node.height()));
        node.y(clamp(node.y(), -node.height(), stage.height() / stage.scaleY() + node.height()));
    });
    layer.add(node);
    openOptionsSidebar(node);
    node.setDraggable(true);
    tr.nodes().forEach(element => {
        element.setDraggable(false);
    });
    tr.nodes([node]);
    tr.setZIndex(layer.children.length - 1);
    lineGuideStops = Guides.getLineGuideStops([node], stage, layer, currentPage.value == "inside");
}

function addText() {
    var text = new Konva.Text({
        text: 'Sample Text',
        fontSize: 30,
        fontFamily: 'Calibri',
        fill: '#000000',
        name: "Text",
    });
    addNode(text);
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
            lineGuideStops = Guides.getLineGuideStops(transformer.nodes() as Konva.Shape[], stage, layer, currentPage.value == "inside");

        } else if (metaPressed && isSelected) {
            const nodes = transformer.nodes().slice();
            nodes.splice(nodes.indexOf(e.target), 1);
            if (nodes.length == 0) closeSidebar();
            e.target.setDraggable(false);
            transformer.nodes(nodes);
            lineGuideStops = Guides.getLineGuideStops(transformer.nodes() as Konva.Shape[], stage, layer, currentPage.value == "inside");
        } else if (metaPressed && !isSelected) {
            e.target.setDraggable(true);
            const nodes = transformer.nodes().concat([e.target]);
            if (nodes.length == 1) openOptionsSidebar(e.target);
            else closeSidebar();
            transformer.nodes(nodes);
            lineGuideStops = Guides.getLineGuideStops(transformer.nodes() as Konva.Shape[], stage, layer, currentPage.value == "inside");
        }
    });
    drawLayer.on('dragmove', function (e) {
        if (!(e.target instanceof Konva.Shape)) return;

        // clear all previous lines on the screen
        drawLayer.find('.guid-line').forEach((l) => l.destroy());

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

    var containerWidth = container.offsetWidth - 32;
    var containerHeight = container.offsetHeight - 150;

    var scaleX = containerWidth / pageSizes[currentPage.value].width;
    var scaleY = containerHeight / pageSizes[currentPage.value].height;

    var scale = Math.min(scaleX, scaleY, 1);

    stage.width(pageSizes[currentPage.value].width * scale);
    stage.height(pageSizes[currentPage.value].height * scale);

    stage.scaleX(scale);
    stage.scaleY(scale);
}

function stageToImage(page: string) {
    if (!["front", "inside", "back"].includes(page)) return;

    const lStage = stageMap.get(page)!;
    const ogWidth = lStage.width();
    const ogHeight = lStage.height();
    const ogScale = lStage.scale();

    lStage.width(pageSizes[page].width)
        .height(pageSizes[page].height)
        .scale({ x: 1, y: 1 });
    lStage.batchDraw();

    const result = lStage.toDataURL({
        pixelRatio: 1,
        mimeType: 'image/png',
        quality: 1
    });

    lStage.width(ogWidth)
        .height(ogHeight)
        .scale(ogScale);
    lStage.batchDraw();

    return result;
}
async function stageToBlob(page: string) {
    if (!["front", "inside", "back"].includes(page)) return;

    const lStage = stageMap.get(page)!;
    const ogWidth = lStage.width();
    const ogHeight = lStage.height();
    const ogScale = lStage.scale();

    lStage.width(pageSizes[page].width)
        .height(pageSizes[page].height)
        .scale({ x: 1, y: 1 });
    lStage.batchDraw();

    const result = await lStage.toBlob({
        pixelRatio: 1,
        mimeType: 'image/png',
        quality: 1
    });

    lStage.width(ogWidth)
        .height(ogHeight)
        .scale(ogScale);
    lStage.batchDraw();

    return result;
}
async function shareCard() {
    waitingForResult = true;
    
    const formData = new FormData();
    const pages = ['front', 'inside', 'back'];
    
    for (const page of pages) {
        const blob = await stageToBlob(page).then(blob => blob as Blob);
        if (blob) {
            formData.append(page, blob, `${page}.png`);
        }
    }

    try {
        const result = await axios.post(`${API_BASE_URL}/card/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        
        if (!waitingForResult) return;
        resultsReceived.value = true;
        results.value = `${window.location.origin}/card/${result.data.id}`;
    } catch (error: any) {
        if (!waitingForResult) return;
        results.value = `Error: ${error.message}`;
        resultsReceived.value = true;
    } finally {
        waitingForResult = false;
    }
}
function downloadImages() {
    stageMap.forEach((stage, page) => {
        const dataURL = stageToImage(page);
        if (!dataURL) return;

        const link = document.createElement('a');
        link.download = `card_${page}.png`;
        link.href = dataURL;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
}
function downloadPDF() {
    const pdf = new jsPDF({
        orientation: 'landscape',
        unit: 'pt',
        format: [1000, 1414]
    });

    const frontImg = stageToImage('front');
    const backImg = stageToImage('back');
    if (frontImg && backImg) {
        const frontStage = stageMap.get('front')!;
        frontStage.find('Text').forEach((text) => {
            var kText = text as Konva.Text;
            const size = kText.fontSize() / 0.75;
            pdf.setFontSize(size);
            pdf.text(kText.text(), kText.x() * kText.scaleX(), kText.y() * kText.scaleY(), {
                baseline: 'top',
                angle: -kText.getAbsoluteRotation(),
            });
        });

        pdf.addImage(frontImg, 'PNG', 0, 0, 707, 1000);

        const backStage = stageMap.get('back')!;
        backStage.find('Text').forEach((text) => {
            var kText = text as Konva.Text;
            const size = kText.fontSize() / 0.75;
            pdf.setFontSize(size);
            pdf.text(kText.text(), kText.x() * kText.scaleX() + 707, kText.y() * kText.scaleY(), {
                baseline: 'top',
                angle: -kText.getAbsoluteRotation(),
            });
        });

        pdf.addImage(backImg, 'PNG', 707, 0, 707, 1000);
    }

    // Second page: Inside
    pdf.addPage([1000, 1414]);
    const insideImg = stageToImage('inside');
    if (insideImg) {
        const insideStage = stageMap.get('inside')!;
        insideStage.find('Text').forEach((text) => {
            var kText = text as Konva.Text;
            const size = kText.fontSize() / 0.75;
            pdf.setFontSize(size);
            pdf.text(kText.text(), kText.x() * kText.scaleX(), kText.y() * kText.scaleY(), {
                baseline: 'top',
                angle: -kText.getAbsoluteRotation(),
            });
        });

        pdf.addImage(insideImg, 'PNG', 0, 0, 1414, 1000);
    }

    pdf.save('greeting_card.pdf');
}
function closeShareModal() {
    resultsReceived.value = false;
    waitingForResult = false;
    results.value = "";
}

const pageSizes: { [key: string]: { width: number; height: number } } = {
    "front": { width: 1414 / 2, height: 1000 },
    "inside": { width: 1414, height: 1000 },
    "back": { width: 1414 / 2, height: 1000 },
}

const currentPage = ref("front");
const stageMap = new Map<string, Konva.Stage>();
const fileInput = useTemplateRef("fileInput");
const sidebar = useTemplateRef("sidebar");
const sidebarSlot = useTemplateRef("sidebarSlot");
const mainContainer = useTemplateRef("main-container");
var copiedShapes: Konva.Node[] = [];
var pastePoint: Vector2d;

var lineGuideStops: ReturnType<typeof Guides.getLineGuideStops>;
var stage: Konva.Stage;
var layer: Konva.Layer;
var tr: Konva.Transformer;

const resultsReceived = ref(false);
var waitingForResult = false;
const results = ref("");

onMounted(() => {
    stageMap.set("front", createStage("front"));
    stageMap.set("inside", createStage("inside"));
    stageMap.set("back", createStage("back"));
    switchPage('front');

    fitStageIntoParentContainer();
    window.addEventListener('resize', fitStageIntoParentContainer);
    window.addEventListener('keydown', (event) => {
        if (event.key === 'Delete') {
            deleteSelected();
        } else if ((event.key === 'c' || event.key === 'C') && event.ctrlKey) {
            copiedShapes = tr.nodes();
            var midpoint = { x: 10, y: 10 };
            copiedShapes.forEach((shape) => {
                midpoint.x += shape.x();
                midpoint.y += shape.y();
            });
            midpoint.x /= copiedShapes.length;
            midpoint.y /= copiedShapes.length;
            pastePoint = midpoint;
        } else if ((event.key === 'v' || event.key === 'V') && event.ctrlKey) {
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
            tr.nodes().forEach(element => {
                element.setDraggable(false);
            });
            tr.nodes(newSelect);
            tr.nodes().forEach(element => {
                element.setDraggable(true);
            });
            copiedShapes = newSelect;
            var midpoint = { x: 10, y: 10 };
            copiedShapes.forEach((shape) => {
                midpoint.x += shape.x();
                midpoint.y += shape.y();
            });
            midpoint.x /= copiedShapes.length;
            midpoint.y /= copiedShapes.length;
            pastePoint = midpoint;
        }

    });
    window.addEventListener('mousedown', (event) => {
        const rect = stage.container().getBoundingClientRect();
        pastePoint = {
            x: clamp(event.clientX - rect.left, 0, stage.width() / stage.scaleX()),
            y: clamp(event.clientY - rect.top, 0, stage.height() / stage.scaleY())
        };
    });
    mainContainer.value?.addEventListener('click', (e) => {
        if (e.target !== mainContainer.value) return;
        
        tr.nodes().forEach(element => {
            element.setDraggable(false);
        });
        closeSidebar();
        tr.nodes([]);
        tr.resizeEnabled(true);
    })
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
    margin-bottom: 70px;
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