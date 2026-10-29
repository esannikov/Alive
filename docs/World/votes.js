/* Vote writes stay inside Giscus OAuth; only a public, computed summary is read here. */
(() => {
 const data=window.ALIVE_WORLD, viewer=document.querySelector('#viewer'), codeNode=document.querySelector('#hero-code');
 if(!viewer||!codeNode||!data?.comments?.enabled)return;
 const root=new URL(document.body.dataset.root||'./',location.href), cfg=data.comments;
 const box=document.createElement('section');box.className='variant-votes';box.setAttribute('aria-label','Голосование по варианту');
 const widget=document.createElement('div'),status=document.createElement('div'),hint=document.createElement('small');
 status.className='vote-summary';status.setAttribute('aria-live','polite');hint.className='vote-hint';hint.textContent='Женя, Лена ×2, Игорь · сводка обновляется в 09:00 и 21:00 по Киеву. При смене выбора учитывается последний из активных голосов.';
 box.append(widget,status,hint);viewer.querySelector('.viewer-caption').after(box);
 let current='',frame=null,feed=null,failed=false;
 const labels={esannikov:'Женя',elenaalive:'Лена', 'isto3110-ship-it':'Игорь'};
 function render(){status.replaceChildren();const v=feed?.variants?.[current];
  if(!v){status.textContent=failed?'Сводка голосов недоступна.':'Сводка голосов загружается…';return;}
  for(const [side,emoji] of [['for','👍'],['against','👎']]){const part=document.createElement('span');const names=v.votes.filter(x=>x.choice===side).map(x=>(labels[x.login.toLowerCase()]||x.login)+(x.weight===2?' ×2':''));part.textContent=emoji+' '+v.scores[side]+' · '+(names.join(', ')||'нет голосов');status.append(part);}
  if(v.status==='unanimous_against'){const mark=document.createElement('span');mark.className='vote-against';mark.textContent='На разбор: все против';status.append(mark);}
  if(feed.generatedAt)status.title='Сводка от '+new Date(feed.generatedAt).toLocaleString('ru-RU');
 }
 function select(){const code=codeNode.textContent.trim();if(code===current)return;current=code;render();
  let session='';try{session=JSON.parse(localStorage.getItem('giscus-session')||'""');}catch(_){}
  const origin=new URL(location.href);origin.searchParams.delete('giscus');origin.hash=code;
  const params=new URLSearchParams({origin:origin.href,backLink:origin.href,session:typeof session==='string'?session:'',repo:cfg.repo,repoId:cfg.repoId,category:cfg.category,categoryId:cfg.categoryId,term:'ALIVE vote v1 '+code,strict:'1',reactionsEnabled:'1',emitMetadata:'1',inputPosition:'bottom',description:'Голосование за вариант '+code,theme:cfg.voteTheme});
  frame=document.createElement('iframe');frame.src='https://giscus.app/ru/widget?'+params;frame.title='Голосование '+code;frame.setAttribute('aria-label','Голосование '+code);frame.style.cssText='border:0;width:100%;height:80px;color-scheme:dark';frame.scrolling='no';widget.replaceChildren(frame);
 }
 window.addEventListener('message',e=>{if(e.origin!=='https://giscus.app'||e.source!==frame?.contentWindow||!e.data?.giscus)return;const m=e.data.giscus;if(Number.isFinite(m.resizeHeight))frame.style.height=Math.max(44,Math.min(180,m.resizeHeight))+'px';if(m.error&&!String(m.error).includes('Discussion not found')){status.textContent='Голосование не загрузилось. Попробуйте обновить страницу.';}if(m.signOut){try{localStorage.removeItem('giscus-session');}catch(_){}current='';select();}});
 async function refresh(){try{const url=new URL('https://raw.githubusercontent.com/'+cfg.repo+'/codex/alive-roadmap-site/docs/World/votes.json');url.searchParams.set('v',Date.now());const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error();const d=await r.json();if(d.schemaVersion!==1||!d.variants)throw Error();feed=d;failed=false;}catch(_){failed=true;}render();}
 new MutationObserver(select).observe(codeNode,{subtree:true,childList:true,characterData:true});select();refresh();
})();
