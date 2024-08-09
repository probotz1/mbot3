from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import ffmpeg
import os
from pyrogram.errors import FloodWait
import time

# Initialize the bot
app = Client("my_bot", api_id="28015531", api_hash="2ab4ba37fd5d9ebf1353328fc915ad28", bot_token="7321073695:AAE2ZvYJg6_dQNhEvznmRCSsKMoNHoQWnuI")

# Utilities
def download_file(client, message):
    file_id = message.video.file_id if message.video else message.document.file_id
    file_path = client.download_media(file_id)
    return file_path

def run_ffmpeg_process(input_path, output_path, process):
    try:
        process(input=input_path, output=output_path).run()
        return output_path
    except Exception as e:
        return str(e)

def format_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024**2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024**3:
        return f"{size / 1024**2:.2f} MB"
    else:
        return f"{size / 1024**3:.2f} GB"

async def send_progress_message(message, status, file_size=None, progress=None, speed=None, eta=None):
    progress_bar = "⬢" * int(progress // 2) + "⬡" * int((100 - progress) // 2)
    status_message = f"""
    {status}

    ╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
    ┣⪼ 🗃️ Sɪᴢᴇ: {file_size} | {file_size}
    ┣⪼ ⏳️ Dᴏɴᴇ : {progress:.2f}%
    ┣⪼ 🚀 Sᴩᴇᴇᴅ: {speed}
    ┣⪼ ⏰️ Eᴛᴀ: {eta}
    ╰━━━━━━━━━━━━━━━➣
    """
    await message.reply_text(status_message)

# Main menu with features
@app.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼️ Thumbnail Extractor", callback_data="thumbnail_extractor")],
        [InlineKeyboardButton("✏️ Caption and Buttons Editor", callback_data="caption_editor")],
        [InlineKeyboardButton("🎵 Audio & Subtitles Remover", callback_data="audio_subtitle_remover")],
        [InlineKeyboardButton("🎵 Audio & Subtitles Extractor", callback_data="audio_subtitle_extractor")],
        [InlineKeyboardButton("✂️ Video Trimmer", callback_data="video_trimmer")],
        [InlineKeyboardButton("➕ Video Merger", callback_data="video_merger")],
        [InlineKeyboardButton("🔇 Mute Audio in Video File", callback_data="mute_audio")],
        [InlineKeyboardButton("🎥 Video and Audio Merger", callback_data="video_audio_merger")],
        [InlineKeyboardButton("🎥 Video and Subtitle Merger", callback_data="video_subtitle_merger")],
        [InlineKeyboardButton("🎥 Video to GIF Converter", callback_data="video_to_gif")],
        [InlineKeyboardButton("✂️ Video Splitter", callback_data="video_splitter")],
        [InlineKeyboardButton("🖼️ Screenshot Generator", callback_data="screenshot_generator")],
        [InlineKeyboardButton("🖼️ Manual Screenshot Generator", callback_data="manual_screenshot")],
        [InlineKeyboardButton("📹 Video Sample Generator", callback_data="video_sample_generator")],
        [InlineKeyboardButton("🎵 Video to Audio Converter", callback_data="video_to_audio")],
        [InlineKeyboardButton("📉 Video Optimizer", callback_data="video_optimizer")],
        [InlineKeyboardButton("🔀 Video Converter", callback_data="video_converter")],
        [InlineKeyboardButton("✏️ Video Renamer", callback_data="video_renamer")],
        [InlineKeyboardButton("ℹ️ Media Information", callback_data="media_info")],
        [InlineKeyboardButton("📁 Create Archive File", callback_data="create_archive")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")],
    ])
    await message.reply("Select an option from below 👇", reply_markup=keyboard)

