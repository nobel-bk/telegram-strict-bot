from pyrogram import Client, filters
import json, os, hashlib, asyncio
from flask import Flask
from threading import Thread

FILE_NAME = "media_map.json"
media_map = {}

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        media_map = json.load(f)

API_ID = 28488147
API_HASH = "a6a1451f063db8d579791a51b7270dff"
BOT_TOKEN = "7950704145:AAG9mn2aeFsuUibEIUPfX2LahVHA7EtTYvs"

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def save_data():
    with open(FILE_NAME, "w") as f:
        json.dump(media_map, f)

def get_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

@app.on_message(filters.group & (filters.photo | filters.video | filters.document))
def media_handler(client, message):
    try:
        file_path = app.download_media(message)
        file_hash = get_hash(file_path)
        sender = str(message.from_user.id)
        os.remove(file_path)

        if file_hash in media_map:
            if media_map[file_hash] != sender:
                message.delete()
        else:
            media_map[file_hash] = sender
            save_data()
    except Exception as e:
        print("Error:", e)

# Flask app to keep service alive
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot is live"

def run_web():
    flask_app.run(host='0.0.0.0', port=8080)

# Start web server
Thread(target=run_web).start()

# Start Telegram bot normally
if __name__ == "__main__":
    print("✅ Strict Media Bot is running...")
    app.run()
