<template>
    <header>
        <NavigationBar>
            <template #middle>
                <div class="btn-group" role="group">                    
                    <button type="button" class="btn me-3 align-items-center d-flex py-0" @click="addText">
                        <i class="bi bi-textarea-t px-2 my-0" style="font-size: 1.5rem"/>
                        <span>Add Text</span>
                    </button>
                    <button type="button" class="btn me-3 align-items-center d-flex py-0" @click="openShapesSidebar">
                        <i class="bi bi-plus-square-dotted px-2 my-0" style="font-size: 1.5rem"/>
                        <span>Add Shape</span>
                    </button>
                    <!-- <button type="button" class="btn me-3 align-items-center d-flex py-0" @click="openStickerSidebar">
                        <i class="bi bi-sticky px-2 my-0" style="font-size: 1.5rem"/>
                        <span>Add Sticker</span>
                    </button> -->
                    <button type="button" class="btn align-items-center d-flex py-0" @click="fileInput?.click()">
                        <i class="bi bi-image px-2 my-0" style="font-size: 1.5rem"/>
                        <span>Add Image</span>
                    </button>
                    <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" accept="image/*" />
                </div>
            </template>
            <template #end>
                ho
            </template>
        </NavigationBar>
    </header>

    <div style="position:relative">
        <main class="main-container" ref="main-container">
            <div id="canvas-container" ref="canvas-container"></div>
        </main>
        <SideBar ref="sidebar">
            <div ref="sidebarSlot"></div>
        </SideBar>
    </div>
</template>

<script setup lang="ts">
import { createVNode, onMounted, ref, render, useTemplateRef } from 'vue';
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
                // Clear the input value to allow the same file to be selected again
                if (input) input.value = '';
            };
            img.onerror = function() {
                console.error('Error loading image');
                if (input) input.value = '';
            };
            img.src = e.target?.result as string;
        };
        reader.onerror = function() {
            console.error('Error reading file');
            if (input) input.value = '';
        };
        reader.readAsDataURL(file);
    }
}
function addImage(img: HTMLImageElement) {
    const landscape = img.width > img.height;
    const maxWidth = Math.min(img.width, stage.width());
    const maxHeight = Math.min(img.height, stage.height());
    const scaleX = maxWidth / img.width;
    const scaleY = maxHeight / img.height;
    const scale = Math.min(scaleX, scaleY);

    const imageNode = new Konva.Image({
        image: img,
        width: img.width * scale,
        height: img.height * scale,
    });
    
    var newScale = 1;
    if (imageNode.width() > stage.width()/2 && landscape) {
        newScale = (stage.width()/2)/imageNode.width();
    } else if (imageNode.height() > stage.height()/2 && !landscape) {
        newScale = (stage.height()/2)/imageNode.height();
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
    node.x(stage.width() / 2);
    node.y(stage.height() / 2);
    node.on('mouseover', function () {
        document.body.style.cursor = 'pointer';
    });
    node.on('mouseout', function () {
        document.body.style.cursor = 'default';
    });
    node.on('dragmove', () => {
        node.x(clamp(node.x(), 0, stage.width()));
        node.y(clamp(node.y(), 0, stage.height()));
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
// function openStickerSidebar() {
//     // Todo
//     // const shapeCreateVNode = createVNode(ShapeCreate);

//     // shapeCreateVNode.props = {
//     //     onShapeSelected: addNode
//     // };

//     // if (sidebarSlot.value) {
//     //     render(shapeCreateVNode, sidebarSlot.value);
//     // } else console.error("sidebar slot is not there");

//     // sidebar.value?.expandSidebar()
// }

const fileInput = useTemplateRef("fileInput");
const canvasContainer = useTemplateRef("canvas-container");
const sidebar = useTemplateRef("sidebar");
const sidebarSlot = useTemplateRef("sidebarSlot");
const mainContainer = useTemplateRef("main-container");
var tr: Konva.Transformer;
var stage: Konva.Stage;
var layer: Konva.Layer;

onMounted(() => {
    var sceneWidth = 1018;
    var sceneHeight = 720;
    stage = new Konva.Stage({
        container: 'canvas-container',
        width: Math.min(sceneWidth),
        height: Math.min(sceneWidth)
    });
    const bgLayer = new Konva.Layer();
    bgLayer.add(new Konva.Rect({
        fill: '#FFFFFF',
        x: 0,
        y: 0,
        width: sceneWidth,
        height: sceneHeight
    }))
    stage.add(bgLayer);
    layer = new Konva.Layer();
    stage.add(layer);

    tr = new Konva.Transformer();
    tr.flipEnabled(true);
    tr.rotationSnaps([0, 45, 90, 135, 180, 225, 270, 315]);
    tr.rotationSnapTolerance(3);

    layer.add(tr);

    // selection handling 
    stage.on('click tap', function (e) {
        // Remove all selections
        if (e.target === stage || e.target.getLayer() === bgLayer) {
            tr.nodes().forEach(element => {
                element.setDraggable(false);
            });
            closeSidebar();
            tr.nodes([]);
            tr.resizeEnabled(true);
            return;
        }
        if (e.target.getLayer() !== layer) {
            return;
        }
        // Select or unselect elements
        const metaPressed = e.evt.ctrlKey || e.evt.metaKey;
        const isSelected = tr.nodes().indexOf(e.target) >= 0;

        if (!metaPressed && !isSelected) {
            openOptionsSidebar(e.target);
            e.target.setDraggable(true);
            tr.nodes().forEach(element => {
                element.setDraggable(false);
            });
            tr.nodes([e.target]);
            tr.resizeEnabled(!(e.target instanceof Konva.Text));
            
        } else if (metaPressed && isSelected) {
            const nodes = tr.nodes().slice();
            nodes.splice(nodes.indexOf(e.target), 1);
            if (nodes.length == 0) closeSidebar();
            e.target.setDraggable(false);
            tr.nodes(nodes);
            tr.resizeEnabled(!nodes.some(node => node instanceof Konva.Text));
        } else if (metaPressed && !isSelected) {
            e.target.setDraggable(true);
            const nodes = tr.nodes().concat([e.target]);
            if (nodes.length == 1) openOptionsSidebar(e.target);
            else closeSidebar();
            tr.nodes(nodes);
            if (e.target instanceof Konva.Text) tr.resizeEnabled(false);
        }
    });

    function fitStageIntoParentContainer() {
        if (!mainContainer.value) return;
        var container = mainContainer.value;

        var containerWidth = container.offsetWidth;
        var containerHeight = container.offsetHeight;

        var scaleX = containerWidth / sceneWidth;
        var scaleY = containerHeight / sceneHeight;
        
        var scale = Math.min(scaleX, scaleY, 1);
        
        stage.width(sceneWidth * scale);
        stage.height(sceneHeight * scale);
        stage.scale({ x: scale, y: scale });
    }

      fitStageIntoParentContainer();
      window.addEventListener('resize', fitStageIntoParentContainer);

    layer.draw();
    tr.setZIndex(layer.children.length - 1);
});
</script>

<style scoped>
.main-container {
    background-color: #F5F3F4;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh; 
    padding: 20px; 
}

#canvas-container {
    margin: 0px;
    padding: 0px;
    overflow: hidden;
}
</style>