# Thumbnail Extractor
@app.on_callback_query(filters.regex("thumbnail_extractor"))
async def thumbnail_extractor(client, callback_query):
    await callback_query.message.edit("Send me a video file to extract thumbnails.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "thumbnail.jpg"
            process = ffmpeg.input(file_path).filter('thumbnail', n=1).output(output_path, vframes=1)
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Caption and Buttons Editor
# To be implemented according to your specific needs.

# Audio & Subtitles Remover
@app.on_callback_query(filters.regex("audio_subtitle_remover"))
async def audio_subtitle_remover(client, callback_query):
    await callback_query.message.edit("Send me a video file to remove audio or subtitles.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "output_no_audio.mp4"
            process = ffmpeg.input(file_path).output(output_path, an=None, sn=None)
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Audio & Subtitles Extractor
@app.on_callback_query(filters.regex("audio_subtitle_extractor"))
async def audio_subtitle_extractor(client, callback_query):
    await callback_query.message.edit("Send me a video file to extract audio or subtitles.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            audio_output = "output_audio.aac"
            subtitle_output = "output_subtitles.srt"
            audio_process = ffmpeg.input(file_path).output(audio_output, vn=None)
            subtitle_process = ffmpeg.input(file_path).output(subtitle_output, vn=None, an=None, map='0:s:0')
            run_ffmpeg_process(file_path, audio_output, audio_process)
            run_ffmpeg_process(file_path, subtitle_output, subtitle_process)
            await message.reply_document(audio_output)
            await message.reply_document(subtitle_output)
            os.remove(file_path)
            os.remove(audio_output)
            os.remove(subtitle_output)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Trimmer
@app.on_callback_query(filters.regex("video_trimmer"))
async def video_trimmer(client, callback_query):
    await callback_query.message.edit("Send me a video file and specify start and end times to trim.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            start_time = "00:00:30"  # Replace with dynamic time from user input
            end_time = "00:01:00"  # Replace with dynamic time from user input
            output_path = "trimmed_video.mp4"
            process = ffmpeg.input(file_path, ss=start_time, to=end_time).output(output_path)
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Merger
@app.on_callback_query(filters.regex("video_merger"))
async def video_merger(client, callback_query):
    await callback_query.message.edit("Send me the videos you want to merge.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            video1_path = download_file(client, message)
            # Wait for the second file upload
            video2_path = download_file(client, message)
            output_path = "merged_video.mp4"
            process = ffmpeg.input(video1_path).input(video2_path).output(output_path)
            result = run_ffmpeg_process(video1_path, output_path, process)
            await message.reply_document(result)
            os.remove(video1_path)
            os.remove(video2_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Mute Audio in Video File
@app.on_callback_query(filters.regex("mute_audio"))
async def mute_audio(client, callback_query):
    await callback_query.message.edit("Send me a video file to mute audio.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "muted_video.mp4"
            process = ffmpeg.input(file_path).output(output_path, an=None)
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video and Audio Merger
@app.on_callback_query(filters.regex("video_audio_merger"))
async def video_audio_merger(client, callback_query):
    await callback_query.message.edit("Send me the video and audio files to merge.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            video_path = download_file(client, message)
            # Wait for the audio file upload
            audio_path = download_file(client, message)
            output_path = "merged_video_audio.mp4"
            process = ffmpeg.input(video_path).input(audio_path).output(output_path)
            result = run_ffmpeg_process(video_path, output_path, process)
            await message.reply_document(result)
            os.remove(video_path)
            os.remove(audio_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video and Subtitle Merger
@app.on_callback_query(filters.regex("video_subtitle_merger"))
async def video_subtitle_merger(client, callback_query):
    await callback_query.message.edit("Send me the video and subtitle files to merge.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            video_path = download_file(client, message)
            # Wait for the subtitle file upload
            subtitle_path = download_file(client, message)
            output_path = "merged_video_subtitles.mp4"
            process = ffmpeg.input(video_path).input(subtitle_path).output(output_path)
            result = run_ffmpeg_process(video_path, output_path, process)
            await message.reply_document(result)
            os.remove(video_path)
            os.remove(subtitle_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video to GIF Converter
@app.on_callback_query(filters.regex("video_to_gif"))
async def video_to_gif(client, callback_query):
    await callback_query.message.edit("Send me a video file to convert to GIF.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "video.gif"
            process = ffmpeg.input(file_path).output(output_path, vf="fps=10,scale=320:-1:flags=lanczos")
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Splitter
@app.on_callback_query(filters.regex("video_splitter"))
async def video_splitter(client, callback_query):
    await callback_query.message.edit("Send me a video file to split into parts.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "split_video.mp4"
            process = ffmpeg.input(file_path).output(output_path, vf="fps=10,scale=320:-1:flags=lanczos")
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Screenshot Generator
@app.on_callback_query(filters.regex("screenshot_generator"))
async def screenshot_generator(client, callback_query):
    await callback_query.message.edit("Send me a video file to generate screenshots.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "screenshot.png"
            process = ffmpeg.input(file_path).filter('thumbnail', n=1).output(output_path, vframes=1)
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Manual Screenshot Generator
@app.on_callback_query(filters.regex("manual_screenshot"))
async def manual_screenshot(client, callback_query):
    await callback_query.message.edit("Send me a video file to generate a screenshot manually.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "manual_screenshot.png"
            process = ffmpeg.input(file_path).filter('select', 'eq(n\,1)').output(output_path, vframes=1)
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Sample Generator
@app.on_callback_query(filters.regex("video_sample_generator"))
async def video_sample_generator(client, callback_query):
    await callback_query.message.edit("Send me a video file to generate a sample.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "video_sample.mp4"
            process = ffmpeg.input(file_path).output(output_path, t="00:00:10")
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video to Audio Converter
@app.on_callback_query(filters.regex("video_to_audio"))
async def video_to_audio(client, callback_query):
    await callback_query.message.edit("Send me a video file to convert to audio.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "audio.mp3"
            process = ffmpeg.input(file_path).output(output_path, vn=None)
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Optimizer
@app.on_callback_query(filters.regex("video_optimizer"))
async def video_optimizer(client, callback_query):
    await callback_query.message.edit("Send me a video file to optimize.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "optimized_video.mp4"
            process = ffmpeg.input(file_path).output(output_path, vcodec="libx265", crf=28)
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Converter
@app.on_callback_query(filters.regex("video_converter"))
async def video_converter(client, callback_query):
    await callback_query.message.edit("Send me a video file to convert to another format.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "converted_video.mp4"
            process = ffmpeg.input(file_path).output(output_path)
            result = run_ffmpeg_process(file_path, output_path, process)
            await message.reply_document(result)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Renamer
@app.on_callback_query(filters.regex("video_renamer"))
async def video_renamer(client, callback_query):
    await callback_query.message.edit("Send me a video file and specify the new name.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = download_file(client, message)
            new_name = "new_video_name.mp4"  # Replace with dynamic name from user input
            os.rename(file_path, new_name)
            await message.reply_document(new_name)
            os.remove(new_name)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Media Information
@app.on_callback_query(filters.regex("media_info"))
async def media_info(client, callback_query):
    await callback_query.message.edit("Send me a video or audio file to get media information.")

    @app.on_message(filters.media)
    async def handle_media(client, message):
        try:
            file_path = download_file(client, message)
            info = ffmpeg.probe(file_path)
            await message.reply_text(f"Media Info: {info}")
            os.remove(file_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Create Archive File
@app.on_callback_query(filters.regex("create_archive"))
async def create_archive(client, callback_query):
    await callback_query.message.edit("Send me the files you want to include in the archive.")

    @app.on_message(filters.document)
    async def handle_document(client, message):
        try:
            file_path = download_file(client, message)
            output_path = "archive.zip"
            process = f"zip -r {output_path} {file_path}"
            os.system(process)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Cancel
@app.on_callback_query(filters.regex("cancel"))
async def cancel(client, callback_query):
    await callback_query.message.edit("Operation canceled.")

# Start the bot
app.run()
