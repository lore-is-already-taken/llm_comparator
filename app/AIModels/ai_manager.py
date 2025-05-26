from app.AIModels.chatGPT import send_to_chatgpt
from app.models.image import QuestionImage


def send_prompt(image: QuestionImage, prompt):
    chat_gpt = send_to_chatgpt(image, prompt)
