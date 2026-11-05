#!/usr/bin/env python3
"""Command Line Interface for downloading YouTube videos as MP3 audio files."""

import argparse
import sys
import os
import converter


def build_parser() -> argparse.ArgumentParser:
    """Builds and returns the command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Convertidor de enlaces de YouTube a MP3 (extracción de audio).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("url", help="Enlace/URL del video de YouTube a convertir")
    parser.add_argument(
        "-o",
        "--output",
        default="./downloads",
        help="Carpeta o directorio de destino donde guardar el archivo MP3",
    )
    parser.add_argument(
        "-b",
        "--bitrate",
        choices=converter.VALID_BITRATES,
        default=converter.DEFAULT_BITRATE,
        help="Calidad de audio / Bitrate en kbps (128, 192, 256, 320)",
    )
    parser.add_argument(
        "-n",
        "--name",
        default=None,
        help="Nombre personalizado para el archivo generado (sin extensión)",
    )
    parser.add_argument(
        "-i",
        "--info-only",
        action="store_true",
        help="Solo mostrar metadatos e información del video sin descargar",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    url = args.url.strip()
    if not url:
        print("Error: Debe proporcionar un enlace válido de YouTube.", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Obteniendo información de: {url}")
    try:
        info = converter.get_video_info(url)
        print(f"[+] Título: {info['title']}")
        print(f"[+] Canal / Creador: {info['uploader']}")
        print(f"[+] Duración: {info['duration_formatted']}")

        if args.info_only:
            return

        print(f"[*] Extrayendo audio y convirtiendo a MP3 ({args.bitrate} kbps)...")
        res = converter.download_audio_as_mp3(
            url=url,
            output_dir=os.path.abspath(args.output),
            bitrate=args.bitrate,
            custom_filename=args.name,
        )

        size_mb = res["filesize"] / (1024 * 1024)
        print("\n" + "=" * 50)
        print("[✓] ¡Conversión completada con éxito!")
        print(f"[✓] Archivo: {res['filename']}")
        print(f"[✓] Ruta: {res['filepath']}")
        print(f"[✓] Tamaño: {size_mb:.2f} MB")
        print("=" * 50)

    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
