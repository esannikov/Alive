/* Run with an installed Playwright on NODE_PATH and docs served locally. */
const {chromium}=require('playwright');const assert=require('node:assert/strict');const fs=require('node:fs');
const base=process.env.WORLD_BASE_URL||'http://127.0.0.1:8771/World/';
(async()=>{const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.route('https://giscus.app/**',r=>r.abort());
 const go=async p=>{await page.goto(base+p);await page.waitForFunction(()=>document.documentElement.dataset.ready==='true');};
 await go('characters/emma/#emma038');assert((await page.locator('#identity-caption').innerText()).includes('emma-type-009'));
 assert.equal(await page.locator('#viewer-rail .rail-item').count(),12);assert.equal(await page.locator('#identity-frame-rail .rail-item').count(),5);
 assert.equal(await page.locator('#series-select').isVisible(),false);
 await page.locator('#identity-frame-rail [data-code="emma027"]').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('#hero-code').innerText(),'emma027');assert.equal(await page.locator('#identity-frame-rail [data-code="emma027"]').evaluate(e=>document.activeElement===e),true);
 await page.locator('#identity-select').selectOption('emma-type-020');assert.equal(await page.locator('#hero-code').innerText(),'emma023');assert(await page.locator('#next-image').isDisabled());assert.equal(await page.locator('#identity-frame-rail .rail-item').count(),1);
 await go('characters/emma/#emma-type-009');assert.equal(await page.locator('#hero-code').innerText(),'emma038');assert.equal(await page.locator('#identity-select').inputValue(),'emma-type-009');
 await page.locator('#next-image').click();assert((await page.locator('#identity-caption').innerText()).includes('emma-type-009'));
 await go('characters/emma/#emma012');await page.waitForURL('**/#emma028');assert((await page.locator('#identity-caption').innerText()).includes('emma-type-009'));
 await go('characters/emma/#emma036');assert(await page.locator('#copy-identity').isDisabled());assert((await page.locator('#identity-caption').innerText()).includes('сопоставления'));
 await go('characters/tais/#tais053');assert((await page.locator('.derivative.active').innerText()).includes('5'));assert.equal(await page.locator('#viewer-rail .rail-item').count(),2);assert.equal(await page.locator('#identity-frame-rail .rail-item').count(),4);
 await page.locator('#viewer-rail [data-identity="tais-type-059"]').click();assert.equal(await page.locator('#hero-code').innerText(),'tais059');assert.equal(await page.locator('#identity-frame-rail .rail-item').count(),1);
 await go('characters/kolka/#kolka034');assert.equal(await page.locator('#identity-frame-rail .rail-item').count(),4);
 await go('characters/romik/#romik007');assert((await page.locator('#identity-caption').innerText()).includes('romik-type-002'));
 await go('characters/vovik/#romik007');assert((await page.locator('#identity-caption').innerText()).includes('vovik-type-007'));
 await go('characters/emma/#emma038');await page.locator('#compare-toggle').click();await page.locator('#compare-right').selectOption('emma023');assert((await page.locator('#compare-caption-right').innerText()).includes('emma023'));
 await page.locator('#compare-toggle').click();await page.setViewportSize({width:390,height:844});assert(await page.locator('#identity-select').isVisible());const selectorBox=await page.locator('#identity-select').boundingBox(),compareBox=await page.locator('#compare-toggle').boundingBox();assert(selectorBox.x+selectorBox.width<=compareBox.x,'Identity filter overlaps compare control');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 fs.mkdirSync('output/playwright',{recursive:true});await page.screenshot({path:'output/playwright/emma-identity-mobile.png'});await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:'output/playwright/emma-identity-desktop.png'});await page.locator('#viewer-rail').scrollIntoViewIfNeeded();await page.screenshot({path:'output/playwright/emma-identity-controls.png'});
 await go('robots/gardener/#gardener005');assert.equal(await page.locator('#identity-select').count(),0);await page.locator('#next-image').click();assert.equal(await page.locator('#hero-code').innerText(),'gardener006');
 await go('ships/moag/');assert.equal(await page.locator('#identity-select').count(),0);assert(await page.locator('#hero-image').count());
 assert.deepEqual(errors,[]);console.log('PASS: identity groups, stable hashes, keyboard focus, frame navigation, A/B separation, shared scene membership, comparison and mobile layout');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
