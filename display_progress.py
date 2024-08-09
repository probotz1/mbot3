import sys
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

class ProgressBar:
    def __init__(self, total_size):
        self.total_size = total_size
        self.current_size = 0

    def update(self, current_size):
        self.current_size = current_size
        percentage = (self.current_size / self.total_size) * 100
        bar_length = 40
        block = int(round(bar_length * self.current_size / self.total_size))
        progress = "|" + "=" * block + "-" * (bar_length - block) + "|"
        sys.stdout.write(f"\r{progress} {percentage:.2f}%")
        sys.stdout.flush()

def progress_for_pyrogram(current, total):
    progress = ProgressBar(total)
    progress.update(current)

async def on_message(client, message: Message):
    # This example assumes that `message` has a file to download or upload
    file_size = message.document.file_size
    await message.download(file_name="downloaded_file", progress=progress_for_pyrogram, progress_args=(file_size,))

app = Client("my_bot")

app.add_handler(MessageHandler(on_message, filters.document))

app.run()
