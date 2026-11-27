/* Real WebGL interaction checks. Run with a local docs server and Playwright. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.BASE_URL||'http://127.0.0.1:8774';
const route=base+'/World/ships/moag/model/';
const shotDir=process.env.SHOT_DIR;
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
 try {
  const context=await browser.newContext({viewport:{width:1440,height:1100},reducedMotion:'reduce'});
  const page=await context.newPage(), errors=[], requests=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>requests.push(r.url()));
  await page.goto(base+'/World/ships/moag/');
  await page.locator('.derivatives a', {hasText:'3D-модель'}).click();assert.equal(page.url(),route);
  assert.equal(await page.locator('[aria-current="page"]', {hasText:'3D-модель'}).count(),1);
  assert(!requests.some(x=>x.endsWith('.glb')),'Model must not load before user requests it');
  await page.getByRole('button',{name:'Открыть 3D-модель',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#station-model').loaded,null,{timeout:90000});
  await page.waitForFunction(()=>!document.querySelector('#rotate-model').disabled);
  const state=()=>page.locator('#station-model').evaluate(v=>({orbit:v.getCameraOrbit(),target:v.getCameraTarget(),rotation:v.turntableRotation,auto:v.autoRotate}));
  let previous=await state();
  const rect=await page.locator('#station-model').boundingBox();
  await page.mouse.move(rect.x+rect.width/2,rect.y+rect.height/2);await page.mouse.down();await page.mouse.move(rect.x+rect.width*.7,rect.y+rect.height/2,{steps:12});await page.mouse.up();
  await page.waitForFunction(t=>Math.abs(document.querySelector('#station-model').getCameraOrbit().theta-t)>.01,previous.orbit.theta);
  await page.locator('#zoom-in').click();await page.waitForTimeout(150);assert((await state()).orbit.radius<previous.orbit.radius);
  await page.locator('#zoom-out').click();
  for(const view of ['top','bottom','spire','rim','overview']){
   await page.locator(`[data-view="${view}"]`).click();
   await page.waitForTimeout(200);assert.equal(await page.locator(`[data-view="${view}"]`).getAttribute('aria-pressed'),'true');
   if(view==='spire')assert(Math.abs((await state()).target.y-252)<1);
   if(view==='bottom')assert((await state()).orbit.phi>Math.PI/2);
   if(shotDir&&['bottom','spire','rim'].includes(view)){await page.evaluate(()=>{document.activeElement.blur();window.scrollTo(0,0)});await page.screenshot({path:shotDir+'/'+view+'.png',fullPage:true});}
  }
  await page.locator('#rotate-model').click();assert((await state()).auto);await page.locator('#rotate-model').click();assert(!(await state()).auto);
  if(await page.locator('#model-fullscreen').isVisible()){
   await page.locator('#model-fullscreen').click();await page.waitForFunction(()=>!!document.fullscreenElement);
   await page.locator('#model-fullscreen').click();await page.waitForFunction(()=>!document.fullscreenElement);
  }
  await page.locator('#station-model .userInput').focus();previous=await state();await page.keyboard.press('ArrowLeft');await page.waitForTimeout(200);assert.notEqual((await state()).orbit.theta,previous.orbit.theta);
  await page.locator('[data-view="overview"]').click();
  if(shotDir){await page.evaluate(()=>{document.activeElement.blur();window.scrollTo(0,0)});await page.screenshot({path:shotDir+'/desktop.png',fullPage:true});}
  await page.setViewportSize({width:390,height:844});await page.locator('[data-view="overview"]').click();await page.waitForTimeout(350);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  if(shotDir){await page.evaluate(()=>{document.activeElement.blur();window.scrollTo(0,0)});await page.screenshot({path:shotDir+'/mobile.png',fullPage:true});}
  assert.deepEqual(errors,[]);
  const external3D=requests.filter(u=>/^https?:/.test(u)&&!u.startsWith(base)&&/model-viewer|draco|\.glb/.test(u));assert.deepEqual(external3D,[]);
  // A failed GLB request must leave the poster and recover with Retry.
  const errorPage=await context.newPage();await errorPage.route('**/moag041-v05.glb*',r=>r.fulfill({status:503,body:'Unavailable'}));
  await errorPage.goto(route);await errorPage.locator('#load-model').click();await errorPage.locator('#retry-model').waitFor({state:'visible'});
  assert(await errorPage.locator('#model-cover').isVisible());assert.equal(await errorPage.locator('#model-stage').getAttribute('aria-busy'),null);
  await errorPage.unroute('**/moag041-v05.glb*');await errorPage.locator('#retry-model').click();await errorPage.waitForFunction(()=>document.querySelector('#station-model').loaded,null,{timeout:90000});
  // Decoder initialization failures are cached inside the runtime: Retry must reload it.
  const decoderPage=await context.newPage();await decoderPage.route('**/draco_decoder.wasm',r=>r.fulfill({status:503,body:'Unavailable'}));
  await decoderPage.goto(route);await decoderPage.locator('#load-model').click();await decoderPage.locator('#retry-model').waitFor({state:'visible',timeout:60000});
  await decoderPage.unroute('**/draco_decoder.wasm');await decoderPage.locator('#retry-model').click();await decoderPage.waitForFunction(()=>document.querySelector('#station-model').loaded,null,{timeout:90000});
  assert.equal(new URL(decoderPage.url()).searchParams.get('load3d'),null);
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const fallback=await nojs.newPage();await fallback.goto(route);assert(await fallback.locator('noscript .noscript-note').isVisible());assert(await fallback.locator('.model-cover img').isVisible());
  console.log('PASS: gallery entry, lazy loading, actual GLB, mouse and keyboard rotation, zoom, 5 views, auto-rotation, fullscreen, mobile layout, local decoder, GLB and Draco failure/retry, no-JS fallback.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
