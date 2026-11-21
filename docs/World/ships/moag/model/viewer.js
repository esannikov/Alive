/* Local-only model-viewer runtime and Draco decoder; no CDN requests. */
const viewer = document.querySelector('#station-model');
const stage = document.querySelector('#model-stage');
const cover = document.querySelector('#model-cover');
const start = document.querySelector('#load-model');
const status = document.querySelector('#model-load-state');
const message = document.querySelector('#load-message');
const progress = document.querySelector('#model-progress');
const retry = document.querySelector('#retry-model');
const rotate = document.querySelector('#rotate-model');
const fullscreen = document.querySelector('#model-fullscreen');
const controls = [...document.querySelectorAll('#model-toolbar button')];
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const presets = {
  overview: {orbit:'-35deg 64deg 108%', target:'0m 50m 0m'},
  top: {orbit:'-35deg 3deg 112%', target:'0m 20m 0m'},
  bottom: {orbit:'-35deg 122deg 110%', target:'0m -30m 0m'},
  spire: {orbit:'-35deg 70deg 330m', target:'0m 252m 0m'},
  rim: {orbit:'38deg 63deg 145m', target:'308m 60m 401m'}
};
let phase = 'idle';
let attempts = 0;
let watchdog;
let milestone = -1;
let runtimePromise;

function stopRotation() {
  viewer.autoRotate = false;
  rotate.setAttribute('aria-pressed', 'false');
}
function failure(text) {
  phase = 'error';
  stage.removeAttribute('aria-busy');
  clearTimeout(watchdog);
  stopRotation();
  controls.forEach(button => { button.disabled = true; });
  cover.hidden = false;
  start.hidden = true;
  document.querySelector('#model-size').hidden = true;
  status.hidden = false;
  progress.hidden = true;
  message.textContent = text;
  retry.hidden = false;
}
async function load() {
  if (phase === 'loading' || phase === 'ready') return;
  phase = 'loading'; attempts += 1; milestone = -1;
  start.hidden = true; retry.hidden = true; status.hidden = false; progress.hidden = false;
  document.querySelector('#model-size').hidden = true;
  message.textContent = 'Загружаем модель…'; progress.value = 0;
  stage.setAttribute('aria-busy', 'true');
  clearTimeout(watchdog);
  watchdog = setTimeout(() => failure('Загрузка занимает слишком много времени. Проверьте соединение и попробуйте снова.'), 90000);
  try {
    runtimePromise ||= import('../../../vendor/model-viewer/model-viewer-4.1.0.min.js').catch(error => { runtimePromise = null; throw error; });
    const {ModelViewerElement} = await runtimePromise;
    ModelViewerElement.dracoDecoderLocation = new URL('../../../vendor/draco/', import.meta.url).href;
    viewer.interpolationDecay = reducedMotion.matches ? 0 : 70;
    viewer.rotationPerSecond = '9deg';
    viewer.src = new URL('moag041-v05.glb' + (attempts > 1 ? '?retry=' + attempts : ''), import.meta.url).href;
  } catch (_) {
    failure('Не удалось запустить 3D-просмотр. Попробуйте снова или откройте страницу в браузере с поддержкой WebGL.');
  }
}
viewer.addEventListener('progress', event => {
  if (phase !== 'loading') return;
  const value = Math.round(event.detail.totalProgress * 100);
  progress.value = value;
  const step = Math.floor(value / 25);
  if (step !== milestone) { milestone = step; message.textContent = value >= 100 ? 'Подготавливаем изображение…' : `Загружаем модель… ${value}%`; }
});
viewer.addEventListener('load', () => {
  clearTimeout(watchdog); phase = 'ready';
  cover.hidden = true; status.hidden = true; stage.removeAttribute('aria-busy');
  controls.forEach(button => { button.disabled = false; });
  fullscreen.hidden = !document.fullscreenEnabled;
  viewer.cameraTarget = presets.overview.target;
  viewer.cameraOrbit = presets.overview.orbit;
  viewer.jumpCameraToGoal();
  // Focus the pinned component's keyboard surface, not an extra host tab stop.
  viewer.shadowRoot.querySelector('.userInput')?.focus({preventScroll:true});
});
viewer.addEventListener('error', () => { stage.removeAttribute('aria-busy'); failure('Модель не загрузилась. Проверьте соединение или попробуйте другой браузер.'); });
viewer.addEventListener('camera-change', event => {
  if (event.detail.source !== 'user-interaction') return;
  document.querySelectorAll('[data-view]').forEach(button => button.setAttribute('aria-pressed', 'false'));
});
start.addEventListener('click', load);
retry.addEventListener('click', () => {
  // A failed Draco/WASM initialization is cached by the pinned runtime.
  // Reload its module state, then resume this explicitly requested load.
  const destination = new URL(location.href);
  destination.searchParams.set('load3d', '1');
  location.replace(destination);
});
document.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => {
  stopRotation(); viewer.resetTurntableRotation(0);
  const preset = presets[button.dataset.view];
  viewer.cameraTarget = preset.target; viewer.cameraOrbit = preset.orbit;
  if (reducedMotion.matches) viewer.jumpCameraToGoal();
  document.querySelectorAll('[data-view]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
}));
function zoom(factor) {
  const orbit = viewer.getCameraOrbit();
  viewer.cameraOrbit = `${orbit.theta}rad ${orbit.phi}rad ${Math.max(30, Math.min(4000, orbit.radius * factor))}m`;
}
document.querySelector('#zoom-in').addEventListener('click', () => zoom(.8));
document.querySelector('#zoom-out').addEventListener('click', () => zoom(1.25));
rotate.addEventListener('click', () => { viewer.autoRotate = !viewer.autoRotate; rotate.setAttribute('aria-pressed', String(viewer.autoRotate)); });
reducedMotion.addEventListener('change', () => { viewer.interpolationDecay = reducedMotion.matches ? 0 : 70; if (reducedMotion.matches) stopRotation(); });
document.addEventListener('visibilitychange', () => { if (document.hidden) stopRotation(); });
fullscreen.addEventListener('click', async () => {
  try { if (document.fullscreenElement) await document.exitFullscreen(); else await stage.requestFullscreen(); }
  catch (_) { fullscreen.hidden = true; }
});
document.addEventListener('fullscreenchange', () => { fullscreen.textContent = document.fullscreenElement ? 'Выйти из полного экрана' : 'На весь экран'; });

const resume = new URL(location.href);
if (resume.searchParams.get('load3d') === '1') {
  resume.searchParams.delete('load3d');
  history.replaceState(history.state, '', resume);
  load();
}
