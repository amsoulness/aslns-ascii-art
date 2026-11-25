"""Export the existing renderer captures to phone-compatible H.264 videos.
Run from the repository root: python tools/export_mobile.py
Requires requirements-preview.txt. No artwork code is changed.
"""
import json
from pathlib import Path
import subprocess
import imageio_ffmpeg
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
WORKS = [
    ('BUTTERFLY-HEART', 'Butterfly heart', 'Two butterflies trace a sparkling heart together.', '03_finished.png'),
    ('BLOOMING-BOUQUET', 'Blooming bouquet', 'Five little flowers, tied with a pink ribbon.', '03_finished.png'),
    ('MOONLIGHT-CATS', 'Moonlight cats', 'Two cats sit together under a heart-shaped moon.', '03_finished.png'),
    ('NAME-HEART', 'A heart for you', 'Type any name into a glowing, beating heart.', '03_finished.png'),
    ('DAISY', 'Daisy', 'White petals open around a golden heart.', '03_bloom.png'),
    ('ROSE', 'In bloom', 'A spark grows into a rose, petal by petal.', '03_bloom.png'),
    ('BUTTERFLY', 'Butterfly', 'A crack in the glass. A world of wings.', '03_flight.png'),
    ('GOLDFISH', 'Goldfish', 'A shimmering school swims through the dark.', '02_hello.png'),
    ('GNOME', 'Gnome', 'A tiny visitor with a lantern and a shy hello.', '02_hello.png'),
    ('FLIP-PHONE', 'Incoming call', 'A familiar flip phone lights up and opens.', '03_calling.png'),
    ('GOOD-LUCK', 'Good luck', 'A four-leaf clover written in many languages.', '03_front.png'),
    ('SKIPPED-A-BEAT', 'Skipped a beat', 'A bright heart pulses through a field of letters.', '03_heart.png'),
    ('I-LOVE-YOU', 'I love you', 'A turning heart made of words in 114 languages.', '03_front.png'),
    ('SNOWMAN', "Don't melt", 'A little snowman gathers, stands, and begins to melt.', '02_standing.png'),
    ('NIGHT-TIDE', 'Night tide', 'Waves break into a glittering sea of characters.', '02_breaking.png'),
    ('BLACK-HOLE', 'Black hole', 'A glowing disk curves around a dark center.', '03_flow.png'),
    ('CAT-KNIGHT', 'Cat knight', 'A tiny knight, a flowing cape, and a very big sword.', '03_knight.png'),
    ('MONEY-RAIN', 'Money rain', 'Letter-drawn notes tumble through the air.', '02_rain.png'),
    ('BIRTHDAY-CAKE', 'Happy birthday', 'A cake takes shape and a candle comes to life.', '03_happy_birthday.png'),
    ('DIAMOND-RING', 'Will you', 'A diamond ring forms from dust and catches the light.', '02_finished.png'),
]

if __name__ == '__main__':
    media = ROOT / 'docs/media'
    media.mkdir(parents=True, exist_ok=True)
    reports = {item['work']: item for item in json.loads((ROOT / 'PREVIEW_CAPTURE.json').read_text())}
    entries = []
    for key, title, description, poster in WORKS:
        slug = key.lower()
        output = media / (slug + '.mp4')
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error',
            '-y', '-ignore_loop', '1', '-i', str(ROOT / key / 'images/preview.gif'),
            '-an', '-vf', 'fps=10', '-c:v', 'libx264', '-profile:v', 'baseline',
            '-level', '3.0', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart',
            str(output)], check=True)
        with Image.open(ROOT / key / 'images' / poster) as image:
            image.convert('RGB').resize((432, 384), Image.Resampling.LANCZOS).save(
                media / (slug + '.webp'), quality=88)
        entries.append({'id': key, 'title': title, 'description': description,
                        'video': f'media/{slug}.mp4', 'poster': f'media/{slug}.webp',
                        'seconds': reports[key]['loop_seconds'], 'bytes': output.stat().st_size})
        print('Exported', key, output.stat().st_size, 'bytes', flush=True)
    (ROOT / 'docs/artworks.json').write_text(json.dumps(entries, indent=2) + '\n', encoding='utf-8')
