from pyrogram import Client, filters
import json, os, hashlib

FILE_NAME = "media_hashes.json"
seen_hashes = set()

if os.path.exists(FILE_NAME):
    try:
        with open(FILE_NAME, "r") as f:
            seen_hashes = set(json.load(f))
    except Exception as e:
        print("❌ JSON Load Error:", e)

def save_hashes():
    with open(FILE_NAME, "w") as f:
        json.dump(list(seen_hashes), f)

def get_file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

API_ID = 28488147
API_HASH = "a6a1451f063db8d579791a51b7270dff"
BOT_TOKEN = "7950704145:AAG9mn2aeFsuUibEIUPfX2LahVHA7EtTYvs"

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.group & (filters.photo | filters.video | filters.document))
def handle_media(client, message):
    try:
        file_path = app.download_media(message)
        file_hash = get_file_hash(file_path)
        os.remove(file_path)

        if file_hash in seen_hashes:
            message.delete()
            print("🗑️ ডুপ্লিকেট ডিলিট")
        else:
            seen_hashes.add(file_hash)
            save_hashes()
            print("✅ নতুন মিডিয়া সংরক্ষিত")
    except Exception as e:
        print("Error:", e)

print("🚀 Bot is running...")
app.run()
