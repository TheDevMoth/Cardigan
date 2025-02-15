
import logging
import os
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from nanoid import generate
from PIL import Image
from io import BytesIO

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from pydantic import BaseModel, Field

# Cosmos DB Configuration
from azure.cosmosdb.table import TableService

the_connection_string = os.environ["COSMOS_CONNECTION_STRING"]
table = TableService(endpoint_suffix = "table.cosmos.azure.com", connection_string= the_connection_string)

COSMOS_CONTAINER_NAME = "cardtable"
ACCOUNT_URL = "https://cardiganstorage.blob.core.windows.net"
BLOB_STORAGE = "card-storage"

credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(ACCOUNT_URL, credential=credential)
card_storage = blob_service_client.get_container_client(container=BLOB_STORAGE) 


class Card(BaseModel):
    PartitionKey: str = Field(default="card")
    RowKey: str = Field()
    front: bool = Field(default=None)
    front_inside: bool = Field(default=None)
    back_inside: bool = Field(default=None)
    back: bool = Field(default=None)
    audio: str = Field(default=None)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/card")
async def upload_card(
    front: UploadFile = UploadFile(...),
    inside: UploadFile = UploadFile(...),
    back: UploadFile = UploadFile(...),
    audio: UploadFile = UploadFile(...)
):
    # Input validation
    for file in [front, inside, back]:
        if file.content_type not in ["image/jpeg", "image/png"]:
            return {"error": f"File {file.filename} is not a valid image."}

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

    id = generate(size=12)
    card = Card(
        RowKey=id,
        front=True,
        front_inside=True,
        back_inside=True,
        back=True
    )

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

    card_storage.upload_blob(name=f"{id}_front.png", data=front_bytes)
    card_storage.upload_blob(name=f"{id}_front_inside.png", data=front_inside_bytes)
    card_storage.upload_blob(name=f"{id}_back_inside.png", data=back_inside_bytes)
    card_storage.upload_blob(name=f"{id}_back.png", data=back_bytes)

    if audio.filename is not None:
        if audio.content_type in ["audio/mpeg", "audio/wav"]:
            card.audio = audio.filename.split('.')[-1]
            audio_bytes = BytesIO(await audio.read())
            audio_bytes.seek(0)
            card_storage.upload_blob(name=f"{id}_audio.{card.audio}", data=audio_bytes)
        else:
            return {"error": f"File {audio.filename} is not a valid audio file."}
    print(card)
    table.insert_entity(COSMOS_CONTAINER_NAME, card.model_dump())

    return {"id": id}

@app.get("/card/{card_id}")
async def read_card(card_id: str):
    try:
        card = table.get_entity(COSMOS_CONTAINER_NAME,"card",card_id)
    except Exception as e:
        logging.error(f"Error reading card: {e}")
        return {"error": "Card not found."}

    images = {
        "front": f"{card_storage.url}/{card.RowKey}_front.png",
        "front_inside": f"{card_storage.url}/{card.RowKey}_front_inside.png",
        "back_inside": f"{card_storage.url}/{card.RowKey}_back_inside.png",
        "back": f"{card_storage.url}/{card.RowKey}_back.png",
        "audio": f"{card_storage.url}/{card.RowKey}_audio.{card.audio}" if "audio" in card else None
    }

    return images
