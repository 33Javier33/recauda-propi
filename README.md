# Convertidor de YouTube a MP3

Una herramienta completa y eficiente para convertir enlaces de YouTube en archivos de audio MP3, extrayendo el audio en alta calidad y guardándolo directamente en tu dispositivo.

Ofrece una **interfaz web moderna y responsiva**, soporte para despliegue estático y en la nube (Vercel, GitHub Pages) y una **herramienta por línea de comandos (CLI)** con backend en Python.

---

## Modos de Uso

El proyecto está diseñado para funcionar de dos formas:

1. **Modo Web / Despliegue en Vercel (Front-end)**:
   - Funciona sin necesidad de configurar un servidor propio.
   - Detecta la disponibilidad del video mediante YouTube oEmbed.
   - Proporciona opciones de descarga y conversión directa de MP3 a tu dispositivo.
2. **Modo Servidor Local / Full-Stack (Python + FastAPI + yt-dlp + FFmpeg)**:
   - Extracción directa nativa con `yt-dlp` y conversión automática con `ffmpeg`.
   - Soporte para bitrates personalizados (128, 192, 256, 320 kbps).
   - Inyección de etiquetas ID3 y metadatos.

---

## Características

- 🎵 **Extracción directa de audio**: Convierte cualquier video de YouTube a formato MP3 limpio y optimizado.
- 🎚️ **Selección de calidad (Bitrate)**: Soporte para 128 kbps, 192 kbps, 256 kbps y hasta 320 kbps.
- 📱 **Descarga directa en tu dispositivo**: Compatible con navegadores en teléfonos móviles (Android, iOS) y ordenadores.
- 🖼️ **Metadatos e información**: Muestra el título, autor, duración y miniatura del video antes de la conversión.
- ☁️ **Compatible con Vercel**: Incluye configuración `vercel.json` y fallbacks en cliente.
- 💻 **CLI Integrada**: Opción para automatizar descargas por terminal o en scripts.
- 🏷️ **Etiquetas ID3 incrustadas**: Guarda metadatos automáticos dentro del archivo MP3 (título, autor).

---

## Requisitos para Modo Local / Backend

1. **Python 3.10+**
2. **FFmpeg** instalado en el sistema operativo:
   - En Debian/Ubuntu: `sudo apt-get install ffmpeg`
   - En macOS: `brew install ffmpeg`
   - En Windows: `winget install Gyan.FFmpeg` o descargando desde ffmpeg.org

---

## Instalación y Ejecución Local

1. Clona el repositorio e ingresa al directorio:
   ```bash
   git clone <url-del-repositorio>
   cd recauda-propi
   ```

2. Instala las dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```

3. Inicia el servidor web local con Uvicorn:
   ```bash
   python3 app.py
   ```
   O directamente:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

4. Abre tu navegador en `http://localhost:8000`.

---

## Despliegue en Vercel

Este repositorio incluye `vercel.json` para despliegue instantáneo en Vercel:
1. Conecta tu repositorio de GitHub a tu cuenta de Vercel.
2. Selecciona el proyecto y despliega (Vercel detectará la configuración estática automáticamente).
3. Tu aplicación web estará disponible de inmediato.

---

## Línea de Comandos (CLI)

Puedes usar la herramienta por terminal `cli.py` para descargar audios sin abrir el navegador:

```bash
# Descarga básica con calidad estándar (192 kbps) a ./downloads
python3 cli.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Descarga con máxima calidad (320 kbps) en una carpeta específica
python3 cli.py "https://www.youtube.com/watch?v=VIDEO_ID" -b 320 -o ~/Musica

# Asignar un nombre personalizado al archivo MP3
python3 cli.py "https://www.youtube.com/watch?v=VIDEO_ID" -n "mi_cancion_favorita"

# Solo consultar información y metadatos sin descargar
python3 cli.py "https://www.youtube.com/watch?v=VIDEO_ID" -i
```

Opciones disponibles en el CLI:
```text
options:
  -h, --help            Muestra el mensaje de ayuda.
  -o, --output OUTPUT   Directorio destino donde guardar el archivo (default: ./downloads).
  -b, --bitrate BITRATE Calidad en kbps: 128, 192, 256, 320 (default: 192).
  -n, --name NAME       Nombre personalizado para el archivo MP3 generado.
  -i, --info-only       Muestra información del video sin descargar.
```

---

## Pruebas Automatizadas

Para ejecutar la suite de pruebas unitarias y de integración:

```bash
pytest
```
