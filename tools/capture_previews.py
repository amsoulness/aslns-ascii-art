"""Run each artwork's window renderer and capture reproducible repository previews.

Install requirements-preview.txt, then run: python tools/capture_previews.py [WORK ...]
Uses SDL's offscreen display. Only the in-memory timing is adapted: 10 animation
samples per second, saved as a 5 fps GIF. Artwork source files are not modified.
"""
import ast
import inspect
import json
import os
from pathlib import Path
import sys

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import pygame
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
TIMES = {
    'BIRTHDAY-CAKE': (2, 6, 12), 'BLACK-HOLE': (1.5, 5, 14),
    'BUTTERFLY': (1.4, 3, 12), 'CAT-KNIGHT': (1, 8, 16),
    'DAISY': (3, 10, 16), 'DIAMOND-RING': (1.5, 6, 13),
    'FLIP-PHONE': (4, 5.6, 12), 'GNOME': (3, 8, 13),
    'GOLDFISH': (3, 8, 13), 'GOOD-LUCK': (1.5, 5, 10),
    'I-LOVE-YOU': (1.5, 6, 10), 'MONEY-RAIN': (3.5, 7, 15),
    'NIGHT-TIDE': (2, 8, 14), 'ROSE': (3, 6, 16),
    'SKIPPED-A-BEAT': (2, 6, 12), 'SNOWMAN': (0.9, 7, 20.9),
}


class Timing(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        if (isinstance(node.func, ast.Name) and node.func.id == 'min'
                and node.args and isinstance(node.args[0], ast.Name)
                and node.args[0].id == 'dt'):
            return ast.copy_location(ast.Constant(0.1), node)
        return node


class Finished(Exception):
    pass


def capture(name):
    folder = ROOT / name
    source = next(folder.glob('*.py'))
    tree = ast.fix_missing_locations(Timing().visit(ast.parse(source.read_text(encoding='utf-8-sig'))))
    namespace = {'__file__': str(source), '__name__': 'preview_' + name.replace('-', '_')}
    exec(compile(tree, str(source), 'exec'), namespace)
    loop = float(namespace['LOOP'])
    screenshots = sorted((folder / 'images').glob('0*.png'))
    assert len(screenshots) == 3, (name, screenshots)
    targets = dict(zip(screenshots, TIMES[name]))
    images, saved, seen = [], {}, set()
    original_flip, original_clock = pygame.display.flip, pygame.time.Clock

    class Clock:
        def tick(self, fps=0):
            return 100

    # The interactive app computes ahead with worker processes. For capture,
    # evaluate the identical frame function synchronously at fixed timestamps.
    if 'Frames' in namespace:
        class Frames:
            def __init__(self): self.restart()
            def restart(self): self.k = 0
            def close(self): pass
            def next(self):
                t = self.k / 10
                self.k += 1
                return t, namespace['render'](t)
        namespace['Frames'] = Frames

    def flip():
        state = inspect.currentframe().f_back.f_locals
        t = float(state['t'])
        key = round(t * 10)
        if key in seen or t >= loop - 0.099:
            raise Finished
        seen.add(key)
        screen = state['screen']
        image = Image.frombytes('RGB', screen.get_size(), pygame.image.tobytes(screen, 'RGB'))
        for path, target in targets.items():
            if path not in saved and t + 0.001 >= target:
                image.save(path, optimize=True)
                saved[path] = round(t, 2)
        if key % 2 == 0:
            images.append(image.resize((432, 384), Image.Resampling.LANCZOS).quantize(colors=96))

    pygame.display.flip, pygame.time.Clock = flip, Clock
    try:
        namespace['main']()
    except Finished:
        pass
    finally:
        pygame.display.flip, pygame.time.Clock = original_flip, original_clock
        pygame.quit()
    assert len(saved) == 3 and len(images) > 40, (name, saved, len(images))
    images[0].save(folder / 'images/preview.gif', save_all=True,
                   append_images=images[1:], duration=200, loop=0, optimize=True)
    report = {'work': name, 'loop_seconds': loop, 'screenshots':
              {p.name: t for p, t in saved.items()}, 'gif_frames': len(images),
              'gif_size': [432, 384], 'gif_fps': 5, 'render_samples': len(seen)}
    print(json.dumps(report), flush=True)
    return report


if __name__ == '__main__':
    names = sys.argv[1:] or sorted(TIMES)
    results = [capture(name) for name in names]
    output = ROOT / 'PREVIEW_CAPTURE.json'
    previous = json.loads(output.read_text()) if output.exists() else []
    updated = {item['work']: item for item in previous + results}
    output.write_text(json.dumps(list(updated.values()), indent=2) + '\n', encoding='utf-8')
