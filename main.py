from pyrogram import Client, filters
import json
import os
import hashlib

FILE_NAME = "media_hashes.json"
seen_hashes = set()

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        seen_hashes = set(json.load(f))

API_ID = 28488147
API_HASH = "a6a1451f063db8d579791a51b7270dff"
BOT_TOKEN = "7950704145:AAG9mn2aeFsuUibEIUPfX2LahVHA7EtTYvs"

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def save_hashes():
    with open(FILE_NAME, "w") as f:
        json.dump(list(seen_hashes), f)


def get_file_hash(path):
    with open(path, "rb") as f:
        file_bytes = f.read()
        return hashlib.sha256(file_bytes).hexdigest()


@app.on_message(filters.group
                & (filters.photo | filters.video | filters.document))
def handle_media(client, message):
    try:
        file_path = app.download_media(message)
        file_hash = get_file_hash(file_path)
        os.remove(file_path)  # save space

        if file_hash in seen_hashes:
            message.delete()
        else:
            seen_hashes.add(file_hash)
            save_hashes()
    except Exception as e:
        print("Error processing file:", e)


print("✅ Bot with media hashing is running...")
app.run()
