# ASLNS · ASCII Code Art

ASLNS is a creative coding artist who writes artworks in Python.
Every piece is drawn only with letters, numbers and symbols.

This repository is an archive of the works and a technical portfolio:
what each piece is, why it was made, and which techniques shaped it.

## Watch on your phone

**[Open the mobile gallery](https://amsoulness.github.io/aslns-ascii-art/)**

Choose any of the 16 artworks and tap **Play animation**. Works in a modern
phone, tablet, or desktop browser without installing Python. Includes pause,
restart, fullscreen, search, and shareable links to individual artworks.
Videos show the rendered output of the Python animations; use the source code
to run the original interactive programs on a computer.

## Works

| | Work | Year | Source code | Watch on mobile |
|---|---|---|---|---|
| ![](BUTTERFLY/images/03_flight.png) | [BUTTERFLY](BUTTERFLY/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=BUTTERFLY) |
| ![](GOLDFISH/images/02_hello.png) | [GOLDFISH](GOLDFISH/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=GOLDFISH) |
| ![](GNOME/images/02_hello.png) | [GNOME](GNOME/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=GNOME) |
| ![](FLIP-PHONE/images/03_calling.png) | [FLIP PHONE (Incoming Call)](FLIP-PHONE/) | 2026 | full code, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=FLIP-PHONE) |
| ![](GOOD-LUCK/images/03_front.png) | [GOOD LUCK (Four-Leaf Clover)](GOOD-LUCK/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=GOOD-LUCK) |
| ![](SKIPPED-A-BEAT/images/03_heart.png) | [SKIPPED A BEAT](SKIPPED-A-BEAT/) | 2026 | full code, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=SKIPPED-A-BEAT) |
| ![](I-LOVE-YOU/images/03_front.png) | [I LOVE YOU](I-LOVE-YOU/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=I-LOVE-YOU) |
| ![](SNOWMAN/images/02_standing.png) | [DON'T MELT (Snowman)](SNOWMAN/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=SNOWMAN) |
| ![](NIGHT-TIDE/images/02_breaking.png) | [NIGHT TIDE](NIGHT-TIDE/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=NIGHT-TIDE) |
| ![](BLACK-HOLE/images/03_flow.png) | [BLACK HOLE](BLACK-HOLE/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=BLACK-HOLE) |
| ![](CAT-KNIGHT/images/03_knight.png) | [CAT KNIGHT](CAT-KNIGHT/) | 2026 | full code, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=CAT-KNIGHT) |
| ![](MONEY-RAIN/images/02_rain.png) | [MONEY RAIN](MONEY-RAIN/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=MONEY-RAIN) |
| ![](BIRTHDAY-CAKE/images/03_happy_birthday.png) | [HAPPY BIRTHDAY (Birthday Cake)](BIRTHDAY-CAKE/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=BIRTHDAY-CAKE) |
| ![](DAISY/images/03_bloom.png) | [DAISY](DAISY/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=DAISY) |
| ![](ROSE/images/03_bloom.png) | [IN BLOOM (Rose)](ROSE/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=ROSE) |
| ![](DIAMOND-RING/images/02_finished.png) | [WILL YOU (Diamond Ring)](DIAMOND-RING/) | 2026 | free, in this repository | [Play animation](https://amsoulness.github.io/aslns-ascii-art/?art=DIAMOND-RING) |

New works are added over time.

## Technology

Python · NumPy · pygame-ce · Pillow · OpenCV. No 3D software.

## Links

- Instagram: [@ft.aslns](https://instagram.com/ft.aslns)

---

## License

I share this code for you. Study it, change it, and use what you learn to make your own ASCII art.
Please don't repost this code, or a big part of it, as your own, don't post my artwork as your own,
don't sell it or use it commercially without my permission, and don't use it to train AI models.
A credit to @ft.aslns is always appreciated. If you see my code or artwork posted as someone else's, please report it and let me know on Instagram [@ft.aslns](https://instagram.com/ft.aslns).
Full terms in [LICENSE.txt](LICENSE.txt).

© 2026 ASLNS. All rights reserved.
Images and videos in this repository may not be reused without permission.

## Run the collection

Tested on Windows with Python 3.12. Download or clone the entire repository so
the bundled sprites and precomputed animation data stay beside their scripts.

```sh
python -m pip install -r requirements.txt
python DAISY/daisy.py
```

Replace `DAISY/daisy.py` with the desired artwork's script. Each artwork also
has its own minimal `requirements.txt`. Click its window, then use Space to
pause/resume, R to restart, S to save a screenshot, or Esc to close.

All 16 works have three freshly rendered full-canvas screenshots and a looping
preview. See [preview generation and verification](PREVIEWS.md).
