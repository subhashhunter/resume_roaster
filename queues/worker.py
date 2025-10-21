from db.collections.files import files_collection
from bson import ObjectId
from pdf2image import convert_from_path
import os

from google import genai
from google.genai import types


client = genai.Client()


async def process_file(id: str, file_path: str):
    
    await files_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": "processing"}})
    print("processing")

    
    await files_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": "converting to images"}})
    print("converting to image")

    
    pages = convert_from_path(file_path)
    images = []

    for i, page in enumerate(pages):
        image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        page.save(image_save_path, 'JPEG')
        images.append(image_save_path)

    await files_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": "converting to images success"}})
    print("success")

    
    image_parts = []
    for img_path in images:
        with open(img_path, "rb") as f:
            image_bytes = f.read()
        image_parts.append(types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"))

    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            "Roast this resume?",
            image_parts[0]  
        ]
    )

    print("AI response:", response.text)
    await files_collection.update_one({"_id":ObjectId(id)},{
        "$set":{
            "status":"done",
            "result":response.text
        }
    })

# flake8:noqa

