import os
import json
from assembly import assemblyai_transcribe
from src.gemini import summarize_speaker_text_gemini

from src.youtube import download_youtube_mp3


if __name__ == "__main__":
    print("Starting the process...")

    video_id = "ATeL5I8puL4"
    print(f"Downloading YouTube video with ID: {video_id}")
    audio_filepath = download_youtube_mp3(video_id)
    print(f"Downloaded audio file path: {audio_filepath}")

    # check if the file transcription_id.txt exists in the same folder as the audio file
    transcription__file_path = os.path.join(os.path.dirname(audio_filepath), "transcription_id.txt")
    if os.path.exists(transcription__file_path):
        with open(transcription__file_path, "r") as f:
            transcription_id = f.read()
        print(f"Found existing transcription ID: {transcription_id}")
    else:
        transcription_id = None
        print("No existing transcription ID found.")

    print("Starting transcription process...")
    transcription = assemblyai_transcribe(
        transcription_id=transcription_id, audio_filepath=audio_filepath
    )
    print("Transcription completed.")

    transcription_json_path = (
        f"transcription_{os.path.basename(audio_filepath).split('.')[0]}.json"
    )
    print(f"Saving transcription to: {transcription_json_path}")
    # salvar no mesmo folder do arquivo de áudio
    with open(
        os.path.join(os.path.dirname(audio_filepath), transcription_json_path), "w"
    ) as f:
        json.dump(transcription.json_response, f, indent=4)
    print("Transcription saved.")

    print("Starting summarization process...")
    gemini_output_path = os.path.join(
        os.path.dirname(audio_filepath), f"gemini_summary_{os.path.basename(audio_filepath).split('.')[0]}.md"
    )
    custom_prompt = None
    article = summarize_speaker_text_gemini(data=transcription.json_response, output_path=gemini_output_path, custom_prompt=custom_prompt)
    print("Summarization completed.")