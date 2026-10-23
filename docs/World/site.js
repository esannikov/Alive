/* Static ALIVE catalogue. No accounts, writes, approvals, or remote API calls. */
(() => {
  'use strict';
  const data = window.ALIVE_WORLD;
  if (!data) return;
  const root = new URL(document.body.dataset.root || './', location.href);
  const url = p => new URL(p, root).href;
  const $ = s => document.querySelector(s);
  const byCode = Object.fromEntries(data.assets.map(a => [a.code, a]));
  const objects = Object.fromEntries(data.objects.map(o => [o.id, o]));
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
      text: `${a.code} ${objects[a.object].title} ${a.title} ${series[a.series]} ${objects[a.object].variant_notes?.[a.series]||''} ${objects[a.object].kind==='ship'?'корабль станция внешний облик':'портрет внешность'} концепт`,
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
  const isShip=objects[objectId].kind==='ship';
  const select = $('#series-select'); let active = assets[0], comparing = false;
  const visibleAssets = () => assets.filter(a=>isShip?a.series===active.series:select.value==='all'||a.series===select.value);
  const showSeries = () => {
    if(isShip){$('#gallery-count').textContent=`${new Set(assets.map(a=>a.series)).size} вариантов`;return;}
    document.querySelectorAll('.asset-tile').forEach(el=>{el.hidden=select.value!=='all'&&el.dataset.series!==select.value;});
    const count=visibleAssets().length; $('#gallery-count').textContent=objects[objectId].kind==='ship'?`${count} кадров`:`${count} вариантов`;
  };
  const setActive = (code, push=false) => {
    const a=byCode[code]; if(!a||a.object!==objectId) return false;
    active=a;
    if(select&&select.value!=='all'&&select.value!==a.series) select.value=a.series;
    showSeries();
    const img=$('#hero-image'); img.src=url(a.original); img.alt=`${a.code}: ${a.title}`;
    $('#hero-link').href=url(a.original); $('#original-link').href=url(a.original);
    if($('#variant-note'))$('#variant-note').textContent=objects[objectId].variant_notes?.[a.series]||'';
    $('#hero-code').textContent=a.code; $('#hero-title').textContent=a.title+(a.archived?' · убран из подборки':'');
    document.querySelectorAll('.asset-tile').forEach(el=>{
      const chosen=isShip?el.dataset.series===a.series:el.dataset.code===code;el.classList.toggle('selected',chosen);
      if(chosen)el.querySelector('.thumb-link').setAttribute('aria-current','true');else el.querySelector('.thumb-link').removeAttribute('aria-current');
    });
    document.querySelectorAll('.ship-view-link').forEach(link=>{if(link.dataset.code===code)link.setAttribute('aria-current','true');else link.removeAttribute('aria-current');});
    const pair=assets.filter(item=>item.series===a.series);
    document.querySelectorAll('[data-angle]').forEach(button=>button.setAttribute('aria-pressed',String(pair[Number(button.dataset.angle)]?.code===code)));
    if(push){const dest=new URL(location.href);dest.hash=code;history.pushState({code},'',dest);}
    if($('#image-dialog').open) refreshDialog();
    return true;
  };
  const step = delta => {const list=visibleAssets();const i=list.findIndex(a=>a.code===active.code);setActive(list[i<0?(delta>0?0:list.length-1):(i+delta+list.length)%list.length].code,true);};
  function refreshDialog(){const img=$('#dialog-image');img.src=url(active.original);img.alt=`${active.code}: ${active.title}`;$('#dialog-caption').textContent=`${active.code} · ${active.title}`;}
  function fromHash() {
    let code;try{code=decodeURIComponent(location.hash.slice(1)).toLowerCase();}catch(_){code='';}
    if(code&&code!=='gallery'&&!setActive(code))announce('Такой код не найден у этого объекта.');
    if(!code){if(select)select.value=objects[objectId].default_series;setActive(objects[objectId].cover);} else if(code==='gallery'){if(select&&isShip)select.value='all';showSeries();}
  }
  document.querySelectorAll('.thumb-link, .ship-view-link').forEach(a=>a.addEventListener('click',e=>{
    if(e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;
    e.preventDefault();setActive(a.dataset.code||a.closest('.asset-tile').dataset.code,true);
    if(!comparing){$('#viewer').scrollIntoView({block:'start',behavior:'auto'});}
  }));
  select?.addEventListener('change',()=>{showSeries();setActive(visibleAssets()[0].code,true);});
  document.querySelectorAll('[data-angle]').forEach(button=>button.addEventListener('click',()=>{const pair=assets.filter(a=>a.series===active.series);const a=pair[Number(button.dataset.angle)];if(a)setActive(a.code,true);}));
  $('#previous-image').addEventListener('click',()=>step(-1));$('#next-image').addEventListener('click',()=>step(1));
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
  function updateCompare(side){const a=byCode[$('#compare-'+side).value];const img=$('#compare-image-'+side);img.src=url(a.original);img.alt=`${a.code}: ${a.title}`;$('#compare-caption-'+side).textContent=`${a.code} · ${a.title}`;}
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
