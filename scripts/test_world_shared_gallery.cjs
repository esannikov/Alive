/* One stable image may appear in both its character gallery and a reserve. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.WORLD_BASE_URL||'http://127.0.0.1:8769/World/';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('https://giscus.app/**',r=>r.abort());
  await page.goto(base+'characters/emma/');
  assert.deepEqual(await page.locator('#viewer-rail .rail-item').evaluateAll(els=>els.map(e=>e.dataset.code)),[1,2,3,5,7,8,9,10].map(i=>'emma'+String(i).padStart(3,'0')));
  assert.equal(await page.locator('#compare-left option').count(),8);
  for(const i of [1,2,3,5,7,8,9,10]){
   const code='emma'+String(i).padStart(3,'0');await page.locator('#viewer-rail [data-code="'+code+'"]').click();
   await page.waitForFunction(()=>document.querySelector('#hero-image').parentElement.dataset.state==='ready');
   assert.equal(await page.locator('#hero-code').innerText(),code);
   assert(!(await page.locator('#hero-title').innerText()).includes('убран'));
  }
  await page.goto(base+'characters/emma/#emma006');assert.equal(await page.locator('#hero-code').innerText(),'emma006');assert(page.url().includes('/base-girls/'));
  await page.goto(base+'characters/base-girls/#emma006');assert.equal(await page.locator('#hero-code').innerText(),'emma006');assert(page.url().includes('/base-girls/'));
  assert.equal(await page.locator('#viewer-rail .rail-item').count(),90);
  await page.goto(base+'characters/base-girls/?giscus=test-return');assert.equal(await page.locator('#hero-code').innerText(),'emma006');assert(page.url().endsWith('#emma006'));
  await page.goto(base+'search.html?q=emma006');assert.equal(await page.locator('.search-result').count(),1);assert((await page.locator('.search-result').getAttribute('href')).includes('/characters/base-girls/#emma006'));
  for(const id of ['fedor','kolka']){await page.goto(base+'characters/'+id+'/#fedor028');assert.equal(await page.locator('#hero-code').innerText(),'fedor028');assert(page.url().includes('/'+id+'/'));}
  await page.goto(base+'characters/ilya/#ilya003');await page.waitForURL('**/characters/egor/#ilya003');assert.equal(await page.locator('#hero-code').innerText(),'ilya003');
  await page.goto(base+'characters/base-girls/#valek014');await page.waitForURL('**/characters/valek/#valek014');assert((await page.locator('#hero-title').innerText()).includes('убран'));
  assert.deepEqual(errors,[]);console.log('PASS: current Emma selection, reserve redirect, shared Fedor/Kolka candidate, Egor transfer and archived Valek');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
