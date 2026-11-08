# 🎵 Stahování hudby do MP3: návod pro úplné začátečníky (Windows)

Hudba se ukládá do složky **`E:\Hudba ai stahovani`** jako MP3 v kvalitě 320 kbps
i s obalem alba, interpretem a názvem.

---

## Instalace (3 kroky, jen jednou)

### Krok 1: Nainstaluj programy

1. Klikni na **Start**, napiš **PowerShell** a otevři ho.
2. Zkopíruj tenhle řádek, vlož ho do PowerShellu (pravým tlačítkem myši) a zmáčkni **Enter**:

```powershell
winget install -e --id Python.Python.3.13 ; winget install -e --id Gyan.FFmpeg ; winget install -e --id DenoLand.Deno
```

3. Když se něco zeptá (`Y/N`), napiš **Y** a Enter. Počkej, až to doběhne.

> Co se instaluje: **Python** (spouští skript), **FFmpeg** (převádí do MP3) a
> **Deno** (pomocník, kterého dnes YouTube vyžaduje).

### Krok 2: Nainstaluj stahovač yt-dlp

1. **Zavři PowerShell a otevři ho znovu.** Je to důležité, jinak nové programy nenajde.
2. Vlož tenhle řádek a zmáčkni Enter:

```powershell
py -m pip install -U "yt-dlp[default]"
```

### Krok 3: Ulož skript do složky `E:\Hudba ai stahovani`

1. Složka **`E:\Hudba ai stahovani`** už existuje (je to zároveň složka, kam se ukládá hudba).
2. Ulož do ní soubory **`downloader.py`** a **`stahni.bat`** z tohoto repozitáře
   (na GitHubu: zelené tlačítko **Code → Download ZIP**, rozbal a oba soubory přetáhni do `E:\Hudba ai stahovani`).

   > Když kód kopíruješ ručně do Poznámkového bloku: *Soubor → Uložit jako* →
   > Typ: **Všechny soubory**, Kódování: **UTF-8**, název `downloader.py`.

3. **První spuštění (test):** v PowerShellu napiš:

```powershell
py "E:\Hudba ai stahovani\downloader.py" "Queen - Bohemian Rhapsody"
```

Za chvíli najdeš MP3 ve složce `E:\Hudba ai stahovani`. 🎉

---

## Jak stahovat (3 způsoby)

**A) Příkaz v PowerShellu** (nejrychlejší, právě takový příkaz ti vygeneruje Claude):

```powershell
py "E:\Hudba ai stahovani\downloader.py" "Queen - Bohemian Rhapsody" "Eminem - Lose Yourself" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

- **Název písničky** → najde se na YouTube a stáhne se první výsledek.
- **Odkaz na video** → stáhne se to video.
- **Odkaz na playlist nebo album** → stáhne se celé, do vlastní podsložky, očíslované.

**B) Dvojklik na `E:\Hudba ai stahovani\stahni.bat`** → zeptá se tě. Napiš písničky (každou na nový řádek),
nakonec zmáčkni Enter na prázdném řádku.

**C) Seznam v textovém souboru:** napiš do `seznam.txt` jednu písničku nebo odkaz na řádek a:

```powershell
py "E:\Hudba ai stahovani\downloader.py" "E:\Hudba ai stahovani\seznam.txt"
```

(nebo přetáhni `seznam.txt` myší na ikonu `stahni.bat`).

Už stažené písničky se znovu nestahují (pamatuje si je soubor `_uz_stazeno.txt` ve složce s hudbou).

---

## Když něco nefunguje

| Problém | Řešení |
|---|---|
| `py` nebo `ffmpeg` „není rozpoznán“ | Zavři a znovu otevři PowerShell. Když to nepomůže, restartuj PC. |
| Přestalo to stahovat / chyby z YouTube | Aktualizuj stahovač: `py -m pip install -U "yt-dlp[default]"` (YouTube se často mění) |
| „Sign in to confirm you're not a bot“ | Přihlas se na YouTube ve **Firefoxu**, otevři `E:\Hudba ai stahovani\downloader.py` v Poznámkovém bloku a změň `COOKIES_Z_PROHLIZECE = None` na `COOKIES_Z_PROHLIZECE = "firefox"`. |
| Stáhla se jiná verze písničky | Napiš přesnější název (např. přidej „official audio“) nebo použij přímo odkaz. |
| Chci jinou cílovou složku | V `downloader.py` změň řádek `OUTPUT_DIR = r"E:\Hudba ai stahovani"`. |

> Poznámka: stránky jako mp3juice nejsou potřeba. yt-dlp stahuje přímo z YouTube
> (a z dalších webů, např. SoundCloud nebo Bandcamp) a ve vyšší kvalitě.
> Stahuj jen obsah, ke kterému na to máš právo.

---

## Jak zadávat písničky Claudovi

Pošli Claudovi seznam písniček, alb nebo odkazů v jakékoli podobě a on ti vrátí **jediný hotový příkaz**:
zkopíruješ ho do PowerShellu a zmáčkneš Enter. Pravidlo je uložené v souboru `CLAUDE.md`
(pro Claude Code v tomto repozitáři). Pro běžný chat na claude.ai ho vlož do
*Settings → Profile → „What personal preferences should Claude consider…“* nebo do instrukcí projektu:

```text
Když ti pošlu seznam písniček, alb nebo odkazů na hudbu, odpověz JEDINÝM příkazem
pro PowerShell ve formátu:
py "E:\Hudba ai stahovani\downloader.py" "Interpret - Písnička" "https://odkaz" ...
Každá položka v uvozovkách, vše na jednom řádku. Názvy oprav na "Interpret - Název".
U celého alba použij "Interpret - Album full album", nebo odkaz na playlist, pokud ho mám.
Uvozovky uvnitř názvů odstraň. Žádné další vysvětlování, jen příkaz v bloku kódu.
```
