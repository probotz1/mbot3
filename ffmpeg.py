import subprocess

def run_ffmpeg_process(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg process failed: {e}")
