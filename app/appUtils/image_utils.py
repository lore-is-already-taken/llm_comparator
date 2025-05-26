import hashlib
from pathlib import Path

from fastapi import UploadFile

from app.models.image import QuestionImage


async def process_image(image: UploadFile) -> QuestionImage:
    content = await image.read()
    size = len(content)
    image_hash = hashlib.sha256(content).hexdigest()
    filename = image.filename
    content_type = image.content_type

    adapter = {
        "size": size,
        "hash": image_hash,
        "name": filename,
        "content_type": content_type,
        "uri": "",
    }
    final_image = QuestionImage(**adapter)
    return final_image


async def check_image(image, final_image) -> str:
    # Save image locally
    # Create directory if it doesn't exist
    save_dir = Path("./saved_images")
    save_dir.mkdir(exist_ok=True)

    # Create filename using hash and original extension
    file_extension = Path(image.filename).suffix if image.filename else ""
    filename = f"{final_image.hash}{file_extension}"
    file_path = save_dir / filename

    # Check if the file already exists
    if file_path.exists():
        print(f"File already exists: {file_path}")
        route = str(file_path.resolve()).split("/")
        fileroute = f"./{route[-2]}/{route[-1]}"
        return fileroute

    # If file doesn't exist, save it
    # Reset file pointer to beginning
    await image.seek(0)

    # Save the file
    with open(file_path, "wb") as f:
        content = await image.read()
        f.write(content)

    route = str(file_path.resolve()).split("/")
    fileroute = f"./{route[-2]}/{route[-1]}"
    return fileroute
