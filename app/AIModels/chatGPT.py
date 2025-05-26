import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.models.image import QuestionImage
from app.prompt.prompts import HAND_PROMPT_3

load_dotenv()
API_KEY = os.getenv("OPEN_AI_KEY")

client = OpenAI(api_key=API_KEY)


def send_to_chatgpt(image: QuestionImage, question):
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    # Path to your image
    image_path = image.uri

    # Getting the Base64 string
    base64_image = encode_image(image_path)

    # response = client.responses.create(
    #     model="gpt-4.1",
    #     input="Write a one-sentence bedtime story about a unicorn.",
    # )
    response = client.responses.create(
        model="gpt-4.1",
        instructions=HAND_PROMPT_3,
        input=str(
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "what's in this image?"},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ]
        ),
    )

    print(response.output_text)
