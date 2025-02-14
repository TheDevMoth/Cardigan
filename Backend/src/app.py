import asyncio
from uuid import uuid4, UUID
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from nanoid import generate
from database import Card, SessionDep, create_db_and_tables
from sqlmodel import select
from PIL import Image
from io import BytesIO

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient

account_url = "https://cardiganstorage.blob.core.windows.net"
blob_service_client: BlobServiceClient = None
card_storage: ContainerClient  = None

def init_blob_service_client():
    """Ensure the BlobServiceClient is initialized and reused."""
    global blob_service_client, card_storage
    if blob_service_client is None:
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(account_url, credential=credential)
        card_storage = blob_service_client.get_container_client(container="card-storage")
        
app = FastAPI()

init_blob_service_client()
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

    id = generate(size=12)
    card = Card(
        id=id,
        front=f"{id}_front",
        front_inside=f"{id}_front_inside",
        back_inside=f"{id}_back_inside",
        back=f"{id}_back",
    )

    # Read the original image bytes
    front_bytes = BytesIO(await front.read())
    back_bytes = BytesIO(await back.read())
    inside_bytes = BytesIO(await inside.read())

    # Process front and back images
    front_img = Image.open(front_bytes)
    back_img = Image.open(back_bytes)

    if front_img.size != (707, 1000) or back_img.size != (707, 1000):
        return {"error": "Front or back image does not have required dimensions (707x1000)"}

    # Process inside image (split in half)
    inside_img = Image.open(inside_bytes)
    if inside_img.size != (1414, 1000):
        return {"error": "Inside image does not have required dimensions (1414x1000)"}

    # Split inside image into left and right halves
    front_inside = inside_img.crop((0, 0, 707, 1000))
    back_inside = inside_img.crop((707, 0, 1414, 1000))

    # Prepare the upload tasks
    front_bytes.seek(0)
    front_inside_bytes = BytesIO()
    front_inside.save(front_inside_bytes, format="PNG")
    front_inside_bytes.seek(0)
    back_inside_bytes = BytesIO()
    back_inside.save(back_inside_bytes, format="PNG")
    back_inside_bytes.seek(0)
    back_bytes.seek(0)

    card_storage.upload_blob(name=f"{card.front}.png", data=front_bytes),
    card_storage.upload_blob(name=f"{card.front_inside}.png", data=front_inside_bytes),
    card_storage.upload_blob(name=f"{card.back_inside}.png", data=back_inside_bytes),
    card_storage.upload_blob(name=f"{card.back}.png", data=back_bytes),

    session.add(card)
    session.commit()
    return {"id": card.id}

@app.get("/card/{card_id}")
async def read_card(card_id: str, session: SessionDep):
    statement = select(Card).where(Card.id == card_id)
    card = session.exec(statement).first()
    if not card:
        return {"error": "Card not found."}

    images = {
        "front": f"{card_storage.url}/{card.front}.png",
        "front_inside": f"{card_storage.url}/{card.front_inside}.png",
        "back_inside": f"{card_storage.url}/{card.back_inside}.png",
        "back": f"{card_storage.url}/{card.back}.png",
    }

    return images
