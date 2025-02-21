from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
import json
from pathlib import Path

# Importações das funções do projeto
from src.assembly import assemblyai_transcribe
from src.gemini import summarize_speaker_text_gemini
from src.youtube import download_youtube_mp3
from src.utils import slugfy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Define o diretório raiz para salvar os arquivos
ROOT_TALKS_DIR = Path(__file__).parent / "talks"
ROOT_TALKS_DIR.mkdir(parents=True, exist_ok=True)


def process_video(video_id: str, custom_prompt: str, sid: str):
    """
    Processa um vídeo do YouTube: baixa o áudio, transcreve e gera um resumo.
    """

    def send_update(stage, log, status):
        """Envia atualizações do processo via WebSocket"""
        update = {"stage": stage, "log": log, "status": status}
        socketio.emit('timeline_update', update, room=sid)
        print(f"{stage} - {log}")

    send_update("Iniciando...", "Starting the process...", "LOADING")

    try:
        send_update("Baixando vídeo do YouTube...", f"Downloading video ID: {video_id}", "LOADING")
        audio_filepath, yt_title = download_youtube_mp3(video_id, str(ROOT_TALKS_DIR))
        yt_title_slug = slugfy(yt_title)

        # Define o diretório do vídeo
        video_dir = ROOT_TALKS_DIR / yt_title_slug
        video_dir.mkdir(parents=True, exist_ok=True)

        send_update("Áudio baixado...", f"Downloaded: {audio_filepath}", "LOADING")
    except Exception as e:
        send_update("Erro ao baixar vídeo", f"Error: {e}", "ERROR")
        return

    # Caminho do arquivo de transcrição dentro da pasta do vídeo
    transcription_file_path = video_dir / "transcription_id.txt"
    transcription_id = None

    if transcription_file_path.exists():
        try:
            with open(transcription_file_path, "r") as f:
                transcription_id = f.read().strip()
            send_update("Transcrição existente encontrada", f"Transcription ID: {transcription_id}", "LOADING")
        except Exception as e:
            send_update("Erro ao ler transcrição existente", f"Error: {e}", "ERROR")
            return
    else:
        send_update("Nenhuma transcrição existente encontrada", "Proceeding with new transcription.", "LOADING")

    try:
        send_update("Iniciando transcrição...", "Starting transcription...", "LOADING")
        transcription = assemblyai_transcribe(transcription_id=transcription_id, audio_filepath=audio_filepath)
        send_update("Transcrição completa!", "Transcription completed.", "LOADING")
    except Exception as e:
        send_update("Erro na transcrição", f"Error: {e}", "ERROR")
        return

    # Salva a transcrição na pasta do vídeo
    transcription_json_path = video_dir / "transcription.json"
    try:
        send_update("Salvando transcrição...", f"Saving to: {transcription_json_path}", "LOADING")
        with open(transcription_json_path, "w") as f:
            json.dump(transcription.json_response, f, indent=4)
        send_update("Transcrição salva!", "Transcription saved successfully.", "LOADING")
    except Exception as e:
        send_update("Erro ao salvar transcrição", f"Error: {e}", "ERROR")
        return

    try:
        send_update("Iniciando resumo...", "Starting summarization...", "LOADING")
        summary_path = video_dir / "summary.md"

        article = summarize_speaker_text_gemini(
            data=transcription.json_response,
            output_path=str(summary_path),
            custom_prompt=custom_prompt
        )

        send_update("Resumo completo!", "Summarization completed.", "COMPLETED")
        socketio.emit('article', {"article": article}, room=sid)
    except Exception as e:
        send_update("Erro no resumo", f"Error: {e}", "ERROR")


@socketio.on('start_process')
def handle_start_process(data):
    video_id = data.get("video_id")
    custom_prompt = data.get("custom_prompt")
    sid = request.sid
    socketio.start_background_task(process_video, video_id, custom_prompt, sid)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
