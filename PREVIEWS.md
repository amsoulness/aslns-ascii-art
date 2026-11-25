# Preview generation and verification

All 20 artworks were run with their supplied main window renderer on
26 November 2026, using Python 3.12 on Windows and an offscreen SDL display.
The capture report in [PREVIEW_CAPTURE.json](PREVIEW_CAPTURE.json) records
the three screenshot timestamps, loop length, render samples and GIF frame count.

## Reproduce

```sh
python -m pip install -r requirements-preview.txt
python tools/capture_previews.py
```

Pass one or more artwork directory names to regenerate a subset:

```sh
python tools/capture_previews.py ROSE DAISY
```

The runner executes each artwork's main window loop. An in-memory AST transform
advances animation time in 0.1-second steps, and the frame clock does not wait.
For Butterfly and Goldfish, the same frame functions run synchronously instead
of using their interactive worker pool. The artwork source files are unchanged.
This verifies the rendered animation, not the machine's real-time frame rate.

Three screenshots per work preserve the full 1080 Ã— 960 canvas, attribution,
status text and glow. The GIF samples every other rendered frame at 432 Ã— 384,
5 fps, with a 96-color palette and an infinite loop. Screenshots keep their
existing names so artwork READMEs and the main collection table continue to work.
System font availability can affect exact glyph appearance on other computers.

## Dependencies

Per-artwork requirements contain only packages imported by the supplied playback
or rendering script. The root requirements cover every artwork, including Pillow
for Birthday Cake and preview exports. Playwright is only required by the optional
multilingual sprite generators; the already-generated sprites are bundled.

Verified package versions:

- numpy: 2.5.5
- pygame-ce: 2.5.8
- opencv-python: 5.1.0.95
- Pillow: 13.0.0

## Licenses

The existing copyright, personal-use permissions and restrictions are retained.
License formatting and scope notes now identify documentation and generated previews.
Source photos identified in Cat Knight and Skipped a Beat remain the property
of their respective creators; their original photos are not included.

## Mobile video exports

After regenerating the GIF captures, run:

```sh
python -m pip install -r requirements-preview.txt
python tools/export_mobile.py
```

This creates 20 MP4 videos (H.264 Baseline, YUV420p, fast-start metadata),
small WebP posters, and the gallery manifest in docs/. Videos are derived from
the captured GIFs; repeated frames at 10 fps preserve their 5 fps source motion.
They contain no audio and are downloaded only when a visitor chooses to play.
The responsive player provides native video controls, restart, fullscreen,
search, and shareable artwork URLs. It pauses when its tab is hidden.
This is playback of rendered output, not browser execution of Python.

Name Heart is an exception to video playback: its mobile player renders a live
canvas heart made from the typed name. The generic MP4/GIF remains an archived
preview; the interactive desktop application and browser canvas use the same
scanline layout approach to repeat whole names across the heart.
