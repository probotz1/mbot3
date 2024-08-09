from tqdm import tqdm
import time

def display_progress(total_size, current_size):
    progress = (current_size / total_size) * 100
    print(f"Progress: {progress:.2f}%")
