import json
import os
import aiogram
from aiogram import types


PHOTOS_DIR = "images"


async def download_photo(
    message: types.Message, location: int, checklist_order: int
) -> str:
    try:
        photo = message.photo[-1]
        os.makedirs(PHOTOS_DIR, exist_ok=True)
        file_id = photo.file_id
        file_name = f"{file_id}.jpg"
        file_path = os.path.join(PHOTOS_DIR, file_name)
        await photo.download(destination_file=file_path)

        await save_photo_url(
            file_path=file_path,
            user_id=str(message.from_user.id),
            location=location,
            checklist_order=checklist_order,
        )
        return file_path
    except FileNotFoundError:
        print("Error: Unable to create directory for saving the photo.")
    except aiogram.utils.exceptions.TelegramAPIError as e:
        print(f"Telegram API Error: {e}")


async def save_photo_url(
    file_path: str, user_id: str, location: str, checklist_order: str
):
    data = await load_data()
    if user_id not in data:
        data[user_id] = {}
    if location not in data[user_id]:
        data[user_id][location] = {}
    data[user_id][location][checklist_order] = file_path
    await save_data(data)


async def load_data() -> dict:
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = {}
    except FileNotFoundError:
        with open("data.json", "w") as file:
            pass
        data = {}
    return data


async def save_data(data: dict):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
