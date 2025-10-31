<template>
    <div class="screen">
        <header>
            <NavigationBar>
                <template #middle>
                    <div class="btn-group" role="group">
                        <button type="button" class="btn me-sm-4 me-md-2 me-xl-4 px-1 align-items-center d-flex py-0" @click="addText">
                            <i class="bi bi-textarea-t px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Text</span>
                        </button>
                        <button type="button" class="btn me-sm-4 me-md-2 me-xl-4 px-1 align-items-center d-flex py-0"
                            @click="openShapesSidebar">
                            <i class="bi bi-plus-square-dotted px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Shape</span>
                        </button>
                        <button type="button" class="btn me-sm-4 me-md-2 me-xl-4 px-1 align-items-center d-flex py-0"
                            @click="openEmojiSidebar">
                            <i class="bi bi-emoji-wink px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Emoji</span>
                        </button>
                        <button type="button" class="btn align-items-center d-flex py-0 px-1" @click="fileInput?.click()">
                            <i class="bi bi-image px-2 my-0" style="font-size: 1.5rem" />
                            <span>Add Image</span>
                        </button>
                        <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" accept="image/*" />
                    </div>
                </template>
                <template #end>
                    <button v-if="showUploadAudio" type="button" class="btn btn-other rounded-4 me-3" data-bs-toggle="modal" data-bs-target="#audioModal">
                        <span v-if="audioUploaded" class="hide-when-small px-1">Change audio</span>
                        <span v-else class="hide-when-small px-1">Add audio</span>
                        <i class="bi bi-soundwave"></i>
                    </button>
                    <button type="button" class="btn btn-danger ps-3 rounded-4" data-bs-toggle="modal" data-bs-target="#doneModal" @click="() => hasUnsavedChanges = false">
                        Done!
                        <i class="bi bi-chevron-right"></i>
                    </button>
                </template>
            </NavigationBar>
        </header>

        <AudioModal @file-removed="removeFile" @file-uploaded="addFile"></AudioModal>

        <DoneModal @share-card="shareCard" 
            @close-share-modal="closeShareModal" 
            @download-images="downloadImages" 
            @download-p-d-f="downloadPDF"
            ref="done-modal"
        />
        <CardModal @card-selected="handleCardTypeSelected" ref="cardModal" />
        
        <div style="position:relative">
            <main class="main-container" ref="main-container" @drop="handleDrop" @dragover="handleDragOver">
                <div ref="frontCanvasContainer"></div>
                <div ref="insideCanvasContainer"></div>
                <div ref="backCanvasContainer"></div>
            </main>
            <SideBar ref="sidebar">
                <div ref="sidebarSlot"></div>
            </SideBar>
        </div>
        <footer>
            <div class="btn-group" role="group" ref="footer-buttons">
                <button @click="switchPage('front')" :class="{ active: currentPage === 'front' }">
                    <div style="transform: scale(1.5, 2.5)"><i class="bi bi-wallet2 px-2 my-0" /></div>
                </button>
                <button @click="switchPage('inside')" :class="{ active: currentPage === 'inside' }" ref="inside-button">
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
import { createVNode, h, nextTick, onMounted, ref, render, useTemplateRef, type VNode } from 'vue';
import NavigationBar from '@/components/NavigationBar.vue';
import SideBar from '@/components/SideBar.vue';
import ShapeOptions from '@/components/ShapeOptions.vue';
import ShapeCreate from '@/components/ShapeCreate.vue';
import EmojiCreate from '@/components/EmojiCreate.vue';
import Canvas from '@/components/Canvas.vue';
import DoneModal from '@/components/DoneModal.vue';
import CardModal from '@/components/CardModal.vue';
import AudioModal from '@/components/AudioModal.vue';
import Konva from 'konva';
import type { Vector2d } from 'konva/lib/types';
import jsPDF from 'jspdf';
import axios from 'axios';
import { CardType } from '@/scripts/Constants';

import { useHead } from '@vueuse/head'

useHead({
    title: 'Cardigan: Create & Share Personalized Greeting Cards',
    meta: [
        { name: 'description', content: 'Design unique digital greeting cards for any occasion. Easily customize with photos, messages, and more. Share the joy with friends and family!' },
        { property: 'og:title', content: 'Cardigan: Create & Share Personalized Greeting Cards' },
        { property: 'og:description', content: 'Design unique digital greeting cards for any occasion. Easily customize with photos, messages, and more. Share the joy with friends and family!' },
        { property: 'og:image', content: 'https://www.cardigan.publicvm.com/cardigan.png' },
        { property: 'og:url', content: 'https://www.cardigan.publicvm.com' }
    ]
})

const handleDrop = (event: DragEvent) => {
  event.preventDefault();

  const files = event.dataTransfer?.files;
  if (files && files.length > 0) {
    const file = files[0];

    if (file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                addImage(img);
            };
            img.onerror = () => {
                console.error('Error loading image');
            };
            img.src = e.target?.result as string;
        };
        reader.onerror = () => {
            console.error('Error reading file');
        };
        reader.readAsDataURL(file);
    }
  }
};
const handleDragOver = (event: DragEvent) => {
    event.preventDefault(); // Necessary to allow drop
};

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
        onShapeSelected: currentCanvas!.addNode
    };

    if (sidebarSlot.value) {
        render(shapeCreateVNode, sidebarSlot.value);
    } else console.error("sidebar slot is not there");

    sidebar.value?.forceExpandSidebar()
}

function openEmojiSidebar() {
    const emojiCreateVNode = createVNode(EmojiCreate);

    emojiCreateVNode.props = {
        onEmojiSelected: (node: Konva.Shape) => currentCanvas!.addNode(node, false)
    };

    if (sidebarSlot.value) {
        render(emojiCreateVNode, sidebarSlot.value);
    } else console.error("sidebar slot is not there");
    
    sidebar.value?.forceExpandSidebar();
}

function closeSidebar() {
    if (sidebarSlot.value) {
        render(null, sidebarSlot.value);
    }
    sidebar.value?.retractSidebar();
}

function deleteSelected() {
    currentCanvas?.deleteSelected();
}

function addText() {
    var text = new Konva.Text({
        text: 'Sample Text',
        fontSize: 30,
        fontFamily: 'Calibri',
        fill: '#000000',
        name: "Text",
    });
    currentCanvas?.addNode(text);
}

function addImage(img: HTMLImageElement) {
    currentCanvas?.addImage(img);
}

function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
        const file = input.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                addImage(img);
                if (input) input.value = '';
            };
            img.onerror = () => {
                console.error('Error loading image');
                if (input) input.value = '';
            };
            img.src = e.target?.result as string;
        };
        reader.onerror = () => {
            console.error('Error reading file');
            if (input) input.value = '';
        };
        reader.readAsDataURL(file);
    }
}

function switchPage(page: string) {
    currentCanvas?.deselectThisCanvas();
    
    currentPage.value = page;
    currentCanvas = canvasMap.get(page)!;
    currentCanvas?.selectThisCanvas();

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

    currentCanvas?.fitStageIntoParentContainer(scale);
}
async function shareCard() {
    waitingForResult = true;
    
    const formData = new FormData();
    const blobPromises = Array.from(canvasMap.entries()).map(async ([page, canvas]) => {
        const blob = await canvas.toBlob() as Blob;
        return { page, blob }; 
    });
    const blobs = await Promise.all(blobPromises); 
    blobs.forEach(({ page, blob }) => { 
        if (blob) formData.append(page, blob, `${page}.png`);
    });
    if (audioFile) {
        formData.append('audio', audioFile);
    }
    try {
        const result = await axios.post(`/api/card`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        
        if (!waitingForResult) return;
        if (result.data.error != undefined)
            doneModal.value?.updateResults(`Error: ${result.data.error}`);
        else
            doneModal.value?.updateResults(`${window.location.origin}/card/${result.data.id}`);
    } catch (error: any) {
        if (!waitingForResult) return;
        doneModal.value?.updateResults(`Error: ${error.message}`);
    } finally {
        waitingForResult = false;
    }
}
function downloadImages() {
    canvasMap.forEach((canvas, page) => {
        const dataURL = canvas.toImage();
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
        orientation: 'portrait',
        unit: 'pt',
        format: [1414, 2000]
    });

    const frontImg = canvasMap.get('front')!.toImage();
    const frontCanvas = canvasMap.get('front')!;
    frontCanvas!.stage().find('Text').forEach((text) => {
        var kText = text as Konva.Text;
        const size = kText.fontSize() * kText.scaleX() * 0.9;
        pdf.setFontSize(size);
        pdf.text(kText.text(), kText.x(), kText.y(), {
            baseline: 'top',
            angle: -kText.getAbsoluteRotation(),
        });
    });
    pdf.addImage(frontImg, 'PNG', 0, 0, 707, 1000);
    
    if (cardType == CardType.OneSided){ 
        pdf.save('greeting_card.pdf');
        return;
    }
    
    const backImg = canvasMap.get('back')!.toImage();
    const backCanvas = canvasMap.get('back')!;
    backCanvas.stage().find('Text').forEach((text) => {
        var kText = text as Konva.Text;
        const size = kText.fontSize() * kText.scaleX() * 0.9;
        pdf.setFontSize(size);
        pdf.text(kText.text(), kText.x() + 707, kText.y(), {
            baseline: 'top',
            angle: -kText.getAbsoluteRotation(),
        });
    });
    pdf.addImage(backImg, 'PNG', 707, 0, 707, 1000);

    if (cardType == CardType.TwoSided){ 
        pdf.save('greeting_card.pdf');
        return;
    }

    // Second page: Inside
    const insideImg = canvasMap.get('inside')!.toImage();
    const insideCanvas = canvasMap.get('inside')!;
    insideCanvas.stage().find('Text').forEach((text) => {
        var kText = text as Konva.Text;
        const size = kText.fontSize() * kText.scaleX() * 0.9;
        pdf.setFontSize(size);
        pdf.text(kText.text(), kText.x(), kText.y()+1000, {
            baseline: 'top',
            angle: -kText.getAbsoluteRotation(),
        });
    });

    pdf.addImage(insideImg, 'PNG', 0, 1000, 1414, 1000);

    pdf.save('greeting_card.pdf');
}
function updatePastePoint(x: number, y: number){
    pastePoint = {x: x, y: y}
}
function closeShareModal() {
    waitingForResult = false;
}
function handleCardTypeSelected(type: CardType) {
    cardType = type;
    // Decide which footer buttons to show
    if (cardType == CardType.OneSided){
        footerButtonGroup.value!.style.display = "none";
        showUploadAudio.value = false;
    } else if (cardType == CardType.TwoSided){
        footerInsideButton.value!.style.display = "none";
        showUploadAudio.value = false;
    }

    // init the necessary cards
    var frontCanvas = h(Canvas, {page: "front", onOpenOptions: openOptionsSidebar, onCloseOptions: closeSidebar, onUpdatePastePoint: updatePastePoint, onChangesHappened: () => hasUnsavedChanges = true});
    if (frontCanvasContainer.value) render(frontCanvas, frontCanvasContainer.value);
    vNodeMap.set("front", frontCanvas);
    
    if (cardType == CardType.Openable){
        var insideCanvas = h(Canvas, {page: "inside", onOpenOptions: openOptionsSidebar, onCloseOptions: closeSidebar, onUpdatePastePoint: updatePastePoint, onChangesHappened: () => hasUnsavedChanges = true});
        if (insideCanvasContainer.value) render(insideCanvas, insideCanvasContainer.value);
        vNodeMap.set("inside", insideCanvas);
    }
    if (cardType == CardType.Openable || cardType == CardType.TwoSided){
        var backCanvas = h(Canvas, {page: "back", onOpenOptions: openOptionsSidebar, onCloseOptions: closeSidebar, onUpdatePastePoint: updatePastePoint, onChangesHappened: () => hasUnsavedChanges = true});
        if (backCanvasContainer.value) render(backCanvas, backCanvasContainer.value);
        vNodeMap.set("back", backCanvas);
    }

    nextTick(()=>{
        vNodeMap.forEach((node,key) => {
            canvasMap.set(key, node.component?.exposed as InstanceType<typeof Canvas>);
        });
        currentCanvas = canvasMap.get("front")!;
        currentCanvas.selectThisCanvas();
        fitStageIntoParentContainer();
        
        window.addEventListener('resize', fitStageIntoParentContainer);
        window.addEventListener('keydown', (event) => {
            const activeElement = document.activeElement;
            if (activeElement?.tagName === 'TEXTAREA' || activeElement?.tagName === 'INPUT') return;
            if (event.key === 'Delete') {
                deleteSelected();
            } else if ((event.key === 'c' || event.key === 'C') && event.ctrlKey) {
                var copyResult = currentCanvas?.copy();
                if (!copyResult) return;
                copiedShapes = copyResult.copiedShapes;
                pastePoint = copyResult.pastePoint;
            } else if ((event.key === 'v' || event.key === 'V') && event.ctrlKey) {
                var pasteResult = currentCanvas?.paste(copiedShapes,pastePoint);
                if (!pasteResult) return;
                copiedShapes = pasteResult.copiedShapes;
                pastePoint = pasteResult.pastePoint;
            }
        });
        mainContainer.value?.addEventListener('click', (e) => {
            if (e.target !== mainContainer.value) return;
            currentCanvas?.deselect();
        })
    })
}
function removeFile(){
    audioFile = null;
    audioUploaded.value = false;
}
function addFile(file: File){
    audioFile = file;
    audioUploaded.value = true;
}

const pageSizes: { [key: string]: { width: number; height: number } } = {
    "front": { width: 1414 / 2, height: 1000 },
    "inside": { width: 1414, height: 1000 },
    "back": { width: 1414 / 2, height: 1000 },
}

const currentPage = ref("front");
var currentCanvas: InstanceType<typeof Canvas> | null = null;
const canvasMap = new Map<string, InstanceType<typeof Canvas>>();
const vNodeMap = new Map<string, VNode>()
const fileInput = useTemplateRef("fileInput");
const sidebar = useTemplateRef("sidebar");
const sidebarSlot = useTemplateRef("sidebarSlot");
const mainContainer = useTemplateRef("main-container");
const doneModal = useTemplateRef("done-modal");
var copiedShapes: Konva.Node[] = [];
var pastePoint: Vector2d;

const frontCanvasContainer = useTemplateRef("frontCanvasContainer");
const insideCanvasContainer = useTemplateRef("insideCanvasContainer");
const backCanvasContainer = useTemplateRef("backCanvasContainer");
const footerInsideButton = useTemplateRef("inside-button");
const footerButtonGroup = useTemplateRef("footer-buttons")
const showUploadAudio = ref(true);

var waitingForResult = false;
var cardType: CardType;
var hasUnsavedChanges = false;
var audioFile: File | null = null;
const audioUploaded = ref(false);

onMounted(() => {
    window.addEventListener('beforeunload', function (e) {
    if (hasUnsavedChanges) {
        e.preventDefault();
        e.returnValue = '';
        return '';
    }
    });
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

.btn-other {
    background-color: #eeeeee;
}

.hide-when-small {
    display: none;
}
@media (min-width: 450px) {
    .hide-when-small {
        display: unset;
    }
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