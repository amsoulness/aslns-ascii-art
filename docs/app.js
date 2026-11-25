'use strict';
const $ = (id) => document.getElementById(id);
const video = $('video');
let artworks = [], selected;
let chosenName = (new URL(location.href).searchParams.get('name') || '').slice(0, 24);
let heartPlaying = false, heartTime = 0, previousFrame = 0;
const nameCanvas = $('name-canvas');
const nameContext = nameCanvas.getContext('2d');
function drawNameHeart() {
  const ctx = nameContext;
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 1080, 960);
  const name = chosenName.trim() || 'Your name';
  const size = Math.max(16, Math.min(24, 550 / [...name].length));
  ctx.font = `${size}px Consolas,monospace`;
  ctx.textBaseline = 'top';
  const width = ctx.measureText(name + ' ').width;
  const pulse = 1 + 0.035 * Math.sin(heartTime * 3.6);
  const points = Array.from({length:360}, (_, i) => {
    const a = i / 360 * Math.PI * 2;
    return [540 + 22 * pulse * 16 * Math.sin(a) ** 3,
      400 - 22 * pulse * (13*Math.cos(a)-5*Math.cos(2*a)-2*Math.cos(3*a)-Math.cos(4*a))];
  });
  let row = 0;
  for (let y = 30; y < 850; y += size * 1.2, row++) {
    const crossings = [];
    points.forEach(([x0,y0],i) => {
      const [x1,y1] = points[(i+1)%points.length];
      const scan = y + size / 2;
      if ((y0 > scan) !== (y1 > scan)) crossings.push(x0 + (scan-y0)*(x1-x0)/(y1-y0));
    });
    crossings.sort((a,b) => a-b);
    for (let i=0; i<crossings.length; i+=2) {
      const left=crossings[i], right=crossings[i+1];
      const count=Math.floor((right-left-10)/width);
      if (count < 1) continue;
      const text=Array(count).fill(name).join(' ');
      ctx.fillStyle=`hsl(${335 + 10*Math.sin(row*.15+heartTime)},90%,${72+8*Math.sin(row*.2+heartTime)**2}%)`;
      ctx.shadowColor='#ff6cab'; ctx.shadowBlur=5;
      ctx.fillText(text,(left+right-ctx.measureText(text).width)/2,y);
    }
  }
  ctx.shadowBlur=0;
  nameCanvas.setAttribute('aria-label', `Heart made from the name ${name}`);
}
function animateNameHeart(timestamp) {
  if (heartPlaying) {
    heartTime += Math.min((timestamp-previousFrame)/1000,0.05);
    drawNameHeart();
  }
  previousFrame=timestamp;
  requestAnimationFrame(animateNameHeart);
}
requestAnimationFrame(animateNameHeart);
const repository = 'https://github.com/amsoulness/aslns-ascii-art';

function status(message) { $('status').textContent = message; }
function reflectPlayback() {
  if (selected?.id === 'NAME-HEART') {
    $('play').textContent = heartPlaying ? 'Pause' : 'Play animation';
    $('stage-play').hidden = heartPlaying;
    return;
  }
  $('play').textContent = video.paused ? 'Play animation' : 'Pause';
  $('stage-play').hidden = !video.paused || Boolean(video.currentSrc);
}
function selectArtwork(artwork, play = false) {
  heartPlaying = false; heartTime = 0;
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
  const editable = artwork.id === 'NAME-HEART';
  if (editable) $('art-meta').textContent = 'YOUR NAME · A LIVING HEART';
  document.querySelector('.playback-note').textContent = editable
    ? 'The letters of your name form the whole heart. Change the name, then share it.'
    : 'Playback of the rendered Python artwork. Soundless, looping, and ready for your phone.';
  $('name-editor').hidden = !editable;
  $('personal-name').hidden = true;
  nameCanvas.hidden = !editable;
  video.hidden = editable;
  if (editable) drawNameHeart();
  video.parentElement.classList.toggle('has-name', editable);
  $('name-input').value = chosenName;
  $('personal-name').textContent = chosenName || 'Your name';
  if (editable && chosenName) url.searchParams.set('name', chosenName);
  else url.searchParams.delete('name');
  history.replaceState(null, '', url);
  status('Ready when you are. Tap play to start.');
  $('stage-play').hidden = false;
  reflectPlayback();
  if (play) start();
}
async function start() {
  if (!selected) return;
  if (selected.id === 'NAME-HEART') {
    heartPlaying = true; reflectPlayback(); status('Playing · your name forms the heart');
    return;
  }
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
$('play').addEventListener('click', () => {
  if (selected?.id === 'NAME-HEART' && heartPlaying) {
    heartPlaying = false; reflectPlayback(); status('Paused. Tap play to continue.');
  } else if (video.paused) start(); else video.pause();
});
$('stage-play').addEventListener('click', start);
$('name-input').addEventListener('input', () => {
  chosenName = $('name-input').value.slice(0, 24);
  $('personal-name').textContent = chosenName || 'Your name';
  drawNameHeart();
  const url = new URL(location.href);
  if (chosenName) url.searchParams.set('name', chosenName);
  else url.searchParams.delete('name');
  history.replaceState(null, '', url);
});
$('restart').addEventListener('click', () => { heartTime=0; video.currentTime = 0; start(); });
$('fullscreen').addEventListener('click', async () => {
  try {
    if (selected?.id === 'NAME-HEART') {
      if (video.parentElement.requestFullscreen) await video.parentElement.requestFullscreen();
      else status('Rotate your phone for a larger heart; your name stays visible here.');
      return;
    }
    if (video.requestFullscreen) await video.requestFullscreen();
    else if (video.webkitEnterFullscreen) { await start(); video.webkitEnterFullscreen(); }
    else status('Use the fullscreen control on the video, or rotate your phone.');
  } catch { status('Use the fullscreen control on the video.'); }
});
function positionPersonalName() {
  const box = video.getBoundingClientRect();
  const stage = video.parentElement.getBoundingClientRect();
  const height = Math.min(box.height, box.width / 1.125);
  $('personal-name').style.top = `${box.top - stage.top + box.height / 2 - height * 0.07}px`;
}
new ResizeObserver(positionPersonalName).observe(video.parentElement);
document.addEventListener('fullscreenchange', positionPersonalName);
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
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { video.pause(); heartPlaying=false; reflectPlayback(); }
});
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
    const response = await fetch('artworks.json?v=20261126-romantic-heart', { cache: 'no-store' });
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
