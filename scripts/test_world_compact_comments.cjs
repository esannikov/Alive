/* Test the supported Giscus DOM contract with local composers. No GitHub writes. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const theme=fs.readFileSync('docs/World/giscus-compact.css','utf8').replace(/^@import.*$/m,'');
const composer=reply=>`<form class="gsc-comment-box ${reply?'gsc-comment-box-is-reply':''}" aria-label="${reply?'Reply':'New comment'}"><div class="gsc-comment-box-tabs"><button type="button">Редактирование</button><button type="button">Предварительный просмотр</button></div><div class="gsc-comment-box-main"><div class="gsc-comment-box-write"><textarea class="gsc-comment-box-textarea" aria-label="${reply?'Reply':'New comment'}"></textarea><div class="gsc-comment-box-textarea-extras">Markdown</div></div></div><div class="gsc-comment-box-bottom"><div class="gsc-comment-box-buttons">${reply?'<button type="button" class="cancel btn">Отмена</button>':''}<button type="submit" class="btn">${reply?'Ответ':'Комментарий'}</button></div></div></form>`;
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{
  for(const width of [1440,390]){
   const page=await browser.newPage({viewport:{width,height:900}});let submissions=0;
   await page.setContent(`<main><div class="gsc-main"><div class="gsc-comments"><div class="gsc-timeline">${[1,2].map(n=>`<article class="gsc-comment"><div><p>Существующее сообщение ${n}</p><div class="gsc-replies"><p>Существующий ответ</p></div><div class="gsc-reply-box"><button type="button">Ответить ${n}</button></div></div></article>`).join('')}</div>${composer(false)}</div></div></main>`);
   await page.addStyleTag({content:`*{box-sizing:border-box}body{background:#090a0b;color:#f3f3ef;font:14px sans-serif}.gsc-comments{display:flex;flex-direction:column}.gsc-comment-box-textarea{width:100%;min-height:100px}.gsc-comment-box{border:1px solid #444}button{padding:6px} ${theme}`});
   await page.evaluate(replyForm=>{
    document.querySelectorAll('.gsc-reply-box').forEach(trigger=>trigger.addEventListener('click',()=>{
     const form=document.createElement('div');form.innerHTML=replyForm;const editor=form.firstElementChild;trigger.replaceWith(editor);
     const close=()=>{editor.replaceWith(trigger);trigger.querySelector('button').focus();};
     editor.querySelector('.cancel').addEventListener('click',close);
     editor.addEventListener('submit',e=>{e.preventDefault();window.__submitted=(window.__submitted||0)+1;close();});
     editor.querySelector('textarea').focus();
    }));
    document.querySelector('.gsc-comments > form').addEventListener('submit',e=>e.preventDefault());
   },composer(true));
   await page.getByRole('textbox',{name:'New comment'}).fill('Сохранённый черновик');
   assert.equal(await page.locator('textarea:visible').count(),1);assert.equal(await page.getByRole('button',{name:'Редактирование'}).count(),0);
   assert.equal(await page.locator('textarea:visible').evaluate(el=>Math.round(el.getBoundingClientRect().height)),72);
   await page.getByRole('button',{name:'Ответить 1',exact:true}).click();
   assert.equal(await page.locator('textarea:visible').count(),1);assert.equal(await page.locator('.gsc-reply-box:visible').count(),0);
   await page.getByRole('textbox',{name:'Reply',exact:true}).fill('Ответ');
   await page.getByRole('button',{name:'Отмена',exact:true}).click();
   assert.equal(await page.locator('textarea:visible').count(),1);assert.equal(await page.getByRole('textbox',{name:'New comment'}).inputValue(),'Сохранённый черновик');
   await page.getByRole('button',{name:'Ответить 2',exact:true}).click();
   await page.getByRole('textbox',{name:'Reply',exact:true}).fill('Локальный тест');await page.getByRole('button',{name:'Ответ',exact:true}).click();
   assert.equal(await page.evaluate(()=>window.__submitted),1);assert.equal(await page.locator('textarea:visible').count(),1);
   assert.equal(await page.getByRole('textbox',{name:'New comment'}).inputValue(),'Сохранённый черновик');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   assert.equal(await page.getByText('Существующий ответ',{exact:true}).count(),2);
   await page.close();
  }
  console.log('PASS: one visible editor, compact height, reply/cancel/local submit, preserved main draft and replies, mobile; external writes=0');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
