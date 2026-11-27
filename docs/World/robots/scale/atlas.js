(()=>{
 const viewer=document.getElementById('atlas-viewer'),poster=document.getElementById('atlas-poster');if(!viewer||!poster)return;
 const choices=[...document.querySelectorAll('[data-atlas-layout]')],slider=document.getElementById('atlas-zoom'),output=document.getElementById('atlas-percent'),status=document.getElementById('atlas-status');
 let selected=0,percent=15,drag=null;
 const file=()=>choices[selected].dataset.atlasLayout;
 function render(){
  poster.style.width=(9000*percent/100)+'px';output.value=Math.round(percent)+'%';slider.value=percent;
  const src=file()+(percent>20?'.png':'-preview.png');
  if(poster.getAttribute('src')!==src){status.textContent=percent>20?'Загрузка оригинала 9K…':'Загрузка схемы…';poster.src=src;}
  document.getElementById('atlas-png').href=file()+'.png';document.getElementById('atlas-svg').href=file()+'.svg';
 }
 function fit(){percent=Math.max(5,Math.min(100,(viewer.clientWidth-(innerWidth<700?24:40))/9000*100));render();viewer.scrollTo(0,0);}
 poster.addEventListener('load',()=>{status.textContent=percent>20?'Оригинал 9000 × 9000':'Превью · при увеличении загружается оригинал 9K';});
 poster.addEventListener('error',()=>{status.textContent='Не удалось загрузить схему. Оригинал доступен по ссылке PNG 9K.';});
 choices.forEach((a,i)=>a.addEventListener('click',e=>{e.preventDefault();selected=i;choices.forEach(x=>x.removeAttribute('aria-current'));a.setAttribute('aria-current','true');poster.alt=a.dataset.alt;render();viewer.scrollTo(0,0);}));
 document.getElementById('atlas-fit').addEventListener('click',fit);
 document.getElementById('atlas-actual').addEventListener('click',()=>{percent=100;render();});
 slider.addEventListener('input',()=>{percent=+slider.value;render();});
 viewer.addEventListener('pointerdown',e=>{if(e.button!==0||e.pointerType==='touch')return;drag={x:e.clientX,y:e.clientY,l:viewer.scrollLeft,t:viewer.scrollTop};viewer.setPointerCapture(e.pointerId);viewer.classList.add('dragging');e.preventDefault();});
 viewer.addEventListener('pointermove',e=>{if(drag){viewer.scrollLeft=drag.l+drag.x-e.clientX;viewer.scrollTop=drag.t+drag.y-e.clientY;}});
 const end=()=>{drag=null;viewer.classList.remove('dragging');};viewer.addEventListener('pointerup',end);viewer.addEventListener('pointercancel',end);viewer.addEventListener('lostpointercapture',end);
 document.querySelectorAll('[data-atlas-js]').forEach(e=>e.hidden=false);fit();
})();
