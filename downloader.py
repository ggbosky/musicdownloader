"""
Stahovač hudby z YouTube (a dalších webů) do MP3.

Použití (v terminálu / PowerShellu):
    py downloader.py "Queen - Bohemian Rhapsody"
    py downloader.py "pisnicka 1" "pisnicka 2" "https://www.youtube.com/watch?v=..."
    py downloader.py "https://www.youtube.com/playlist?list=..."
    py downloader.py seznam.txt            (textový soubor: jedna písnička/odkaz na řádek)
    py downloader.py                       (bez argumentů = zeptá se tě, co stáhnout)

Vše se ukládá jako MP3 (320 kbps) do složky OUTPUT_DIR níže.
"""

import os
import shutil
import sys

# ---------------------------------------------------------------------------
# NASTAVENÍ
# ---------------------------------------------------------------------------
OUTPUT_DIR = r"E:\Hudba ai stahovani"   # sem se ukládá hudba
MP3_KVALITA = "320"                     # kbps (nejvyšší kvalita MP3)
COOKIES_Z_PROHLIZECE = None             # jen když YouTube hlásí "nejsi robot?":
                                        # dej sem "firefox" (musíš tam být přihlášen)
# ---------------------------------------------------------------------------

try:
    import yt_dlp
except ImportError as e:
    print("CHYBA: Nepodařilo se načíst knihovnu yt-dlp.")
    print(f"Důvod: {e!r}")
    print(f"Python: {sys.executable}")
    print(f'Zkus:  & "{sys.executable}" -m pip install -U "yt-dlp[default]"')
    sys.exit(1)


def je_odkaz(text: str) -> bool:
    return text.lower().startswith(("http://", "https://", "www."))


def je_playlist(odkaz: str) -> bool:
    """Odkaz na celý playlist / album (ne na jedno video v playlistu)."""
    o = odkaz.lower()
    return ("/playlist" in o or "/browse/" in o or "/album" in o
            or "/sets/" in o or ("list=" in o and "v=" not in o))


def nacti_polozky(argumenty):
    """Z argumentů udělá seznam písniček/odkazů. Textové soubory rozbalí."""
    polozky = []
    for arg in argumenty:
        arg = arg.strip().strip('"').strip()
        if not arg:
            continue
        if os.path.isfile(arg) and arg.lower().endswith(".txt"):
            with open(arg, encoding="utf-8-sig") as f:
                for radek in f:
                    radek = radek.strip()
                    if radek and not radek.startswith("#"):
                        polozky.append(radek)
        else:
            polozky.append(arg)
    return polozky


def zeptej_se():
    print("Napiš názvy písniček nebo vlož odkazy (každý na nový řádek).")
    print("Až budeš hotov, zmáčkni Enter na prázdném řádku.\n")
    polozky = []
    while True:
        try:
            radek = input("> ").strip()
        except EOFError:
            break
        if not radek:
            break
        polozky.append(radek)
    return polozky


def zkontroluj_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("CHYBA: Nenašel jsem program ffmpeg (je potřeba pro převod do MP3).")
        print("Nainstaluj ho:  winget install -e --id Gyan.FFmpeg")
        print("Pak ZAVŘI a znovu OTEVŘI terminál a zkus to znovu.")
        sys.exit(1)


def nastaveni(slozka: str, playlist: bool) -> dict:
    if playlist:
        # Playlist/album -> vlastní podsložka, skladby očíslované
        sablona = "%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s"
    else:
        sablona = "%(title)s.%(ext)s"

    volby = {
        "format": "bestaudio/best",
        "paths": {"home": slozka},   # cílová složka
        "outtmpl": sablona,
        "noplaylist": True,          # odkaz na video v playlistu = jen to video
        "ignoreerrors": True,        # jedna chyba nezastaví celý playlist
        "windowsfilenames": True,    # názvy souborů bezpečné pro Windows
        "writethumbnail": True,      # obal alba do MP3
        "download_archive": os.path.join(slozka, "_uz_stazeno.txt"),  # nestahuje 2x to samé
        "quiet": False,
        "no_warnings": False,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3",
             "preferredquality": MP3_KVALITA},
            {"key": "FFmpegThumbnailsConvertor", "format": "jpg",
             "when": "before_dl"},
            {"key": "FFmpegMetadata", "add_metadata": True},
            {"key": "EmbedThumbnail"},
        ],
    }
    if COOKIES_Z_PROHLIZECE:
        volby["cookiesfrombrowser"] = (COOKIES_Z_PROHLIZECE,)
    return volby


def stahni(polozka: str, slozka: str) -> bool:
    if je_odkaz(polozka):
        cil = polozka if not polozka.lower().startswith("www.") else "https://" + polozka
        playlist = je_playlist(cil)
    else:
        cil = f"ytsearch1:{polozka}"   # vyhledá a vezme první (nejlepší) výsledek
        playlist = False

    try:
        with yt_dlp.YoutubeDL(nastaveni(slozka, playlist)) as ydl:
            return ydl.download([cil]) == 0
    except Exception as e:  # noqa: BLE001
        print(f"  !! Chyba: {e}")
        return False


def main():
    argumenty = sys.argv[1:]
    slozka = OUTPUT_DIR
    if len(argumenty) >= 2 and argumenty[0] in ("-o", "--slozka"):
        slozka, argumenty = argumenty[1], argumenty[2:]

    polozky = nacti_polozky(argumenty) if argumenty else zeptej_se()
    if not polozky:
        print("Nic k stažení.")
        return

    zkontroluj_ffmpeg()
    os.makedirs(slozka, exist_ok=True)

    print(f"\nUkládám do: {slozka}")
    print(f"Počet položek: {len(polozky)}\n")

    chyby = []
    for i, polozka in enumerate(polozky, 1):
        print(f"=== [{i}/{len(polozky)}] {polozka}")
        if not stahni(polozka, slozka):
            chyby.append(polozka)

    print("\n" + "=" * 50)
    print(f"HOTOVO. Úspěšně: {len(polozky) - len(chyby)} / {len(polozky)}")
    if chyby:
        print("Nepovedlo se:")
        for c in chyby:
            print(f"  - {c}")
        print('Tip: zkus aktualizovat yt-dlp:  py -m pip install -U "yt-dlp[default]"')
    print(f"Hudba je ve složce: {slozka}")


if __name__ == "__main__":
    main()
