# SMB MX - Cápsula de productos (ES)

(Dawniej "Píldora"; stary adres /p/pildora/ przekierowuje 301 na /p/capsula/.)

Generator strony slajdów (telefon + komputer) i PDF-ów.

## Aktualizacja
1. Edytuj teksty w `build.py` (słownik `CONTENT`) lub zdjęcia w `photos/`.
2. `python3 build.py es && python3 render.py es && python3 og.py && python3 web.py`
   (wymaga Python 3, Playwright + Chromium, Pillow).
3. Wynik: `site/p/capsula/` (strona) i `out/*.pdf` (PDF-y; kopia w `dist/`).
4. `git commit` + `git push`, potem w cPanel: Git Version Control > Manage > Deploy HEAD Commit.

Adres: https://simplemadeblinds.mx/p/capsula/ (noindex, bez linku z serwisu).
Deploy: `.cpanel.yml` kopiuje `site/p/capsula` (oraz przekierowanie `site/p/pildora`) do `public_html/simplemadeblinds.mx/p/`.
Marka 3.0 (Navy #1A355C, Merlot #601B22, Encode Sans). Treści: bez cen, bez nieudokumentowanych parametrów.
