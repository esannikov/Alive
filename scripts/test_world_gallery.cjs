/* Run against a locally served docs/ tree with Playwright available in NODE_PATH.
   WORLD_BASE_URL defaults to http://127.0.0.1:8769/World/.
   CHROME_BIN optionally selects an installed Chromium executable. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const data=JSON.parse(fs.readFileSync(path.join(root,'docs/World/data.js'),'utf8').replace(/^window.ALIVE_WORLD=/,'').replace(/;\s*$/,''));
const base=process.env.WORLD_BASE_URL||'http://127.0.0.1:8769/World/';
const byUrl=new Map(data.assets.flatMap(a=>[[a.original,a],[new URL(a.display||a.original,base).href,a]]));
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_BIN?{executablePath:process.env.CHROME_BIN}:{}),args:['--disable-gpu']});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  let releaseSlow;const slow=new Promise(resolve=>releaseSlow=resolve);const failures=new Set();
  await page.route('**/*',async route=>{
   const a=byUrl.get(route.request().url());if(!a)return route.continue();
   if(a.code==='moag013')await slow;
   if(failures.has(a.code))return route.abort();
   await route.fulfill({body:fs.readFileSync(path.join(root,a.sourceFile)),contentType:/\.png$/i.test(a.sourceFile)?'image/png':'image/jpeg'});
  });
  await page.goto(base+'ships/moag/');
  await page.waitForFunction(()=>document.documentElement.dataset.ready==='true'&&document.querySelector('#hero-image').parentElement.dataset.state==='ready');
  assert.equal(await page.locator('.ship-variant').count(),18);
  assert.equal(data.assets.filter(a=>a.object==='moag').length,34);
  assert(!data.assets.some(a=>['moag005','moag009'].includes(a.code)));
  assert(await page.locator('#gallery').isHidden());
  assert.equal(await page.locator('#viewer-rail .rail-item').count(),34);
  await page.locator('#viewer-rail [data-code="moag013"]').scrollIntoViewIfNeeded();
  const before=await page.evaluate(()=>scrollY);
  await page.locator('#viewer-rail [data-code="moag013"]').click();
  const loading=await page.evaluate(()=>({y:scrollY,visibility:getComputedStyle(document.querySelector('#hero-image')).visibility,state:document.querySelector('#hero-image').parentElement.dataset.state,message:document.querySelector('#hero-image').parentElement.querySelector('[role="status"]').textContent,code:document.querySelector('#hero-code').textContent}));
  assert(Math.abs(loading.y-before)<2,JSON.stringify({before,loading}));
  assert.equal(loading.visibility,'hidden');assert.equal(loading.state,'loading');assert.equal(loading.code,'moag013');assert(loading.message.includes('moag013'));
  assert(await page.locator('#image-dialog').isHidden());
  await page.locator('#viewer-rail [data-code="moag019"]').click();
  await page.waitForFunction(()=>document.querySelector('#hero-image').parentElement.dataset.state==='ready'&&document.querySelector('#hero-code').textContent==='moag019');
  releaseSlow();
  await page.waitForResponse(r=>r.url().includes('moag013-parallax-front.png'));
  await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
  assert.equal(await page.locator('#hero-code').innerText(),'moag019');
  assert((await page.locator('#hero-image').getAttribute('src')).includes('moag019-contour-front.png'));
  failures.add('moag021');await page.locator('#viewer-rail [data-code="moag021"]').click();
  await page.waitForFunction(()=>document.querySelector('#hero-image').parentElement.dataset.state==='error');
  assert.equal(await page.locator('#hero-image').evaluate(i=>getComputedStyle(i).visibility),'hidden');
  failures.delete('moag021');await page.locator('#viewer-rail [data-code="moag021"]').click();
  await page.waitForFunction(()=>document.querySelector('#hero-image').parentElement.dataset.state==='ready');
  for(const code of ['moag006','moag010']){
   await page.locator('#viewer-rail [data-code="'+code+'"]').click();
   assert.equal(await page.locator('[data-angle]:visible').count(),1);
   assert.equal(await page.locator('[data-angle]:visible').innerText(),'Ракурс 2');
   await page.locator('#enlarge').click();assert(await page.locator('#image-dialog').isVisible());assert(await page.locator('#dialog-next').isDisabled());
   await page.locator('#close-image').click();
  }
  for(const id of ['tais','fedor','emma','kolka']){
   await page.goto(base+'characters/'+id+'/');
   await page.waitForFunction(()=>document.querySelector('#hero-image').parentElement.dataset.state==='ready');
   assert(await page.locator('#gallery').isHidden());assert(await page.locator('#comments').evaluate(el=>el.open));
   const width=await page.locator('#viewer-rail .rail-item img').first().evaluate(el=>el.getBoundingClientRect().width);assert(Math.abs(width-100.8)<1,`desktop thumbnail width ${width}`);
   await page.locator('#next-image').click();
   await page.waitForFunction(()=>document.querySelector('#hero-image').parentElement.dataset.state==='ready');
  }
  await page.setViewportSize({width:390,height:844});await page.goto(base+'characters/kolka/#kolka003');
  await page.waitForFunction(()=>document.querySelector('#hero-code')?.textContent==='kolka003');
  const mobileWidth=await page.locator('#viewer-rail .rail-item img').first().evaluate(el=>el.getBoundingClientRect().width);
  assert(Math.abs(mobileWidth-86.4)<1,`mobile thumbnail width ${mobileWidth}`);
  assert(await page.locator('#gallery').isHidden());assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  const nojs=await browser.newContext({javaScriptEnabled:false});const fallback=await nojs.newPage();await fallback.goto(base+'characters/kolka/');assert(await fallback.locator('#gallery').isVisible());assert(await fallback.locator('.gallery-fallback').isVisible());await nojs.close();
  assert.deepEqual(errors,[]);
  console.log(JSON.stringify({status:'PASS',shipFrames:34,shipVariants:18,viewportStable:true,oldImageHiddenDuringLoad:true,lateResponseIgnored:true,errorAndRetry:true,singleViewLabels:true,characterNavigation:true}));
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
