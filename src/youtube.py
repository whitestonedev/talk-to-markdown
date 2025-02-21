import os
from pathlib import Path
from pytubefix import YouTube
from tqdm import tqdm
from src.utils import slugfy

def download_youtube_mp3(video_id: str, destination_path: str = "talks") -> tuple[str, str] | None:
    """
    Downloads a YouTube video as MP3 and saves it to the specified folder with a progress bar.

    Args:
        video_id (str): The ID of the YouTube video.
        destination_path (str, optional): The directory where the MP3 file will be saved. Defaults to "talks".

    Returns:
        tuple[str, str] | None: Absolute path of the saved file and video title, or None if the download fails.
    """
    yt_url = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(yt_url)

    audio_stream = yt.streams.filter(only_audio=True).first()
    if not audio_stream:
        print("No audio stream available.")
        return None

    # Ensure main destination directory exists
    dest_path = Path(destination_path).resolve()
    dest_path.mkdir(parents=True, exist_ok=True)

    # Create video-specific directory
    video_folder = dest_path / slugfy(yt.title)
    video_folder.mkdir(parents=True, exist_ok=True)

    # Define final file path
    final_file_path = video_folder / "audio.mp3"

    # Download with progress bar
    temp_path = Path(audio_stream.download(output_path=dest_path))
    file_size = temp_path.stat().st_size

    with tqdm(total=file_size, unit="B", unit_scale=True, desc="Downloading") as pbar:
        def update_progress(stream, chunk, bytes_remaining):
            pbar.update(len(chunk))

        yt.register_on_progress_callback(update_progress)

    # Move and rename file
    temp_path.rename(final_file_path)

    return str(final_file_path), yt.title


if __name__ == "__main__":
    video_id = "AyDTZnlQk24"  # Example: "Rick Astley - Never Gonna Give You Up"
    result = download_youtube_mp3(video_id)
    if result:
        print(f"Download completed: {result[0]} (Title: {result[1]})")
