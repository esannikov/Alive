const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try {
  const feed=JSON.parse(fs.readFileSync('docs/World/recent-comments.json','utf8'));
  let fail=false, requests=0;
  const stats=Object.fromEntries(Object.keys(feed.discussionStats).map(p=>[p,{messageCount:0,last:null}]));
  stats['characters/fedor/']={messageCount:5,last:{author:'isto3110-ship-it-with-a-very-long-display-name',createdAt:'2026-10-26T22:15:00Z'}};
  stats['characters/kolka/']={messageCount:2,last:{author:'ElenaAlive',createdAt:'2026-10-26T19:40:31Z'}};
  const context=await browser.newContext();
  await context.route('https://raw.githubusercontent.com/**/recent-comments.json*',r=>{requests++;return fail?r.abort():r.fulfill({contentType:'application/json',body:JSON.stringify({...feed,discussionStats:stats})});});
  await context.route('https://giscus.app/**',r=>r.abort());
  for(const width of [1440,768,390,320]){
   const page=await context.newPage();await page.setViewportSize({width,height:1000});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   const before=requests;await page.goto('http://127.0.0.1:8769/World/');
   await page.locator('[data-discussion-summary="characters/fedor/"][data-loaded]').waitFor();
   assert.equal(requests-before,1,'Cards and recent feed must share one request');
   const row=page.locator('[data-discussion-summary="characters/fedor/"]');
   assert.equal(await row.locator('.card-discussion-count').innerText(),'5');
   assert.equal(await row.locator('time').innerText(),'27.10.26 00:15');
   assert((await row.getAttribute('aria-label')).includes('5 сообщений'));
   assert((await row.getAttribute('title')).includes('isto3110-ship-it-with-a-very-long-display-name'));
   assert.equal(await page.locator('[data-discussion-summary="ships/moag/"] time').count(),0);
   assert.equal(await page.locator('[data-discussion-summary="ships/moag/"] .card-discussion-count').innerText(),'0');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   assert(await page.locator('.card-discussion').evaluateAll(rows=>rows.every(r=>r.scrollWidth<=r.clientWidth+1 && r.offsetHeight<=32)),'One line without card overflow');
   assert(await row.evaluate(r=>r.previousElementSibling.className==='card-meta'&&r.nextElementSibling.classList.contains('button')));
   await row.scrollIntoViewIfNeeded();await page.screenshot({path:`/private/tmp/world-card-comments-${width}.png`});
   await row.click();assert(page.url().endsWith('/characters/fedor/#comments'));
   assert.deepEqual(errors,[]);await page.close();
  }
  const p=await context.newPage();await p.goto('http://127.0.0.1:8769/World/work.html');await p.locator('[data-discussion-summary][data-loaded]').first().waitFor();
  fail=true;await p.goto('http://127.0.0.1:8769/World/');await p.getByText('Комментарии недоступны',{exact:true}).first().waitFor();assert.equal(await p.locator('.card-discussion-count').count(),0);
  fail=false;await p.getByRole('button',{name:'Повторить',exact:true}).click();await p.locator('[data-discussion-summary][data-loaded]').first().waitFor();
  console.log('PASS: all cards, replies counted, Kyiv date/time, long names, one line at 1440/768/390/320, shared request, links, work page, error/retry');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
