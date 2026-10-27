/* Interaction checks use a local widget fixture; no comments are sent. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--disable-gpu']});
 try {
  const context=await browser.newContext({viewport:{width:390,height:844}});
  const original=JSON.parse(fs.readFileSync('docs/World/recent-comments.json','utf8'));
  const stats=Object.fromEntries(Object.keys(original.discussionStats).map(key=>[key,{messageCount:0,last:null}]));
  const recent=new Date(Date.now()-3600000).toISOString();
  stats['characters/fedor/']={messageCount:5,last:{author:'Producer',createdAt:recent}};
  stats['characters/emma/']={messageCount:2,last:{author:'Producer',createdAt:new Date(Date.now()-7200000).toISOString()}};
  await context.route('https://raw.githubusercontent.com/**/recent-comments.json*',route=>route.fulfill({contentType:'application/json',body:JSON.stringify({...original,discussionStats:stats})}));
  await context.route('https://giscus.app/client.js',route=>route.fulfill({contentType:'application/javascript',body:`const f=document.createElement('iframe');f.className='giscus-frame';f.src='https://giscus.app/fixture';document.querySelector('.giscus').append(f);`}));
  let resizeOnly=false;
  await context.route('https://giscus.app/fixture',route=>route.fulfill({contentType:'text/html',body:resizeOnly?`<script>parent.postMessage({giscus:{resizeHeight:300}},'*');parent.postMessage({giscus:{error:'failed'}},'*')</script>`:`<script>parent.postMessage({giscus:{resizeHeight:300,discussion:null}},'*')</script><p>Test widget</p>`}));
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8769/World/');await page.locator('[data-discussion-summary="characters/fedor/"][data-loaded]').waitFor();
  const fedor=page.locator('[data-discussion-summary="characters/fedor/"]');assert.equal(await fedor.locator('.unread-dot').count(),1);
  await page.locator('[data-filter="robots"]').click();assert.equal(await page.locator('.object-card:visible:not([data-filter-kind="robots"])').count(),0);
  await page.locator('[data-filter="all"]').click();await page.locator('#home-sort').selectOption('activity');assert.equal(await page.locator('.object-grid > .object-card').first().locator('[data-discussion-summary]').getAttribute('data-discussion-summary'),'characters/fedor/');
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.goto('http://127.0.0.1:8769/World/characters/fedor/');assert.equal(await page.evaluate(()=>localStorage.getItem('alive-world:discussion-read:characters/fedor/')),null);
  await page.addInitScript(()=>{Object.defineProperty(navigator,'clipboard',{value:{writeText:async s=>window.__copied=s},configurable:true});});
  await page.reload();await page.locator('#viewer-rail .rail-item').nth(1).click();const code=await page.locator('#hero-code').innerText();
  assert(await page.locator('#comments').evaluate(el=>el.open));assert.equal(await page.locator('#gallery + #comments').count(),1);assert(await page.locator('#gallery').isHidden());assert.equal(await page.locator('#viewer-rail .rail-item').count(),6);await page.locator('.comment-variant').click();await page.locator('#giscus-comments').scrollIntoViewIfNeeded();await page.waitForFunction(()=>document.querySelector('.comments-status').hidden);await page.waitForFunction(()=>localStorage.getItem('alive-world:discussion-read:characters/fedor/'));
  const seen=await page.evaluate(()=>localStorage.getItem('alive-world:discussion-read:characters/fedor/'));await page.locator('#comments > summary').click();await page.locator('#comments > summary').click();assert.equal(await page.evaluate(()=>localStorage.getItem('alive-world:discussion-read:characters/fedor/')),seen);
  assert.equal(await page.evaluate(()=>window.__copied),code);assert((await page.locator('.comment-copy-hint').innerText()).includes('вставьте'));
  const originalFrame=await page.locator('.giscus-frame').getAttribute('src');await page.locator('#viewer-rail .rail-item').nth(2).click();assert.equal(await page.locator('.giscus-frame').getAttribute('src'),originalFrame);assert(await page.locator('#comments').evaluate(el=>el.open));
  const pending=page.locator('[data-pending]').first();await pending.click({force:true});assert.equal(await pending.getAttribute('aria-disabled'),'true');assert((await page.locator('#notice').innerText()).includes('Пока не подготовлено'));
  await page.locator('#compare-toggle').click();const buttons=page.locator('#compare-rail .rail-item');const first=await buttons.nth(2).getAttribute('data-code'),second=await buttons.nth(3).getAttribute('data-code');await buttons.nth(2).click();await buttons.nth(3).click();assert.equal(await page.locator('#compare-left').inputValue(),first);assert.equal(await page.locator('#compare-right').inputValue(),second);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.goto('http://127.0.0.1:8769/World/');await page.locator('[data-discussion-summary="characters/fedor/"][data-loaded]').waitFor();assert.equal(await page.locator('[data-discussion-summary="characters/fedor/"] .unread-dot').count(),0);resizeOnly=true;await page.goto('http://127.0.0.1:8769/World/robots/lon/#comments');await page.waitForFunction(()=>document.querySelector('.comments-status').textContent.includes('не загрузились'));assert.equal(await page.evaluate(()=>localStorage.getItem('alive-world:discussion-read:robots/lon/')),null);assert.deepEqual(errors,[]);
  console.log('PASS: filters, activity sort, local unread, successful widget read, code copy, stable discussion, thumbnail compare, pending tabs, mobile');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
