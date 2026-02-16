import os
import pickle
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# --- আপনার তথ্যসমূহ ---
API_ID = 32779459
API_HASH = "f3a12806b4ba99203461f813041c486e"
BOT_TOKEN = "8535419158:AAGEoEPbFKwE5Gx0V4_f2cxkilzhexlS65A"
ADMIN_ID = 6487613131
CHANNEL_ID = -1002424019668
CHANNEL_LINK = "https://t.me/aurpon_mood_hub"

app = Client("AurponProBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ডাটাবেস ফাইল লোড করা (লিঙ্ক সেভ রাখার জন্য)
DB_FILE = "database.pkl"
if os.path.exists(DB_FILE):
    with open(DB_FILE, "rb") as f:
        file_db = pickle.load(f)
else:
    file_db = {}

def save_db():
    with open(DB_FILE, "wb") as f:
        pickle.dump(file_db, f)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    text_parts = message.text.split()
    param = text_parts[1] if len(text_parts) > 1 else None

    # ১. ফোর্স সাবস্ক্রাইব চেক
    try:
        await client.get_chat_member(CHANNEL_ID, user_id)
    except UserNotParticipant:
        return await message.reply_text(
            f"👋 **হ্যালো {message.from_user.first_name}!**\n\nআমাদের সেবা ব্যবহার করতে আপনাকে চ্যানেলে জয়েন করতে হবে।",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{client.me.username}?start={param}" if param else f"https://t.me/{client.me.username}?start=start")]
            ])
        )

    # ২. ফাইল পাঠানো
    if param and param in file_db:
        await message.reply_text("⚡️ **ফাইলটি প্রসেস হচ্ছে...**")
        try:
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=ADMIN_ID,
                message_id=int(param)
            )
        except:
            await message.reply_document(file_db[param], caption="✅ **ফাইলটি সফলভাবে পাওয়া গেছে!**")
    else:
        await message.reply_text(
            f"🔥 **Welcome to Aurpon File Store!**\n\nআপনি যদি এডমিন হন, তবে যেকোনো ফাইল পাঠান লিঙ্ক তৈরি করতে। আর ইউজার হলে শেয়ার করা লিঙ্কে ক্লিক করুন।",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Developer", url="https://t.me/Aurponbro")]
            ])
        )

@app.on_message((filters.document | filters.video | filters.audio) & filters.private)
async def handle_files(client, message):
    if message.from_user.id != ADMIN_ID:
        return

    # ফাইল আইডি সেভ করা
    file_id = message.document.file_id if message.document else (message.video.file_id if message.video else message.audio.file_id)
    msg_id = str(message.id)
    file_db[msg_id] = file_id
    save_db() # ডাটাবেসে সেভ করা
    
    link = f"https://t.me/{client.me.username}?start={msg_id}"
    
    await message.reply_text(
        f"✅ **নতুন ফাইল স্টোর করা হয়েছে!**\n\n🔗 **আপনার শেয়ার লিঙ্ক:**\n`{link}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Copy Link", url=link)],
            [InlineKeyboardButton("📢 Share to Channel", url=f"https://t.me/share/url?url={link}")]
        ])
    )

print("🚀 প্রফেশনাল ফাইল স্টোর বট চালু হয়েছে!")
app.run()
