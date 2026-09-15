# Empire Corporation — strona firmowa

Strona firmy **Empire Corporation Paweł Głowacz** (NIP 6642140734): https://empirecorporation.eu/ (hosting MyDevil).

## Struktura

- `index.html`, `en.html`, `privacy.html`, `404.html` — strony statyczne
- `assets/` — style, fonty IBM Plex, grafiki
- `blog-src/posts/<slug>.html` — wpisy: blok `<!--META {json} META-->` + treść HTML
- `blog-src/schedule.json` — data publikacji każdego wpisu
- `tools/build_site.py` — buduje stronę i blog (sitemap, RSS, llms.txt, IndexNow)
- `tools/make_og.py` — generuje obrazki podglądu wpisów (`assets/img/blog/`)
- `tools/deploy.sh` — wysyła zatwierdzony kod na serwer i przebudowuje stronę

## Publikacja wpisów

Na serwerze cron uruchamia codziennie o 6:10 `build_site.py`. Wpis pojawia się na stronie
w pierwszym przebiegu w dniu z `schedule.json` lub później. Nowe adresy są zgłaszane do IndexNow.

Nowy wpis: dodaj plik do `blog-src/posts/`, datę do `schedule.json`, uruchom
`python tools/make_og.py`, zrób commit i `sh tools/deploy.sh`.

Podgląd lokalny: `python tools/build_site.py --out ../podglad --today 2026-12-31`.
