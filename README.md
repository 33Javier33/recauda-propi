# Convertidor de YouTube a MP3

Una herramienta completa y eficiente para convertir enlaces de YouTube en archivos de audio MP3, extrayendo el audio en alta calidad y guardándolo directamente en tu dispositivo.

Ofrece tanto una **interfaz web moderna y responsiva** como una **herramienta por línea de comandos (CLI)**.

---

## Características

- 🎵 **Extracción directa de audio**: Convierte cualquier video de YouTube a formato MP3 limpio y optimizado.
- 🎚️ **Selección de calidad (Bitrate)**: Soporte para 128 kbps, 192 kbps, 256 kbps y hasta 320 kbps.
- 📱 **Descarga directa en tu dispositivo**: Compatible con navegadores en teléfonos móviles (Android, iOS) y ordenadores.
- 🖼️ **Metadatos e información**: Muestra el título, autor, duración y miniatura del video antes de la conversión.
- 💻 **CLI Integrada**: Opción para automatizar descargas por terminal o en scripts.
- 🏷️ **Etiquetas ID3 incrustadas**: Guarda metadatos automáticos dentro del archivo MP3 (título, autor).

---

## Requisitos del Sistema

1. **Python 3.10+**
2. **FFmpeg** instalado en el sistema operativo:
   - En Debian/Ubuntu: `sudo apt-get install ffmpeg`
   - En macOS: `brew install ffmpeg`
   - En Windows: `winget install Gyan.FFmpeg` o descargando desde ffmpeg.org

---

## Instalación

1. Clona el repositorio e ingresa al directorio:
   ```bash
   git clone <url-del-repositorio>
   cd recauda-propi
   ```

2. Instala las dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```

---

## Uso

### 1. Aplicación Web

Inicia el servidor web con Uvicorn:

```bash
python3 app.py
```
O directamente con uvicorn:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Abre tu navegador en:
```
http://localhost:8000
```

1. Pega el enlace del video de YouTube en el campo de texto.
2. Selecciona la calidad de audio deseada (128, 192, 256 o 320 kbps).
3. Haz clic en **Convertir y Descargar MP3**.
4. El archivo MP3 se descargará y guardará automáticamente en tu dispositivo.

---

### 2. Línea de Comandos (CLI)

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
