import subprocess

def merge_audio_video(video_path, audio_path, output_path):
    """
    Merge audio and video files using ffmpeg.
    Replaces audio in the video with the new audio track.

    :param video_path: Path to the input video file
    :param audio_path: Path to the input audio file
    :param output_path: Path to the output file
    """
    command = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        output_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Audio and video merged successfully into {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg process failed: {e}")

def mute_video(input_path, output_path):
    """
    Mute the audio in a video file using ffmpeg.

    :param input_path: Path to the input video file
    :param output_path: Path to the output video file with audio muted
    """
    command = [
        'ffmpeg',
        '-i', input_path,
        '-an',  # No audio
        output_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Video muted successfully, output saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg process failed: {e}")
