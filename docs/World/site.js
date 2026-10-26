/* Static ALIVE catalogue. Optional comments use the hosted Giscus service. */
(() => {
  'use strict';
  const data = window.ALIVE_WORLD;
  if (!data) return;
  const root = new URL(document.body.dataset.root || './', location.href);
  const url = p => new URL(p, root).href;
  const $ = s => document.querySelector(s);
  const byCode = Object.fromEntries(data.assets.map(a => [a.code, a]));
  const objects = Object.fromEntries(data.objects.map(o => [o.id, o]));
  const commentsSelectionKey = 'alive-world:comments:' + location.pathname.replace(/index\.html$/, '');
  if (data.comments?.enabled && new URL(location.href).searchParams.has('giscus')) {
    try {
      const saved = sessionStorage.getItem(commentsSelectionKey);
      if (saved && byCode[saved]?.object === document.body.dataset.object) {
        const returned = new URL(location.href); returned.hash = saved;
        history.replaceState(history.state, '', returned);
      }
    } catch (_) { /* Storage may be disabled; the gallery still works. */ }
  }
  document.documentElement.classList.add('js');
  let noticeTimer;
  function announce(message) {
    const el = $('#notice'); el.textContent = message; el.classList.add('visible');
    clearTimeout(noticeTimer); noticeTimer = setTimeout(() => el.classList.remove('visible'), 2400);
  }
  async function copy(text) {
    try { await navigator.clipboard.writeText(text); announce('Скопировано'); }
    catch (_) {
      const box = document.createElement('textarea'); box.value = text;
      box.style.cssText = 'position:fixed;left:-9999px;top:0'; document.body.append(box); box.select();
      const ok = document.execCommand('copy'); box.remove();
      announce(ok ? 'Скопировано' : 'Не удалось скопировать. Выделите код под изображением.');
    }
  }
  function closeMenu(restore=false) { const wasOpen=document.body.classList.contains('menu-open'); document.body.classList.remove('menu-open'); $('#menu-toggle')?.setAttribute('aria-expanded', 'false'); if(restore&&wasOpen) $('#menu-toggle')?.focus(); }
  $('#menu-toggle')?.addEventListener('click', () => {
    const on = document.body.classList.toggle('menu-open'); $('#menu-toggle').setAttribute('aria-expanded', String(on));
    if (on) $('#navigation a')?.focus();
  });
  document.addEventListener('click', e => {
    if (document.body.classList.contains('menu-open') && !e.target.closest('#navigation, #menu-toggle')) closeMenu();
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(true); });
  function expandGroup() {
    const id = location.hash.slice(1); const el = document.getElementById(id);
    if (el?.matches('.catalog-group')) { el.open = true; requestAnimationFrame(() => el.scrollIntoView({block:'start'})); }
  }
  if ($('.catalog-groups')) { expandGroup(); window.addEventListener('hashchange', expandGroup); }

  if (document.body.dataset.page === 'search') {
    const normalize = s => s.toLocaleLowerCase('ru').replaceAll('ё','е').replace(/[^\p{L}\p{N}]+/gu,' ').trim();
    const field = $('#global-search'); field.value = new URLSearchParams(location.search).get('q') || '';
    const series = Object.fromEntries(data.series.map(s => [s.id,s.title]));
    const entries = data.assets.filter(a=>!a.archived).map(a => ({title: `${objects[a.object].title} · ${a.title}`, meta:a.code,
      text: `${a.code} ${objects[a.object].title} ${a.title} ${series[a.series]} ${objects[a.object].variant_notes?.[a.code]||objects[a.object].variant_notes?.[a.series]||''} ${objects[a.object].kind==='ship'?'корабль станция внешний облик':'портрет внешность'} концепт`,
      note: `${series[a.series]} · поисковый вариант`, href:`${a.page||`characters/${a.object}/`}#${a.code}`,image:a.thumb,code:a.code}));
    data.tasks.forEach(t => entries.push({title:t.title,meta:'ProductionFlow',text:`${t.title} ${t.output}`,note:'Задание в плане',href:`../ProductionFlow/#task=${t.id}`}));
    const render = () => {
      const q = normalize(field.value); const parts = q.split(' ').filter(Boolean);
      const exact = entries.find(e => e.code === q);
      const hits = q ? exact ? [exact] : entries.filter(e => parts.every(p => normalize(e.text).includes(p))) : [];
      const list = $('#search-results'); list.replaceChildren();
      $('#search-summary').textContent = !q ? 'Введите имя, код или нужный материал.' : hits.length ? `Найдено: ${hits.length}` : 'Ничего не найдено. Попробуйте имя персонажа или код изображения.';
      hits.forEach(item => {
        const a = document.createElement('a'); a.className='search-result'; a.href=url(item.href);
        if(item.image){ const img=document.createElement('img'); img.src=url(item.image); img.alt=''; img.loading='lazy'; a.append(img); }
        const div=document.createElement('div'),meta=document.createElement('span'),h=document.createElement('h2'),p=document.createElement('p');
        meta.className='mono'; meta.textContent=item.meta; h.textContent=item.title; p.textContent=item.note;
        div.append(meta,h,p); a.append(div); list.append(a);
      });
      const next = new URL(location.href); if(field.value) next.searchParams.set('q',field.value); else next.searchParams.delete('q');
      history.replaceState(null,'',next);
    };
    field.addEventListener('input', render); $('.search-form').addEventListener('submit',e=>{e.preventDefault();render();}); render();
  }

  const objectId = document.body.dataset.object;
  if (!objectId) return;
  const assets = data.assets.filter(a=>a.object===objectId&&!a.archived);
  const galleryOrder=objects[objectId].gallery_order||[];
  const orderOf=a=>galleryOrder.includes(a.code)?galleryOrder.indexOf(a.code):galleryOrder.length;
  assets.sort((a,b)=>orderOf(a)-orderOf(b));
  const isShip=objects[objectId].kind==='ship';
  const select = $('#series-select'); let active = assets[0], comparing = false;
  const variantCount=n=>`${n} ${n%10===1&&n%100!==11?'вариант':[2,3,4].includes(n%10)&&![12,13,14].includes(n%100)?'варианта':'вариантов'}`;
  const visibleAssets = () => assets.filter(a=>isShip?a.series===active.series:select.value==='all'||a.series===select.value);
  const showSeries = () => {
    if(isShip){$('#gallery-count').textContent=`${new Set(assets.map(a=>a.series)).size} вариантов`;return;}
    document.querySelectorAll('.asset-tile').forEach(el=>{el.hidden=select.value!=='all'&&el.dataset.series!==select.value;});
    const count=visibleAssets().length; $('#gallery-count').textContent=objects[objectId].kind==='ship'?`${count} кадров`:variantCount(count);
  };
  const imageCache=new Map(), imageStates=new WeakMap();
  function prepareImage(a){
    const src=url(a.display||a.original);
    if(imageCache.has(src))return imageCache.get(src);
    const picture=new Image(); picture.decoding='async';
    const promise=new Promise((resolve,reject)=>{
      picture.onload=async()=>{try{if(picture.decode)await picture.decode();resolve(picture);}catch(error){imageCache.delete(src);reject(error);}};
      picture.onerror=()=>{imageCache.delete(src);reject(new Error('image-load'));};
    });
    imageCache.set(src,promise);picture.src=src;
    while(imageCache.size>8)imageCache.delete(imageCache.keys().next().value);
    return promise;
  }
  function prefetch(a){
    const connection=navigator.connection;
    if(!a||connection?.saveData||['slow-2g','2g'].includes(connection?.effectiveType))return;
    prepareImage(a).catch(()=>{});
  }
  async function loadPicture(img,a){
    let state=imageStates.get(img);
    if(!state){
      const stage=document.createElement('div');stage.className='media-stage';
      img.parentNode.insertBefore(stage,img);stage.append(img);
      const message=document.createElement('span');message.className='media-status';message.setAttribute('role','status');message.setAttribute('aria-live','polite');message.hidden=true;stage.append(message);
      state={sequence:0,stage,message,code:null,status:'idle'};imageStates.set(img,state);
    }
    const sequence=++state.sequence,src=url(a.display||a.original);state.code=a.code;
    if(img.complete&&img.naturalWidth>0&&img.currentSrc===src){state.status='ready';state.stage.dataset.state='ready';img.style.visibility='visible';img.removeAttribute('aria-busy');state.message.hidden=true;return true;}
    state.status='loading';state.stage.dataset.state='loading';
    img.style.visibility='hidden';img.setAttribute('aria-busy','true');
    state.message.textContent=`Загрузка ${a.code}…`;state.message.hidden=false;
    try{
      await prepareImage(a);
      if(state.sequence!==sequence)return false;
      img.src=src;img.alt=`${a.code}: ${a.title}`;
      if(img.decode)await img.decode();
      if(state.sequence!==sequence)return false;
      img.style.visibility='visible';img.removeAttribute('aria-busy');state.message.hidden=true;state.status='ready';state.stage.dataset.state='ready';return true;
    }catch(_){
      if(state.sequence!==sequence)return false;
      img.style.visibility='hidden';img.removeAttribute('aria-busy');state.status='error';state.stage.dataset.state='error';
      state.message.textContent=`Не удалось загрузить ${a.code}. Выберите кадр ещё раз или откройте оригинал.`;return false;
    }
  }
  const setActive = (code, push=false) => {
    const a=byCode[code]; if(!a||a.object!==objectId) return false;
    active=a;
    if(select&&select.value!=='all'&&select.value!==a.series) select.value=a.series;
    showSeries();
    const img=$('#hero-image');
    loadPicture(img,a).then(ready=>{if(ready&&active.code===a.code){const next=assets.find(item=>item.series===a.series&&item.code!==a.code);prefetch(next);}});
    $('#hero-link').href=url(a.original); $('#original-link').href=url(a.original);
    if($('#variant-note'))$('#variant-note').textContent=objects[objectId].variant_notes?.[a.code]||objects[objectId].variant_notes?.[a.series]||'';
    if (data.comments?.enabled) { try { sessionStorage.setItem(commentsSelectionKey, a.code); } catch (_) {} }
    $('#hero-code').textContent=a.code; $('#hero-title').textContent=a.title+(a.archived?' · убран из подборки':'');
    document.querySelectorAll('.asset-tile').forEach(el=>{
      const chosen=isShip?el.dataset.series===a.series:el.dataset.code===code;el.classList.toggle('selected',chosen);
      if(chosen)el.querySelector('.thumb-link').setAttribute('aria-current','true');else el.querySelector('.thumb-link').removeAttribute('aria-current');
    });
    document.querySelectorAll('.ship-view-link').forEach(link=>{if(link.dataset.code===code)link.setAttribute('aria-current','true');else link.removeAttribute('aria-current');});
    const pair=assets.filter(item=>item.series===a.series);
    document.querySelectorAll('[data-angle]').forEach(button=>{const item=pair[Number(button.dataset.angle)];button.hidden=!item;button.disabled=!item;if(item){button.textContent=item.title.split('·').pop().trim().replace(/^ракурс/i,'Ракурс');button.setAttribute('aria-pressed',String(item.code===code));}});
    for(const id of ['previous-image','next-image','dialog-previous','dialog-next']){const button=$('#'+id);if(button)button.disabled=visibleAssets().length<2;}
    if($('.dialog-navigation'))$('.dialog-navigation').hidden=visibleAssets().length<2;
    if(push){const dest=new URL(location.href);dest.hash=code;history.pushState({code},'',dest);}
    if($('#image-dialog').open) refreshDialog();
    return true;
  };
  const step = delta => {const list=visibleAssets();const i=list.findIndex(a=>a.code===active.code);setActive(list[i<0?(delta>0?0:list.length-1):(i+delta+list.length)%list.length].code,true);};
  function refreshDialog(){const img=$('#dialog-image');loadPicture(img,active);$('#dialog-caption').textContent=`${active.code} · ${active.title}`;}
  function fromHash() {
    let code;try{code=decodeURIComponent(location.hash.slice(1)).toLowerCase();}catch(_){code='';}
    if(code==='comments'||code==='giscus-comments'){setActive(active?.code||objects[objectId].cover);return;}
    const moved=byCode[code];
    if(moved&&moved.object!==objectId&&moved.previousObjects?.includes(objectId)){location.replace(url(moved.page+'#'+encodeURIComponent(code)));return;}
    if(code&&code!=='gallery'&&!setActive(code)){announce((data.deletedCodes||[]).includes(code)?`Кадр ${code} удалён из галереи.`:'Такой код не найден у этого объекта.');const u=new URL(location.href);u.hash=objects[objectId].cover;history.replaceState(null,'',u);setActive(objects[objectId].cover);}
    if(!code){if(select)select.value=objects[objectId].default_series;setActive(objects[objectId].cover);} else if(code==='gallery'){if(select&&isShip)select.value='all';showSeries();}
  }
  document.querySelectorAll('.thumb-link, .ship-view-link').forEach(a=>a.addEventListener('click',e=>{
    if(e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;
    e.preventDefault();setActive(a.dataset.code||a.closest('.asset-tile').dataset.code,true);
    if(isShip&&!comparing){refreshDialog();$('#image-dialog').showModal();}

  }));
  let hoverTimer;
  document.querySelectorAll('.thumb-link, .ship-view-link').forEach(link=>{
    const warm=()=>prefetch(byCode[link.dataset.code||link.closest('.asset-tile').dataset.code]);
    link.addEventListener('pointerenter',()=>{clearTimeout(hoverTimer);hoverTimer=setTimeout(warm,100);});
    link.addEventListener('pointerleave',()=>clearTimeout(hoverTimer));link.addEventListener('focus',warm);link.addEventListener('pointerdown',warm);
  });
  select?.addEventListener('change',()=>{showSeries();setActive(visibleAssets()[0].code,true);});
  document.querySelectorAll('[data-angle]').forEach(button=>button.addEventListener('click',()=>{const pair=assets.filter(a=>a.series===active.series);const a=pair[Number(button.dataset.angle)];if(a)setActive(a.code,true);}));
  $('#previous-image').addEventListener('click',()=>step(-1));$('#next-image').addEventListener('click',()=>step(1));
  $('#dialog-previous')?.addEventListener('click',()=>step(-1));$('#dialog-next')?.addEventListener('click',()=>step(1));
  $('#copy-code').addEventListener('click',()=>copy(active.code));
  $('#copy-link').addEventListener('click',()=>{const u=new URL(location.href);u.hash=active.code;copy(u.href);});
  $('#enlarge').addEventListener('click',()=>{refreshDialog();$('#image-dialog').showModal();});
  $('#close-image').addEventListener('click',()=>$('#image-dialog').close());
  $('#image-dialog').addEventListener('click',e=>{if(e.target===$('#image-dialog'))$('#image-dialog').close();});
  document.addEventListener('keydown',e=>{
    if(e.target.matches('input,textarea,select')||e.ctrlKey||e.metaKey||e.altKey||comparing)return;
    if(e.key==='ArrowRight'){e.preventDefault();step(1);}if(e.key==='ArrowLeft'){e.preventDefault();step(-1);}
  });
  for(const side of ['left','right']){
    const picker=$('#compare-'+side);
    assets.forEach(a=>{const opt=document.createElement('option');opt.value=a.code;opt.textContent=`${a.code} · ${a.title}`;picker.append(opt);});
    picker.addEventListener('change',()=>updateCompare(side));
  }
  function updateCompare(side){const a=byCode[$('#compare-'+side).value];const img=$('#compare-image-'+side);loadPicture(img,a);$('#compare-caption-'+side).textContent=`${a.code} · ${a.title}`;}
  $('#compare-toggle').addEventListener('click',()=>{
    comparing=!comparing;$('#compare-toggle').setAttribute('aria-pressed',String(comparing));$('#compare-toggle').textContent=comparing?'Закрыть сравнение':'Сравнить';
    $('#compare-panel').hidden=!comparing;$('#viewer').hidden=comparing;
    if(comparing){const comparable=assets.includes(active)?active:assets[0];$('#compare-left').value=comparable.code;$('#compare-right').value=assets[(assets.indexOf(comparable)+1)%assets.length].code;updateCompare('left');updateCompare('right');}
  });
  $('#hero-image').addEventListener('error',()=>announce('Изображение не загрузилось. Откройте оригинал по ссылке ниже.'));
  setActive(assets.find(a=>a.code===objects[objectId].cover).code);
  fromHash();
  window.addEventListener('hashchange',fromHash);window.addEventListener('popstate',fromHash);
  document.documentElement.dataset.ready='true';
})();

/* One discussion per canonical page; selecting an image never changes the thread. */
(() => {
  'use strict';
  const config = window.ALIVE_WORLD?.comments;
  const main = document.getElementById('main');
  if (document.body.dataset.page === 'overview') return;
  if (!config?.enabled || !config.repoId || !config.categoryId || !main || document.getElementById('comments')) return;

  // /index.html and / name the same World page. Preserve gallery selection and query parameters.
  if (location.pathname.endsWith('/index.html')) {
    const canonical = new URL(location.href);
    canonical.pathname = canonical.pathname.slice(0, -10);
    history.replaceState(history.state, '', canonical);
  }
  const box = document.createElement('details');
  box.id = 'comments';
  box.className = 'comments';
  box.setAttribute('aria-labelledby', 'comments-heading');
  const summary = document.createElement('summary');
  const title = document.createElement('span');
  title.id = 'comments-heading';
  title.textContent = 'Комментарии';
  const context = document.createElement('span');
  context.className = 'comments-context';
  context.textContent = 'Общее обсуждение';
  const arrow = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  arrow.setAttribute('viewBox', '0 0 24 24'); arrow.setAttribute('aria-hidden', 'true');
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', 'm6 9 6 6 6-6'); arrow.append(path);
  summary.append(title, context, arrow);
  const content = document.createElement('div'); content.className = 'comments-content';
  const fallback = document.createElement('a');
  fallback.className = 'quiet-link comments-link';
  fallback.href = `https://github.com/${config.repo}/discussions?discussions_q=`;
  fallback.target = '_blank';
  fallback.rel = 'noopener noreferrer';
  fallback.textContent = 'Обсуждения на GitHub';
  const status = document.createElement('p');
  status.className = 'comments-status';
  status.setAttribute('role', 'status');
  status.textContent = 'Загрузка комментариев…';
  const host = document.createElement('div');
  host.className = 'giscus';
  host.id = 'giscus-comments';
  const viewerCaption = document.querySelector('#viewer .viewer-caption');
  if (viewerCaption) {
    box.classList.add('comments--gallery');
    const code = document.getElementById('hero-code');
    const copyCode = document.createElement('button');
    copyCode.type = 'button'; copyCode.className = 'quiet-button comments-copy';
    const syncCode = () => { copyCode.textContent = 'Копировать код ' + code.textContent; };
    syncCode(); new MutationObserver(syncCode).observe(code, {childList:true,characterData:true,subtree:true});
    copyCode.addEventListener('click', () => document.getElementById('copy-code')?.click());
    content.append(copyCode);
    viewerCaption.after(box);
  } else main.append(box);
  content.append(status, host, fallback);
  box.append(summary, content);

  let started = false;
  let boundNumber = null;
  const worldRoot = new URL(document.body.dataset.root || './', location.href);
  const pagePath = location.pathname.slice(worldRoot.pathname.length);
  const validNumber = n => Number.isSafeInteger(n) && n > 0;
  let timeout;
  const fail = () => {
    clearTimeout(timeout);
    status.hidden = false;
    status.textContent = 'Комментарии не загрузились. Обновите страницу или откройте обсуждения на GitHub.';
  };
  // Read only messages from this widget, never page content or arbitrary origins.
  window.addEventListener('message', event => {
    const frame = host.querySelector('iframe');
    if (event.origin !== 'https://giscus.app' || event.source !== frame?.contentWindow || !event.data?.giscus) return;
    if (event.data.giscus.error) {
      // No thread exists until the first comment; this is an ordinary empty state.
      if (String(event.data.giscus.error).includes('Discussion not found') && !boundNumber) { clearTimeout(timeout); status.hidden = true; }
      else if (boundNumber) { host.hidden = true; fail(); }
      else fail();
      return;
    }
    if (event.data.giscus.resizeHeight || event.data.giscus.discussion || event.data.giscus.discussion === null) {
      clearTimeout(timeout);
      if (!host.hidden) status.hidden = true;
    }
  });
  const start = async () => {
    if (started) return;
    started = true;
    boundNumber = config.discussionNumbers?.[pagePath];
    if (!validNumber(boundNumber)) {
      // The feed discovers newly created threads without a site rebuild.
      // If lookup is unavailable, don't pretend an existing conversation is empty.
      const controller = new AbortController();
      const lookupTimeout = setTimeout(() => controller.abort(), 8000);
      try {
        const feedURL = 'https://raw.githubusercontent.com/esannikov/Alive/codex/alive-roadmap-site/docs/World/recent-comments.json';
        const response = await fetch(feedURL + '?map=' + Math.floor(Date.now()/60000), {cache:'no-store', credentials:'omit', signal:controller.signal});
        if (!response.ok) throw new Error('Discussion directory unavailable');
        const feed = await response.json();
        if (feed.schemaVersion !== 1 || !feed.discussionNumbers || typeof feed.discussionNumbers !== 'object') throw new Error('Invalid discussion directory');
        boundNumber = feed.discussionNumbers[pagePath];
        if (boundNumber !== undefined && !validNumber(boundNumber)) throw new Error('Invalid discussion number');
      } catch (_) { fail(); return; }
      finally { clearTimeout(lookupTimeout); }
    }
    if (!validNumber(boundNumber)) boundNumber = null;
    if (boundNumber) {
      fallback.href = `https://github.com/${config.repo}/discussions/${boundNumber}`;
      fallback.textContent = 'Открыть обсуждение на GitHub';
    }
    const script = document.createElement('script');
    script.src = 'https://giscus.app/client.js';
    script.async = true;
    script.crossOrigin = 'anonymous';
    Object.assign(script.dataset, {
      repo: config.repo, repoId: config.repoId, category: config.category,
      categoryId: config.categoryId, mapping: boundNumber ? 'number' : 'pathname', strict: '1',
      reactionsEnabled: config.reactionsEnabled || '0', emitMetadata: '1', inputPosition: config.inputPosition || 'bottom',
      theme: 'dark', lang: 'ru', loading: 'lazy'
    });
    if (boundNumber) script.dataset.term = String(boundNumber);
    const selectedHash = location.hash;
    script.addEventListener('error', fail, {once:true});
    script.addEventListener('load', () => {
      // Giscus removes its OAuth query parameter and hash; keep the selected gallery frame.
      if (selectedHash && !location.hash) {
        const restored = new URL(location.href); restored.hash = selectedHash;
        history.replaceState(history.state, '', restored);
      }
    }, {once:true});
    timeout = setTimeout(fail, 20000);
    box.append(script);
  };
  // The compact form stays closed until requested; one iframe survives image changes.
  box.addEventListener('toggle', () => { if (box.open) start(); });
  function openForAnchor() {
    if (['#comments', '#giscus-comments'].includes(location.hash)) box.open = true;
  }
  window.addEventListener('hashchange', openForAnchor);
  openForAnchor();
  if (new URL(location.href).searchParams.has('giscus')) box.open = true;
})();

/* Public read-only feed; GitHub Actions keeps its JSON up to date. */
(() => {
  const section = document.getElementById('recent-comments');
  if (!section || section.dataset.ready) return;
  section.dataset.ready = 'true';
  const list = document.getElementById('recent-comments-list');
  const status = document.getElementById('recent-comments-status');
  const retry = document.getElementById('recent-comments-retry');
  const root = new URL(document.body.dataset.root || './', location.href);
  const source = 'https://raw.githubusercontent.com/esannikov/Alive/codex/alive-roadmap-site/docs/World/recent-comments.json';
  let pending = false, checked = 0;
  const relative = new Intl.RelativeTimeFormat('ru', {numeric: 'auto'});
  function timeLabel(date) {
    const seconds = Math.min(0, (Date.parse(date) - Date.now()) / 1000);
    if (seconds > -60) return 'только что';
    for (const [unit, size] of [['day',86400], ['hour',3600], ['minute',60]]) {
      if (Math.abs(seconds) >= size) return relative.format(Math.ceil(seconds / size), unit);
    }
  }
  function render(items) {
    const fragment = document.createDocumentFragment();
    for (const item of items.slice(0,5)) {
      // Never render external comment markup or accept an arbitrary target URL.
      if (typeof item.page !== 'string' || !/^(?:[a-z0-9-]+\/)*(?:[a-z0-9-]+\.html)?$/.test(item.page) || !Number.isFinite(Date.parse(item.createdAt))) throw new Error('Invalid feed item');
      const li = document.createElement('li');
      const meta = document.createElement('div'); meta.className = 'recent-comment-meta';
      const object = document.createElement('a'); object.href = new URL(item.page + '#comments', root).href; object.textContent = item.title;
      const author = document.createElement('span'); author.textContent = item.author;
      const time = document.createElement('time'); time.dateTime = item.createdAt; time.textContent = timeLabel(item.createdAt); time.title = new Date(item.createdAt).toLocaleString('ru');
      meta.append(object, author, time);
      const excerpt = document.createElement('p'); excerpt.textContent = item.excerpt;
      const link = document.createElement('a'); link.href = object.href; link.className = 'quiet-link recent-comment-link'; link.textContent = 'Перейти к обсуждению';
      li.append(meta, excerpt, link); fragment.append(li);
    }
    list.replaceChildren(fragment); list.hidden = items.length === 0;
    status.textContent = items.length ? '' : 'Комментариев пока нет.'; status.hidden = items.length > 0;
  }
  async function refresh() {
    if (pending) return;
    pending = true; retry.hidden = true;
    const controller = new AbortController(); const timeout = setTimeout(() => controller.abort(), 12000);
    try {
      const response = await fetch(source, {cache:'no-store', credentials:'omit', signal:controller.signal});
      if (!response.ok) throw new Error('Feed unavailable');
      const feed = await response.json();
      if (feed.schemaVersion !== 1 || !Array.isArray(feed.items)) throw new Error('Invalid feed');
      render(feed.items); checked = Date.now();
    } catch (_) {
      status.hidden = false;
      status.textContent = list.childElementCount ? 'Не удалось обновить комментарии. Показана предыдущая загрузка.' : 'Комментарии не загрузились. Повторите попытку или откройте все обсуждения.';
      retry.hidden = false;
    } finally { clearTimeout(timeout); pending = false; }
  }
  retry.addEventListener('click', refresh);
  document.addEventListener('visibilitychange', () => { if (!document.hidden && Date.now() - checked > 60000) refresh(); });
  setInterval(() => { if (!document.hidden && Date.now() - checked > 60000) refresh(); }, 60000);
  refresh();
})();
