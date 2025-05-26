import json
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile

from app.AIModels.ai_manager import send_prompt
from app.appUtils.image_utils import check_image, process_image
from app.db.mongo import MongoHandler

load_dotenv()


MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

app = FastAPI()
db_handler = MongoHandler(MONGO_USER, MONGO_PASSWORD)


@app.get("/")
def root():
    response = {"hola": "como estas"}
    return response


@app.post("/testmodels")
async def testmodels(image: UploadFile = File(...), text: str = Form(...)):
    processed_image = await process_image(image)

    image_exist = db_handler.check_if_exist(processed_image.hash)

    if not image_exist:
        filepath = await check_image(image, processed_image)
        processed_image.uri = str(filepath)
        result = db_handler.save_doc(processed_image)
        await image.seek(0)
        ai_responses = send_prompt(processed_image, text)
        return result
    else:
        filepath = await check_image(image, processed_image)
        processed_image.uri = str(filepath)
        print("asking for the image that already exist...")
        ai_responses = send_prompt(processed_image, text)
        return image_exist


if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
