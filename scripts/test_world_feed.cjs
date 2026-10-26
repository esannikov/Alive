const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try {
  const page=await browser.newPage({viewport:{width:1440,height:1100}});
  let mode='filled';
  const items=Array.from({length:6},(_,i)=>({id:String(i),page:i%2?'robots/lon/':'characters/emma/',title:i%2?'Лон':'Эмма',author:'reviewer',createdAt:new Date(Date.now()-i*3600000).toISOString(),excerpt:i?'Тест отображения комментария к варианту.':'<img src=x onerror="alert(1)"> Тест безопасного текста'}));
  await page.route('https://raw.githubusercontent.com/**/recent-comments.json', r=>mode==='error'?r.abort():r.fulfill({contentType:'application/json',body:JSON.stringify({schemaVersion:1,items:mode==='empty'?[]:items})}));
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8769/World/');
  await page.locator('#recent-comments-list li').first().waitFor();
  assert.equal(await page.locator('#recent-comments-list li').count(),5);
  assert.equal(await page.locator('#recent-comments-list img').count(),0);
  assert.equal(await page.locator('#comments').count(),0);
  assert((await page.locator('.recent-comment-meta a').first().getAttribute('href')).endsWith('/World/characters/emma/#comments'));
  await page.screenshot({path:'/private/tmp/world-feed-desktop.png'});
  await page.setViewportSize({width:390,height:844});
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.screenshot({path:'/private/tmp/world-feed-mobile.png'});
  mode='empty';await page.reload();await page.getByText('Комментариев пока нет.',{exact:true}).waitFor();
  mode='error';await page.reload();await page.getByRole('button',{name:'Повторить',exact:true}).waitFor();
  assert.equal(await page.locator('#recent-comments-list li').count(),0);
  mode='filled';await page.getByRole('button',{name:'Повторить',exact:true}).click();await page.locator('#recent-comments-list li').first().waitFor();
  assert.deepEqual(errors,[]);
  console.log('PASS: five entries, object links, safe text, mobile, empty, error, retry; no external writes');
 } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exit(1)});
