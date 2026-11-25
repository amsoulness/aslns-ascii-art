'use strict';
const $ = (id) => document.getElementById(id);
const video = $('video');
let artworks = [], selected;
const repository = 'https://github.com/amsoulness/aslns-ascii-art';

function status(message) { $('status').textContent = message; }
function reflectPlayback() {
  $('play').textContent = video.paused ? 'Play animation' : 'Pause';
  $('stage-play').hidden = !video.paused || Boolean(video.currentSrc);
}
function selectArtwork(artwork, play = false) {
  video.pause();
  video.removeAttribute('src');
  video.load();
  selected = artwork;
  video.poster = artwork.poster;
  video.setAttribute('aria-label', artwork.title + ' animation');
  $('art-title').textContent = artwork.title;
  $('art-description').textContent = artwork.description;
  $('art-meta').textContent = `${artwork.seconds}s LOOP · ${Math.max(0.1, artwork.bytes / 1048576).toFixed(1)} MB`;
  $('source').href = `${repository}/tree/main/${artwork.id}`;
  $('gif').href = `https://raw.githubusercontent.com/amsoulness/aslns-ascii-art/main/${artwork.id}/images/preview.gif`;
  document.querySelectorAll('.card').forEach(card => card.setAttribute('aria-pressed', String(card.dataset.id === artwork.id)));
  const url = new URL(location.href);
  url.searchParams.set('art', artwork.id);
  history.replaceState(null, '', url);
  status('Ready when you are. Tap play to start.');
  $('stage-play').hidden = false;
  reflectPlayback();
  if (play) start();
}
async function start() {
  if (!selected) return;
  if (!video.getAttribute('src')) video.src = selected.video;
  $('stage-play').hidden = true;
  status('Loading animation…');
  try { await video.play(); status('Playing · loops automatically'); }
  catch (error) {
    if (error.name === 'AbortError') return;
    status('Tap the video play control to start. You can also open the GIF.');
    $('stage-play').hidden = false;
  }
  reflectPlayback();
}
$('play').addEventListener('click', () => { if (video.paused) start(); else video.pause(); });
$('stage-play').addEventListener('click', start);
$('restart').addEventListener('click', () => { video.currentTime = 0; start(); });
$('fullscreen').addEventListener('click', async () => {
  try {
    if (video.requestFullscreen) await video.requestFullscreen();
    else if (video.webkitEnterFullscreen) { await start(); video.webkitEnterFullscreen(); }
    else status('Use the fullscreen control on the video, or rotate your phone.');
  } catch { status('Use the fullscreen control on the video.'); }
});
$('share').addEventListener('click', async () => {
  try {
    if (navigator.share) await navigator.share({ title: selected.title + ' · ASLNS', url: location.href });
    else if (navigator.clipboard) { await navigator.clipboard.writeText(location.href); status('Artwork link copied.'); }
    else status('Copy the address from your browser to share this artwork.');
  } catch (error) { if (error.name !== 'AbortError') status('Copy the address from your browser to share this artwork.'); }
});
video.addEventListener('play', () => { reflectPlayback(); status('Playing · loops automatically'); });
video.addEventListener('pause', () => { reflectPlayback(); if (video.currentTime > 0) status('Paused. Tap play to continue.'); });
video.addEventListener('error', () => { status('The video could not load. Try Open GIF or choose another artwork.'); $('stage-play').hidden = false; });
document.addEventListener('visibilitychange', () => { if (document.hidden) video.pause(); });
$('search').addEventListener('input', () => {
  const query = $('search').value.trim().toLocaleLowerCase();
  let count = 0;
  document.querySelectorAll('.card').forEach(card => {
    card.hidden = !card.dataset.search.includes(query);
    if (!card.hidden) count++;
  });
  $('result-count').textContent = `${count} artwork${count === 1 ? '' : 's'}`;
  $('empty').hidden = count > 0;
});

async function initialize() {
  try {
    const response = await fetch('artworks.json');
    if (!response.ok) throw new Error('Collection unavailable');
    artworks = await response.json();
    const fragment = document.createDocumentFragment();
    for (const artwork of artworks) {
      const card = document.createElement('button');
      card.type = 'button'; card.className = 'card';
      card.dataset.id = artwork.id;
      card.dataset.search = `${artwork.id} ${artwork.title} ${artwork.description}`.toLocaleLowerCase();
      card.setAttribute('aria-pressed', 'false');
      card.setAttribute('aria-label', `Play ${artwork.title}`);
      const imageWrap = document.createElement('div'); imageWrap.className = 'card-image';
      const image = document.createElement('img'); image.src = artwork.poster; image.alt = ''; image.loading = 'lazy'; image.width = 432; image.height = 384;
      const badge = document.createElement('span'); badge.className = 'badge'; badge.textContent = `${artwork.seconds}s loop`;
      imageWrap.append(image, badge);
      const copy = document.createElement('div'); copy.className = 'card-copy';
      const title = document.createElement('span'); title.className = 'card-title'; title.textContent = artwork.title;
      const description = document.createElement('span'); description.className = 'card-caption'; description.textContent = artwork.description;
      copy.append(title, description); card.append(imageWrap, copy);
      card.addEventListener('click', () => { selectArtwork(artwork, true); $('player').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }); });
      fragment.append(card);
    }
    $('gallery').append(fragment);
    for (const id of ['play', 'restart', 'fullscreen', 'share']) $(id).disabled = false;
    const requested = new URL(location.href).searchParams.get('art');
    selectArtwork(artworks.find(art => art.id === requested) || artworks[0]);
  } catch { status('The collection could not load. Refresh the page or open the GitHub collection.'); $('stage-play').hidden = true; }
}
initialize();
