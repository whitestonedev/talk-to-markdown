import os
import json
from assembly import assemblyai_transcribe
from src.gemini import summarize_speaker_text_gemini

from src.youtube import download_youtube_mp3

#
# def generate_articles_markdown(process_folder):
#     """Gera artigos markdown para cada falante e atualiza o estado de processamento."""
#     state = load_state(process_folder)
#     if not state or state["process_stage"] != "segmentation_completed":
#         print("Segmentação de falantes não concluída ou arquivo de estado faltando.")
#         return None
#
#     segments_data = load_json_data(state["segments_file"])
#     if not segments_data:
#         state["process_stage"] = "error"
#         state["error_message"] = "Falha ao carregar dados de segmentos de falantes."
#         save_state(process_folder, state)
#         return None
#
#     summary_files_list = []
#     for speaker_id, text_list in segments_data.items():
#         markdown_article = summarize_speaker_text_gemini(
#             speaker_id, text_list, process_folder
#         )
#         if markdown_article:
#             summary_files_list.append(
#                 str(process_folder / f"summary_speaker_{speaker_id}.md")
#             )  # Rastreia arquivos de resumo
#         else:
#             print(f"Falha ao gerar resumo para o falante {speaker_id}.")
#
#     state["summary_files"] = summary_files_list  # Atualiza lista de arquivos de resumo
#     if (
#         state["process_stage"] != "error"
#     ):  # Apenas se não ocorreu erro durante a sumarização
#         state["process_stage"] = "articles_generated"
#     save_state(process_folder, state)
#     if state["process_stage"] == "articles_generated":
#         print("Geração de artigos concluída.")
#     return summary_files_list



if __name__ == "__main__":
    print("Starting the process...")

    video_id = "CrzX1Hw_hA0"
    print(f"Downloading YouTube video with ID: {video_id}")
    audio_filepath = download_youtube_mp3(video_id)
    print(f"Downloaded audio file path: {audio_filepath}")

    # check if the file transcription_id.txt exists
    if os.path.exists("transcription_id.txt"):
        with open("transcription_id.txt", "r") as f:
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
    article = summarize_speaker_text_gemini(data=transcription.json_response, output_path=gemini_output_path)
    print("Summarization completed.")