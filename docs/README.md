# ASLNS mobile gallery

Public URL: https://amsoulness.github.io/aslns-ascii-art/

A buildless HTML/CSS/JavaScript gallery for all 16 artworks. No account,
server process, or Python installation is needed to watch.

## Deploy on GitHub Pages

The repository's Pages source is the `main` branch, `/docs` folder.
Pushing changes to this folder publishes the gallery. `.nojekyll` keeps
the static files intact. No external CDN or JavaScript dependencies are used.

## Local preview

From the repository root:

```sh
python -m http.server 8765 --directory docs
```

Open http://localhost:8765 in a browser. Opening index.html as a local file
does not work because the player fetches artworks.json.

To regenerate media, see [PREVIEWS.md](../PREVIEWS.md).
Direct links use `?art=ROSE`, `?art=DAISY`, or any artwork folder name.

## Playback and accessibility

Tap an artwork or Play animation to start. Only the selected video loads.
Native video controls provide seeking and playback. The page also supports
pause/resume, restart, fullscreen (where supported), sharing, and search.
Keyboard focus, labelled controls, reduced-motion preferences and narrow phone
screens are supported. Playback stops when the tab is hidden. Video playback
requires a browser with H.264 support; Open GIF is available as a fallback.

## License

Original attribution and restrictions apply to the exported videos and posters.
See [LICENSE.txt](../LICENSE.txt) and the artwork-specific licenses.
