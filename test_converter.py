"""Tests for the YouTube to MP3 converter, CLI, and API endpoints."""

import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
from starlette.testclient import TestClient

import converter
from app import app
from cli import build_parser


@pytest.fixture
def client():
    return TestClient(app)


def test_sanitize_filename():
    assert converter.sanitize_filename("valid_name") == "valid_name"
    assert converter.sanitize_filename('bad/\\:*?"<>|name') == "badname"
    assert converter.sanitize_filename("   multiple   spaces   ") == "multiple spaces"
    assert converter.sanitize_filename("///") == "audio"


def test_get_video_info_mock():
    mock_info = {
        "id": "dQw4w9WgXcQ",
        "title": "Rick Astley - Never Gonna Give You Up",
        "uploader": "RickAstleyVEVO",
        "duration": 213,
        "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/default.jpg",
        "webpage_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    }
    with patch("converter.yt_dlp.YoutubeDL") as mock_ydl:
        mock_ctx = mock_ydl.return_value.__enter__.return_value
        mock_ctx.extract_info.return_value = mock_info

        info = converter.get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert info["id"] == "dQw4w9WgXcQ"
        assert info["title"] == "Rick Astley - Never Gonna Give You Up"
        assert info["duration"] == 213
        assert info["duration_formatted"] == "3:33"
        assert info["uploader"] == "RickAstleyVEVO"


def test_get_video_info_long_duration():
    mock_info = {
        "id": "abc",
        "title": "Long Video",
        "uploader": "Artist",
        "duration": 3665,
        "thumbnail": "thumb.jpg",
    }
    with patch("converter.yt_dlp.YoutubeDL") as mock_ydl:
        mock_ctx = mock_ydl.return_value.__enter__.return_value
        mock_ctx.extract_info.return_value = mock_info

        info = converter.get_video_info("https://example.com")
        assert info["duration_formatted"] == "1:01:05"


def test_download_audio_as_mp3_mock(tmp_path):
    mock_info = {
        "id": "test1234",
        "title": "Test Audio Title",
        "duration": 120,
    }

    # Simulate yt_dlp creating the mp3 file
    def fake_extract_info(url, download=True):
        output_file = tmp_path / "Test Audio Title.mp3"
        output_file.write_bytes(b"dummy mp3 audio data")
        return mock_info

    with patch("converter.yt_dlp.YoutubeDL") as mock_ydl:
        mock_ctx = mock_ydl.return_value.__enter__.return_value
        mock_ctx.extract_info.side_effect = fake_extract_info

        result = converter.download_audio_as_mp3(
            url="https://www.youtube.com/watch?v=test1234",
            output_dir=str(tmp_path),
            bitrate="320",
        )
        assert result["title"] == "Test Audio Title"
        assert result["bitrate"] == "320"
        assert result["filename"] == "Test Audio Title.mp3"
        assert os.path.exists(result["filepath"])
        assert result["filesize"] > 0


def test_cli_argument_parsing():
    parser = build_parser()
    args = parser.parse_args(["https://www.youtube.com/watch?v=123", "-b", "320", "-o", "./my_audio", "-n", "custom_song", "-i"])
    assert args.url == "https://www.youtube.com/watch?v=123"
    assert args.bitrate == "320"
    assert args.output == "./my_audio"
    assert args.name == "custom_song"
    assert args.info_only is True


def test_api_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_serve_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "YouTube to MP3 Converter" in response.text or "Convertidor" in response.text


def test_api_get_info_success(client):
    mock_info = {
        "id": "vid123",
        "title": "Awesome Track",
        "uploader": "Band",
        "duration": 180,
        "duration_formatted": "3:00",
        "thumbnail": "http://img.jpg",
        "webpage_url": "https://www.youtube.com/watch?v=vid123",
    }
    with patch("converter.get_video_info", return_value=mock_info):
        response = client.post("/api/info", json={"url": "https://www.youtube.com/watch?v=vid123"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Awesome Track"
        assert data["duration_formatted"] == "3:00"


def test_api_get_info_invalid_url(client):
    with patch("converter.get_video_info", side_effect=ValueError("Video no encontrado")):
        response = client.post("/api/info", json={"url": "https://invalid-url.com"})
        assert response.status_code == 400
        assert "Video no encontrado" in response.json()["detail"]


def test_api_download_success(client, tmp_path):
    dummy_mp3 = tmp_path / "song.mp3"
    dummy_mp3.write_bytes(b"\xFF\xFB\x90\x00DummyMP3Data")

    mock_result = {
        "filepath": str(dummy_mp3),
        "filename": "song.mp3",
        "title": "My Song",
        "id": "vid123",
        "duration": 180,
        "bitrate": "192",
        "filesize": len(dummy_mp3.read_bytes()),
    }

    with patch("converter.download_audio_as_mp3", return_value=mock_result):
        response = client.get("/api/download?url=https://www.youtube.com/watch?v=vid123&bitrate=192")
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/mpeg"
        assert 'filename="song.mp3"' in response.headers["content-disposition"]
        assert len(response.content) > 0
