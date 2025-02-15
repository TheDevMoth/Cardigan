import Konva from "konva";

const GUIDELINE_OFFSET = 5;

export function getLineGuideStops(skipShapes: Konva.Shape[], stage: Konva.Stage, layer: Konva.Layer, isInside: boolean) {
    // snap to stage
    var vertical = [0, stage.width() / 2, stage.width()];
    var horizontal = [0, stage.height() / 2, stage.height()];

    if (isInside) vertical.push(stage.width() / 4, stage.width() * 3 / 4);

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
export function getObjectSnappingEdges(nodes: Konva.Shape[], absNode: Konva.Shape) {
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
export function getGuides(lineGuideStops: ReturnType<typeof getLineGuideStops>, itemBounds: ReturnType<typeof getObjectSnappingEdges>) {
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
export function drawGuides(guides: ReturnType<typeof getGuides>, layer: Konva.Layer) {
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