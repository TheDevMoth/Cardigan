from uuid import uuid4, UUID
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from database import Card, SessionDep, create_db_and_tables
from sqlmodel import select
from PIL import Image
from io import BytesIO

app = FastAPI()

create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/card")
async def upload_card(
    session: SessionDep,
    front: UploadFile = UploadFile(...),
    inside: UploadFile = UploadFile(...),
    back: UploadFile = UploadFile(...),
):
    # Input validation
    for file in [front, inside, back]:
        if file.content_type not in ["image/jpeg", "image/png"]:
            return {"error": f"File {file.filename} is not a valid image."}

    id = uuid4()
    card = Card(
        id=id,
        front=f"{id}_front",
        front_inside=f"{id}_front_inside",
        back_inside=f"{id}_back_inside",
        back=f"{id}_back",
    )

    # Process front and back images
    front_img = Image.open(BytesIO(await front.read()))
    back_img = Image.open(BytesIO(await back.read()))

    if front_img.size != (707, 1000) or back_img.size != (707, 1000):
        return {"error": "Front or back image does not have required dimensions (707x1000)"}

    # Process inside image (split in half)
    inside_img = Image.open(BytesIO(await inside.read()))
    if inside_img.size != (1414, 1000):
        return {"error": "Inside image does not have required dimensions (1414x1000)"}

    # Split inside image into left and right halves
    front_inside = inside_img.crop((0, 0, 707, 1000))
    back_inside = inside_img.crop((707, 0, 1414, 1000))

    # Save all images
    front_img.save(f"../Frontend/Egreet/public/{card.front}.png", "PNG")
    front_inside.save(f"../Frontend/Egreet/public/{card.front_inside}.png", "PNG")
    back_inside.save(f"../Frontend/Egreet/public/{card.back_inside}.png", "PNG")
    back_img.save(f"../Frontend/Egreet/public/{card.back}.png", "PNG")

    session.add(card)
    session.commit()
    return {"id": card.id}

@app.get("/card/{card_id}")
async def read_card(card_id: str, session: SessionDep):
    statement = select(Card).where(Card.id == UUID(card_id))
    card = session.exec(statement).first()
    if not card:
        return {"error": "Card not found."}

    images = {
        "front": f"{card.front}.png",
        "front_inside": f"{card.front_inside}.png",
        "back_inside": f"{card.back_inside}.png",
        "back": f"{card.back}.png",
    }

    return images
