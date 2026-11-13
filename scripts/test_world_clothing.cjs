/* Clothing collection: discovery, native gallery and unmodified portrait originals. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.WORLD_BASE_URL||'http://127.0.0.1:8773/World/';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('https://giscus.app/**',r=>r.abort());
  await page.goto(base);
  const collection=page.locator('.object-card[data-kind="collection"][data-filter-kind="clothing"]');
  assert.equal(await collection.count(),1);
  assert.equal(await page.locator('.object-card a[href="clothing/tais/"]').count(),0,'Child must remain inside the collection');
  await page.locator('[data-filter="clothing"]').click();
  assert.equal(await page.locator('.object-grid > .object-card:visible').count(),1);
  await collection.locator('h3 a').click();
  assert.equal(await page.locator('h1').innerText(),'Одежда');
  assert.equal(await page.locator('.object-card').count(),1);
  assert.equal(await page.locator('.object-card .card-image img').evaluate(img=>getComputedStyle(img).objectFit),'contain');
  await page.locator('.object-card h3 a').click();
  assert.equal(await page.locator('h1').innerText(),'Одежда Таис');
  const expected=Array.from({length:8},(_,i)=>'taisc'+String(i+1).padStart(3,'0'));
  assert.deepEqual(await page.locator('#viewer-rail .rail-item').evaluateAll(els=>els.map(e=>e.dataset.code)),expected);
  for(const code of expected){
   await page.locator('#viewer-rail [data-code="'+code+'"]').click();
   await page.waitForFunction(()=>document.querySelector('#hero-image').parentElement.dataset.state==='ready');
   assert.equal(await page.locator('#hero-code').innerText(),code);
   assert.deepEqual(await page.locator('#hero-image').evaluate(img=>[img.naturalWidth,img.naturalHeight]),[1024,1536]);
   assert((await page.locator('#original-link').getAttribute('href')).endsWith('/clothing/tais/images/'+code+'.png'));
  }
  await page.locator('#compare-toggle').click();
  assert.equal(await page.locator('#compare-left option').count(),8);
  assert.equal(await page.locator('#compare-right option').count(),8);
  await page.goto(base+'characters/tais/');
  await page.locator('.derivatives a',{hasText:'Костюм'}).click();
  assert(page.url().includes('/clothing/tais/'));
  await page.goto(base+'search.html?q=taisc008');
  assert.equal(await page.locator('.search-result').count(),1);
  await page.locator('.search-result').click();
  await page.waitForFunction(()=>document.querySelector('#hero-code')?.textContent==='taisc008');
  assert.equal(await page.locator('#hero-code').innerText(),'taisc008');
  await page.setViewportSize({width:390,height:844});
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Gallery must fit mobile viewport');
  assert.equal(await page.locator('#hero-code').innerText(),'taisc008');
  const nojs=await browser.newContext({javaScriptEnabled:false});const staticPage=await nojs.newPage();
  await staticPage.goto(base+'clothing/');await staticPage.locator('.object-card h3 a').click();
  assert.equal(await staticPage.locator('.asset-tile').count(),8);await nojs.close();
  assert.deepEqual(errors,[]);
  console.log('PASS: clothing discovery, nested card, 8 full-resolution images, comparison, character link, search, mobile and no-JS gallery');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
