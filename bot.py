from pyrogram import Client, filters
from pyrogram.types import Message
from ffmpeg import merge_audio_video, mute_video
import os

API_ID = "28015531"
API_HASH = "2ab4ba37fd5d9ebf1353328fc915ad28"
BOT_TOKEN = "7321073695:AAE2ZvYJg6_dQNhEvznmRCSsKMoNHoQWnuI"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Bot started! Send me a video and an audio file.")

@app.on_message(filters.video)
async def handle_video(client, message: Message):
    video_path = "downloads/video.mp4"
    await message.download(video_path)
    await message.reply("Video downloaded. Now send the audio file.")

@app.on_message(filters.audio)
async def handle_audio(client, message: Message):
    audio_path = "downloads/audio.mp3"
    await message.download(audio_path)
    await message.reply("Audio downloaded. Merging with video...")

    video_path = "downloads/video.mp4"
    output_path = "downloads/merged_video.mp4"

    merge_audio_video(video_path, audio_path, output_path)
    await message.reply("Audio merged with video. Processing completed!")

@app.on_message(filters.document)
async def handle_document(client, message: Message):
    file_path = "downloads/document.mkv"
    await message.download(file_path)
    output_path = "downloads/muted_video.mp4"
    mute_video(file_path, output_path)
    await message.reply("Video muted successfully!")

app.run()
