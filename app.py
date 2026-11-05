"""FastAPI server for YouTube to MP3 converter web service."""

import os
import shutil
import tempfile
import urllib.parse
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import converter

app = FastAPI(
    title="YouTube to MP3 Converter",
    description="Convierte videos de YouTube a archivos MP3 con alta calidad de audio.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InfoRequest(BaseModel):
    url: str


def cleanup_directory(directory: str):
    """Safely removes temporary directory after sending file."""
    try:
        shutil.rmtree(directory, ignore_errors=True)
    except Exception:
        pass


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serves the main application page."""
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Convertidor YouTube a MP3</h1>", status_code=200)


@app.get("/api/health")
async def health_check():
    """Endpoint to verify server status."""
    return {"status": "ok", "service": "YouTube to MP3 Converter"}


@app.post("/api/info")
async def get_info(payload: InfoRequest):
    """Retrieve video metadata without downloading."""
    url = payload.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="Se requiere una URL válida.")
    try:
        data = converter.get_video_info(url)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar el enlace: {str(e)}")


@app.get("/api/download")
async def download_mp3(
    background_tasks: BackgroundTasks,
    url: str = Query(..., description="YouTube video URL"),
    bitrate: str = Query(converter.DEFAULT_BITRATE, description="Bitrate: 128, 192, 256, 320"),
):
    """Extract and download MP3 audio file directly to user device."""
    url = url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="Se requiere el parámetro 'url'.")

    temp_dir = tempfile.mkdtemp(prefix="yt_mp3_")

    try:
        result = converter.download_audio_as_mp3(
            url=url,
            output_dir=temp_dir,
            bitrate=bitrate,
        )
        filepath = result["filepath"]
        filename = result["filename"]

        # Register cleanup to run after response is finished
        background_tasks.add_task(cleanup_directory, temp_dir)

        # RFC 5987 / URL-encoded filename for Content-Disposition
        encoded_filename = urllib.parse.quote(filename)
        headers = {
            "Content-Disposition": f"attachment; filename=\"{filename}\"; filename*=UTF-8''{encoded_filename}",
            "X-Video-Title": urllib.parse.quote(result["title"]),
        }

        return FileResponse(
            path=filepath,
            media_type="audio/mpeg",
            filename=filename,
            headers=headers,
        )
    except Exception as e:
        cleanup_directory(temp_dir)
        raise HTTPException(status_code=500, detail=f"Error durante la extracción de audio: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
