from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import ffmpeg
import os
import subprocess
import asyncio

# Initialize the bot
app = Client("my_bot", api_id="28015531", api_hash="2ab4ba37fd5d9ebf1353328fc915ad28", bot_token="7321073695:AAE2ZvYJg6_dQNhEvznmRCSsKMoNHoQWnuI")

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

# Utility functions
async def download_file(client, message):
    file = await client.download_media(message)
    return file

def run_ffmpeg_process(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg process failed: {e}")

# Thumbnail Extractor
@app.on_callback_query(filters.regex("thumbnail_extractor"))
async def thumbnail_extractor(client, callback_query):
    await callback_query.message.edit("Send me a video file to extract a thumbnail.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            output_path = "thumbnail.png"
            command = f"ffmpeg -i {file_path} -vf thumbnail -frames:v 1 {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Caption and Buttons Editor
# To be implemented

# Audio & Subtitles Remover
@app.on_callback_query(filters.regex("audio_subtitle_remover"))
async def audio_subtitle_remover(client, callback_query):
    await callback_query.message.edit("Send me a video file to remove audio or subtitles.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            output_path = "output_no_audio.mp4"
            command = f"ffmpeg -i {file_path} -an -sn {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Audio & Subtitles Extractor
@app.on_callback_query(filters.regex("audio_subtitle_extractor"))
async def audio_subtitle_extractor(client, callback_query):
    await callback_query.message.edit("Send me a video file to extract audio or subtitles.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            audio_output = "output_audio.aac"
            subtitle_output = "output_subtitles.srt"
            audio_command = f"ffmpeg -i {file_path} -vn -acodec copy {audio_output}"
            subtitle_command = f"ffmpeg -i {file_path} -an -vn -scodec copy {subtitle_output}"
            run_ffmpeg_process(audio_command)
            run_ffmpeg_process(subtitle_command)
            await message.reply_document(audio_output)
            await message.reply_document(subtitle_output)
            os.remove(file_path)
            os.remove(audio_output)
            os.remove(subtitle_output)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Trimmer
@app.on_callback_query(filters.regex("video_trimmer"))
async def video_trimmer(client, callback_query):
    await callback_query.message.edit("Send me a video file and specify start and end times to trim.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            start_time = "00:00:30"  # Replace with dynamic input from user
            end_time = "00:01:00"  # Replace with dynamic input from user
            output_path = "trimmed_video.mp4"
            command = f"ffmpeg -i {file_path} -ss {start_time} -to {end_time} -c copy {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Merger
@app.on_callback_query(filters.regex("video_merger"))
async def video_merger(client, callback_query):
    await callback_query.message.edit("Send me the videos you want to merge.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            video1_path = await download_file(client, message)
            video2_path = await download_file(client, message)
            output_path = "merged_video.mp4"
            command = f"ffmpeg -i {video1_path} -i {video2_path} -filter_complex concat=n=2:v=1:a=0 {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(video1_path)
            os.remove(video2_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Mute Audio in Video File
@app.on_callback_query(filters.regex("mute_audio"))
async def mute_audio(client, callback_query):
    await callback_query.message.edit("Send me a video file to mute the audio.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            output_path = "muted_video.mp4"
            command = f"ffmpeg -i {file_path} -an {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video and Audio Merger
@app.on_callback_query(filters.regex("video_audio_merger"))
async def video_audio_merger(client, callback_query):
    await callback_query.message.edit("Send me the video and audio files to merge.")

    @app.on_message(filters.video | filters.audio)
    async def handle_media(client, message):
        try:
            media1_path = await download_file(client, message)
            media2_path = await download_file(client, message)
            output_path = "merged_video_audio.mp4"
            command = f"ffmpeg -i {media1_path} -i {media2_path} -c:v copy -c:a aac {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(media1_path)
            os.remove(media2_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video and Subtitle Merger
@app.on_callback_query(filters.regex("video_subtitle_merger"))
async def video_subtitle_merger(client, callback_query):
    await callback_query.message.edit("Send me the video and subtitle files to merge.")

    @app.on_message(filters.video | filters.document)
    async def handle_media(client, message):
        try:
            video_path = await download_file(client, message)
            subtitle_path = await download_file(client, message)
            output_path = "video_with_subtitles.mp4"
            command = f"ffmpeg -i {video_path} -i {subtitle_path} -c:v copy -c:a copy -c:s mov_text {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(video_path)
            os.remove(subtitle_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video to GIF Converter
@app.on_callback_query(filters.regex("video_to_gif"))
async def video_to_gif(client, callback_query):
    await callback_query.message.edit("Send me a video file to convert to GIF.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            output_path = "output.gif"
            command = f"ffmpeg -i {file_path} {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Splitter
@app.on_callback_query(filters.regex("video_splitter"))
async def video_splitter(client, callback_query):
    await callback_query.message.edit("Send me a video file and specify duration to split.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            duration = "00:00:30"  # Replace with dynamic input from user
            output_path = "split_video.mp4"
            command = f"ffmpeg -i {file_path} -t {duration} -c copy {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Screenshot Generator
@app.on_callback_query(filters.regex("screenshot_generator"))
async def screenshot_generator(client, callback_query):
    await callback_query.message.edit("Send me a video file to generate a screenshot.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            output_path = "screenshot.png"
            command = f"ffmpeg -i {file_path} -ss 00:00:01 -vframes 1 {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Manual Screenshot Generator
@app.on_callback_query(filters.regex("manual_screenshot"))
async def manual_screenshot(client, callback_query):
    await callback_query.message.edit("Send me a video file and specify the time to capture a screenshot.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            timestamp = "00:00:01"  # Replace with dynamic input from user
            output_path = "manual_screenshot.png"
            command = f"ffmpeg -i {file_path} -ss {timestamp} -vframes 1 {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Sample Generator
@app.on_callback_query(filters.regex("video_sample_generator"))
async def video_sample_generator(client, callback_query):
    await callback_query.message.edit("Send me a video file to generate a sample.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            output_path = "video_sample.mp4"
            command = f"ffmpeg -i {file_path} -t 00:00:10 -c copy {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video to Audio Converter
@app.on_callback_query(filters.regex("video_to_audio"))
async def video_to_audio(client, callback_query):
    await callback_query.message.edit("Send me a video file to convert to audio.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            output_path = "audio_output.mp3"
            command = f"ffmpeg -i {file_path} -q:a 0 -map a {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Optimizer
@app.on_callback_query(filters.regex("video_optimizer"))
async def video_optimizer(client, callback_query):
    await callback_query.message.edit("Send me a video file to optimize.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            output_path = "optimized_video.mp4"
            command = f"ffmpeg -i {file_path} -vf scale=1280:720 -c:v libx264 -crf 23 {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Converter
@app.on_callback_query(filters.regex("video_converter"))
async def video_converter(client, callback_query):
    await callback_query.message.edit("Send me a video file and specify the format to convert to.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            output_path = "converted_video.mp4"
            format = "mp4"  # Replace with dynamic input from user
            command = f"ffmpeg -i {file_path} {output_path}"
            run_ffmpeg_process(command)
            await message.reply_document(output_path)
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Video Renamer
@app.on_callback_query(filters.regex("video_renamer"))
async def video_renamer(client, callback_query):
    await callback_query.message.edit("Send me a video file and specify the new name.")

    @app.on_message(filters.video)
    async def handle_video(client, message):
        try:
            file_path = await download_file(client, message)
            new_name = "renamed_video.mp4"  # Replace with dynamic input from user
            os.rename(file_path, new_name)
            await message.reply_document(new_name)
            os.remove(new_name)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Media Information
@app.on_callback_query(filters.regex("media_info"))
async def media_info(client, callback_query):
    await callback_query.message.edit("Send me a media file to get information.")

    @app.on_message(filters.video | filters.audio | filters.document)
    async def handle_media(client, message):
        try:
            file_path = await download_file(client, message)
            command = f"ffmpeg -i {file_path}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            await message.reply(result.stdout)
            os.remove(file_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Create Archive File
@app.on_callback_query(filters.regex("create_archive"))
async def create_archive(client, callback_query):
    await callback_query.message.edit("Send me the files to create an archive.")

    @app.on_message(filters.document)
    async def handle_document(client, message):
        try:
            file_path = await download_file(client, message)
            archive_path = "archive.zip"
            command = f"zip {archive_path} {file_path}"
            run_ffmpeg_process(command)
            await message.reply_document(archive_path)
            os.remove(file_path)
            os.remove(archive_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

# Cancel
@app.on_callback_query(filters.regex("cancel"))
async def cancel(client, callback_query):
    await callback_query.message.edit("Cancelled.")

# Start the bot
app.run()
