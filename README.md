# musicdownloader

Jednoduchý stahovač hudby z YouTube (a dalších webů) do MP3 320 kbps
do složky `E:\Hudba ai stahovani`.

- **[NAVOD.md](NAVOD.md)**: instalace a použití krok za krokem (Windows)
- `downloader.py`: samotný skript (yt-dlp + ffmpeg)
- `stahni.bat`: spuštění dvojklikem / přetažením seznamu
- `seznam.txt`: ukázkový seznam písniček
- `CLAUDE.md`: pravidlo pro Clauda (seznam písniček → hotový příkaz)

```powershell
py "E:\Hudba ai stahovani\X\downloader.py" "Queen - Bohemian Rhapsody" "https://www.youtube.com/playlist?list=..."
```
