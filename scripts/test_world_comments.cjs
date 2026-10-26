/* Deterministic browser tests: no external comments or discussions are created. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');const path=require('node:path');
const root=path.resolve(__dirname,'..');
const base=process.env.WORLD_BASE_URL||'http://127.0.0.1:8769/World/';
const localData=fs.readFileSync(path.join(root,'docs/World/data.js'),'utf8');
const data=JSON.parse(localData.slice('window.ALIVE_WORLD='.length).trim().replace(/;$/,''));
const fixture=structuredClone(data);fixture.comments={...fixture.comments,enabled:true,categoryId:'DIC_test_fixture'};
const widget=`<!doctype html><html lang="ru"><head><meta charset="utf-8"></head><body style="background:#090a0b;color:#f3f3ef;font:16px sans-serif;padding:20px"><p>Комментарии · тест отображения</p><p>Войти с GitHub</p><script>parent.postMessage({giscus:{resizeHeight:170,discussion:null}},'${new URL(base).origin}')</script></body></html>`;
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--disable-gpu']});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000}});let clients=0;let fail=false;
  await context.route('**/data.js*',r=>r.fulfill({body:'window.ALIVE_WORLD='+JSON.stringify(fixture)+';',contentType:'application/javascript'}));
  await context.route('https://giscus.app/**',async route=>{
   const u=new URL(route.request().url());
   if(u.pathname==='/client.js'){
    clients++;if(fail)return route.abort();
    // Emulate only the public client contract; never exercise OAuth or createDiscussion.
    return route.fulfill({contentType:'application/javascript',body:`(()=>{const s=document.currentScript,d=s.dataset;const f=document.createElement('iframe');f.title='Комментарии';f.className='giscus-frame';f.src='https://giscus.app/ru/widget?'+new URLSearchParams({...d,term:location.pathname.substring(1).replace(/\\.\\w+$/,'')});document.querySelector('.giscus').append(f);if(new URL(location.href).searchParams.has('giscus'))history.replaceState(null,'',location.pathname);})();`});
   }
   if(u.pathname==='/ru/widget')return route.fulfill({body:widget,contentType:'text/html'});
   return route.fulfill({body:'',contentType:'text/css'});
  });
  const p=await context.newPage();let errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto(base+'characters/valek/index.html?v=test');
  assert(p.url().endsWith('/characters/valek/?v=test'));
  assert.equal(await p.locator('#comments').count(),1);assert.equal(await p.locator('#viewer > #comments').count(),1);
  assert.equal(clients,0,'Giscus must wait for scrolling on a long gallery');
  await p.locator('#comments').scrollIntoViewIfNeeded();if(!await p.locator('#comments').evaluate(el=>el.open))await p.locator('#comments > summary').click();await p.waitForFunction(()=>document.querySelector('#comments .comments-status').hidden);
  let frame=new URL(await p.locator('.giscus-frame').getAttribute('src'));
  for(const [key,value] of Object.entries({mapping:'pathname',strict:'1',theme:'dark',lang:'ru',inputPosition:'bottom',reactionsEnabled:'0'}))assert.equal(frame.searchParams.get(key),value);
  const term=frame.searchParams.get('term');assert(term.endsWith('/characters/valek/'));
  assert.equal(await p.locator('#comments').evaluate(el=>el.previousElementSibling.className),'viewer-caption');
  const originalFrame=frame.href;await p.locator('.thumb-link[href="#valek008"]').click();assert.equal(await p.locator('.giscus-frame').getAttribute('src'),originalFrame);assert((await p.locator('.comments-copy').innerText()).includes('valek008'));
  await p.addScriptTag({path:path.join(root,'docs/World/site.js')});assert.equal(await p.locator('#comments').count(),1);assert.equal(await p.locator('.giscus-frame').count(),1);
  await p.goto(base+'index.html');assert.equal(await p.locator('#comments').count(),0);assert.equal(await p.locator('#recent-comments').count(),1);
  await p.goto(base+'characters/valek/?giscus=test-session#giscus-comments');await p.locator('#comments').scrollIntoViewIfNeeded();if(!await p.locator('#comments').evaluate(el=>el.open))await p.locator('#comments > summary').click();await p.waitForFunction(()=>!location.search.includes('giscus='));assert.equal(new URL(p.url()).hash,'#valek008');
  await p.goto(base+'characters/valek/#comments');await p.locator('#comments').waitFor();assert.equal(new URL(p.url()).hash,'#comments');
  await p.setViewportSize({width:390,height:844});await p.locator('#comments').scrollIntoViewIfNeeded();if(!await p.locator('#comments').evaluate(el=>el.open))await p.locator('#comments > summary').click();assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  if(process.env.QA_SCREENSHOT)await p.screenshot({path:process.env.QA_SCREENSHOT});
  fail=true;await p.goto(base+'robots/lon/');await p.locator('#comments').scrollIntoViewIfNeeded();if(!await p.locator('#comments').evaluate(el=>el.open))await p.locator('#comments > summary').click();await p.waitForFunction(()=>document.querySelector('.comments-status').textContent.includes('не загрузились'));
  assert.deepEqual(errors,[]);
  // All World routes receive the same integration. Disabled config has no remote widget.
  fail=false;
  function htmlFiles(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?htmlFiles(path.join(dir,e.name)):e.name.endsWith('.html')?[path.join(dir,e.name)]:[]);}
  let pages=0;for(const file of htmlFiles(path.join(root,'docs/World'))){await p.goto(new URL(path.relative(path.join(root,'docs/World'),file),base).href);assert.equal(await p.locator('#comments').count(),path.relative(path.join(root,'docs/World'),file)==='index.html'?0:1);pages++;}
  await context.unroute('**/data.js*');await p.goto(base+'characters/valek/');if(!data.comments.enabled)assert.equal(await p.locator('#comments').count(),0);
  console.log(JSON.stringify({status:'PASS',pages,lazy:true,strict:true,indexAlias:true,hashStable:true,oauthReturnHash:true,duplicateGuard:true,mobile:true,loadFailure:true,externalWrites:0}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
