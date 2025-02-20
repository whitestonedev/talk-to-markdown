import os
from pytubefix import YouTube
from tqdm import tqdm

from utils import slugfy


def download_youtube_mp3(video_id: str) -> str:
    """
    Downloads a YouTube video as MP3 e salva na pasta 'talks' com barra de progresso.

    Args:
        video_id: O ID do vídeo do YouTube.
    """

    yt_url = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(yt_url)
    audio_stream = yt.streams.filter(only_audio=True).first()

    if audio_stream:
        download_path = "talks"
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        with tqdm(
            unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=yt.title
        ) as t:
            output_path = audio_stream.download(output_path=download_path)
            path = f"src/talks/{slugfy(yt.title)}"
            if not os.path.exists(path):
                os.makedirs(path)
            destination_path = f"{path}/{slugfy(yt.title)}.mp3"
            os.rename(output_path, destination_path)
            return os.path.abspath(destination_path)
    else:
        return None


if __name__ == "__main__":
    video_id = "AyDTZnlQk24"  # Exemplo: "Rick Astley - Never Gonna Give You Up"
    download_youtube_mp3(video_id)
