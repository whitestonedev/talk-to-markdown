import os

import assemblyai as aai

from tqdm import tqdm

from settings import ASSEMBLYAI_API_KEY

aai.settings.api_key = ASSEMBLYAI_API_KEY


def assemblyai_transcribe(
    audio_filepath: str = None, transcription_id: str = None
):
    """Transcreve arquivo de áudio usando AssemblyAI com diarização, reutiliza transcrições existentes pelo ID."""
    transcription = None
    if transcription_id:
        print(
            f"Transcrição existente encontrada no estado, ID: {transcription_id}. Tentando recuperar..."
        )
        try:
            transcript = aai.Transcript.get_by_id(transcription_id)
            if transcript and transcript.status == "completed":
                transcription = transcript
                return transcription
            else:
                print(
                    f"Falha ao recuperar transcrição existente ou transcrição incompleta. Status: {transcript.status if transcript else 'Unknown'}. Procedendo com nova transcrição."
                )
        except Exception as e:
            raise e

    if transcription is None:
        print(
            "Nenhuma transcrição existente válida encontrada ou recuperação falhou. Enviando para nova transcrição..."
        )
        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(
            speaker_labels=True, language_code="pt"
        )
        try:
            transcript = transcriber.transcribe(audio_filepath, config)
            if transcript and transcript.status == "completed":
                transcription = transcript
                print(
                    f"Nova transcrição concluída com sucesso, ID: {transcript.id}"
                )
                transcription_id_file_path = os.path.join(
                    os.path.dirname(audio_filepath), "transcription_id.txt"
                )
                with open(transcription_id_file_path, "w") as f:
                    f.write(transcription.id)
                return transcription
            else:
                print(
                    f"Nova transcrição falhou ou incompleta. Status: {transcript.status if transcript else 'Unknown'}"
                )
                return None
        except Exception as e:
            raise e
    return transcription



