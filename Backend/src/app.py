import logging
import os
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from nanoid import generate
from PIL import Image
from io import BytesIO
from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from pydantic import BaseModel, Field

# Cosmos DB Configuration
from azure.cosmosdb.table import TableService

CONNECTION_STRING = os.environ["COSMOS_CONNECTION_STRING"]
COSMOS_CONTAINER_NAME = "cardtable"
ACCOUNT_URL = "https://cardiganstorage.blob.core.windows.net"
BLOB_STORAGE = "card-storage"

table = TableService(endpoint_suffix = "table.cosmos.azure.com", connection_string=CONNECTION_STRING)
credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(ACCOUNT_URL, credential=credential)
card_storage = blob_service_client.get_container_client(container=BLOB_STORAGE) 


class Card(BaseModel):
    PartitionKey: str = Field(default="card")
    RowKey: str = Field()
    front: bool = Field(default=False)
    front_inside: bool = Field(default=False)
    back_inside: bool = Field(default=False)
    back: bool = Field(default=False)
    audio: str = Field(default="")

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
    inside: Optional[UploadFile] = None,
    back: Optional[UploadFile] = None,
    audio: Optional[UploadFile] = None
):
    # Input validation
    if front.content_type not in ["image/jpeg", "image/png"]:
        return {"error": f"File {front.filename} is not a valid image."}
    if inside and inside.content_type not in ["image/jpeg", "image/png"]:
        return {"error": f"File {inside.filename} is not a valid image."}
    if back and back.content_type not in ["image/jpeg", "image/png"]:
        return {"error": f"File {back.filename} is not a valid image."}
    if inside and not back:
        return {"error": "Back image must be provided if inside image is provided."}
    if not inside and audio:
        return {"error": "Audio file cannot be provided without inside image."}

    # Read the original image bytes
    front_bytes = BytesIO(await front.read())
    front_img = Image.open(front_bytes)
    if front_img.size != (707, 1000):
        return {"error": "Front image does not have required dimensions (707x1000)"}

    id = generate(size=12)
    card = Card(
        RowKey=id,
        front=True,
        front_inside=bool(inside),
        back_inside=bool(inside),
        back=bool(back)
    )

    # Process inside image (split in half) if provided
    if inside:
        inside_bytes = BytesIO(await inside.read())
        inside_img = Image.open(inside_bytes)
        if inside_img.size != (1414, 1000):
            return {"error": "Inside image does not have required dimensions (1414x1000)"}
        front_inside = inside_img.crop((0, 0, 707, 1000))
        back_inside = inside_img.crop((707, 0, 1414, 1000))
        front_inside_bytes = BytesIO()
        front_inside.save(front_inside_bytes, format="PNG")
        front_inside_bytes.seek(0)
        back_inside_bytes = BytesIO()
        back_inside.save(back_inside_bytes, format="PNG")
        back_inside_bytes.seek(0)
        card_storage.upload_blob(name=f"{id}_front_inside.png", data=front_inside_bytes)
        card_storage.upload_blob(name=f"{id}_back_inside.png", data=back_inside_bytes)

    # Process back image if provided
    if back:
        back_bytes = BytesIO(await back.read())
        back_img = Image.open(back_bytes)
        if back_img.size != (707, 1000):
            return {"error": "Back image does not have required dimensions (707x1000)"}
        back_bytes.seek(0)
        card_storage.upload_blob(name=f"{id}_back.png", data=back_bytes)

    # Upload front image
    front_bytes.seek(0)
    card_storage.upload_blob(name=f"{id}_front.png", data=front_bytes)

    # Process audio file if provided
    if audio:
        if audio.content_type in ["audio/mpeg", "audio/wav"]:
            card.audio = audio.filename.split('.')[-1]
            audio_bytes = BytesIO(await audio.read())
            audio_bytes.seek(0)
            card_storage.upload_blob(name=f"{id}_audio.{card.audio}", data=audio_bytes)
        else:
            return {"error": f"File {audio.filename} is not a valid audio file."}

    table.insert_entity(COSMOS_CONTAINER_NAME, card.model_dump())

    return {"id": id}

@app.get("/card/{card_id}")
async def read_card(card_id: str):
    try:
        card = table.get_entity(COSMOS_CONTAINER_NAME, "card", card_id)
    except Exception as e:
        logging.error(f"Error reading card: {e}")
        return {"error": "Card not found."}

    images = {
        "front": f"{card_storage.url}/{card.RowKey}_front.png",
        "front_inside": f"{card_storage.url}/{card.RowKey}_front_inside.png" if card.front_inside else None,
        "back_inside": f"{card_storage.url}/{card.RowKey}_back_inside.png" if card.back_inside else None,
        "back": f"{card_storage.url}/{card.RowKey}_back.png" if card.back else None,
        "audio": f"{card_storage.url}/{card.RowKey}_audio.{card.audio}" if card.audio else None
    }

    return images
