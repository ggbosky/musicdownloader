# Pravidla pro Clauda v tomto repozitáři

Uživatel používá `downloader.py` ke stahování hudby do MP3 do složky `E:\Hudba ai stahovani`
(Windows). Skript je uložený v `E:\Hudba ai stahovani\X\downloader.py`.

## Hlavní pravidlo: seznam písniček → jeden příkaz

Kdykoliv uživatel pošle seznam písniček, interpretů, alb nebo odkazů (v jakékoli podobě:
odrážky, čárky, zkopírovaný text, odkazy), odpověz **jediným příkazem pro PowerShell**
v bloku kódu, který stačí zkopírovat a zmáčknout Enter:

```powershell
py "E:\Hudba ai stahovani\X\downloader.py" "Interpret - Písnička" "Interpret 2 - Písnička 2" "https://www.youtube.com/watch?v=..."
```

Zásady:
- Vše na **jednom řádku**, každá položka ve **dvojitých uvozovkách**.
- Názvy normalizuj na `Interpret - Název` a oprav zjevné překlepy.
- Odkazy (YouTube, YouTube Music, SoundCloud, Bandcamp…) vlož beze změny.
- Celé album bez odkazu: `"Interpret - Album full album"` (nebo jednotlivé skladby alba, pokud je uživatel chce zvlášť).
- Z názvů odstraň znaky `"` a `` ` ``.
- Při velmi dlouhém seznamu (víc než ~40 položek) místo toho vygeneruj obsah pro `E:\Hudba ai stahovani\X\seznam.txt`
  (jedna položka na řádek) a příkaz `py "E:\Hudba ai stahovani\X\downloader.py" "E:\Hudba ai stahovani\X\seznam.txt"`.
- Žádné zbytečné vysvětlování, stačí příkaz (případně jedna krátká věta, pokud něco nebylo jasné).
