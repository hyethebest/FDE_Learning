// Static phone build (GitHub Pages layout, no server.py): on-device storage, offline, touch layout.
// Usage: sh scripts/build_static.sh && node tests/phone.browser.mjs
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {tmpdir} from 'node:os';
const runtime=process.env.PLAYWRIGHT_MODULE||'playwright';
const {chromium,devices}=await import(runtime);
const root=path.resolve(fileURLToPath(new URL('..',import.meta.url)));
const out=path.resolve(process.env.FDE_QA_OUT||path.join(root,'.test-artifacts'));await fs.mkdir(out,{recursive:true});
const port=Number(process.env.FDE_TEST_PORT||8879);assert(port!==8765);
// Serve _site under a sub-path, like https://<user>.github.io/FDE_Learning/
const temp=await fs.mkdtemp(path.join(tmpdir(),'fde-phone-'));
await fs.cp(path.join(root,'_site'),path.join(temp,'FDE_Learning'),{recursive:true});
const proc=spawn('python3',['-m','http.server',String(port),'--bind','127.0.0.1','--directory',temp],{stdio:'ignore'});
const base=`http://127.0.0.1:${port}/FDE_Learning/`;
for(let i=0;i<50;i++){try{if((await fetch(base)).ok)break;}catch{}await new Promise(r=>setTimeout(r,100));}
const results=[];let browser;
try{
 browser=await chromium.launch({headless:true});
 const bank=JSON.parse(await fs.readFile(path.join(root,'data/questions.json'),'utf8'));
 const quality=new Map(JSON.parse(await fs.readFile(path.join(root,'data/quality.json'),'utf8')).questions.map(q=>[q.id,q]));
 const rounds=JSON.parse(await fs.readFile(path.join(root,'data/rounds.json'),'utf8')).rounds[0];
 const core=bank.filter(q=>rounds.coreIds.includes(q.id)&&quality.get(q.id).examUse!=='hold');
 const context=await browser.newContext({...devices['iPhone 13'],acceptDownloads:true});
 const page=await context.newPage();
 const errors=[],external=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 page.on('request',r=>{if(!r.url().startsWith(base)&&!r.url().startsWith('data:'))external.push(r.url());});
 await page.goto(base);await page.locator('#stem').waitFor();
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
 await page.screenshot({path:path.join(out,'phone-study.png')});
 results.push('子路径静态托管可加载，无本地服务也能启动');

 assert(await page.locator('#install-tip').isVisible());await page.locator('#install-dismiss').tap();
 assert.equal(await page.locator('#install-tip').count(),0);results.push('添加到主屏幕提示可关闭');

 const first=core[0];
 await page.locator('#search').fill(first.id);await page.locator('#stem').waitFor();
 await page.locator(`label.option:has(input[value=${first.answer[0]}])`).tap();
 await page.locator('#submit').tap();await page.locator('.explanation').waitFor();
 await page.locator('#favorite').tap();await page.waitForFunction(()=>document.querySelector('#save-status')?.textContent==='已保存到本机');
 await page.screenshot({path:path.join(out,'phone-explanation.png'),fullPage:true});
 await page.reload();await page.locator('#stem').waitFor();
 assert.equal(await page.locator('#install-tip').count(),0);
 await page.locator('[data-page=favorites]').tap();assert.equal(await page.locator('#favorite').getAttribute('aria-pressed'),'true');
 const stored=await page.evaluate(()=>new Promise(r=>{const q=indexedDB.open('fde-study');q.onsuccess=()=>{const g=q.result.transaction('kv').objectStore('kv').get('progress');g.onsuccess=()=>r(g.result);};}));
 assert.equal(stored.records[first.id].attempts.length,1);assert(stored.records[first.id].favorite);
 results.push('触屏作答、收藏写入 IndexedDB，刷新后保留');

 await page.locator('[data-page=study]').tap();await page.locator('#search').fill('');
 assert(await page.locator('.keyboard-hint').isHidden());results.push('触屏设备隐藏键盘快捷键提示');
 await page.locator(`label.option`).first().tap();await page.locator('#submit').tap();
 const before=await page.locator('.question-meta span').nth(1).textContent();
 await page.locator('#next-after').tap();await page.waitForFunction(b=>document.querySelector('.question-meta span:nth-child(2)')?.textContent!==b,before);
 results.push('解析底部“下一题”按钮可用');

 // Offline: service worker serves the whole app and bank.
 await page.evaluate(()=>navigator.serviceWorker.ready);
 await page.reload();await page.locator('#stem').waitFor();
 assert(await page.evaluate(()=>!!navigator.serviceWorker.controller));
 await context.setOffline(true);
 await page.reload();await page.locator('#stem').waitFor();
 await page.locator(`label.option`).first().tap();await page.locator('#submit').tap();await page.locator('.explanation').waitFor();
 await page.waitForFunction(()=>document.querySelector('#save-status')?.textContent==='已保存到本机');
 await context.setOffline(false);
 results.push('断网后重新打开仍可刷题和保存');

 // Export (falls back to download where the share sheet is unavailable) and import a desktop backup.
 await page.locator('[data-page=backup]').tap();
 assert.equal(await page.locator('#recover').count(),0);
 assert((await page.locator('.reading-block').first().textContent()).includes('浏览器存储'));
 const dl=page.waitForEvent('download');await page.locator('#export').tap();const file=path.join(temp,'phone-backup.json');await (await dl).saveAs(file);
 const exported=JSON.parse(await fs.readFile(file,'utf8'));assert(exported.records[first.id].favorite);
 await page.getByText('上次导出：',{exact:false}).waitFor();results.push('导出备份并记录导出时间');
 const second=core[1],wrong=Object.keys(second.options).find(k=>!second.answer.includes(k));
 const desktop={schemaVersion:1,revision:7,records:{[second.id]:{attempts:[{at:Date.now()-3600000,answers:[wrong],correct:false,questionVersion:second.review.contentHash}],favorite:true}},sessions:[],activeExam:null,settings:{}};
 const desktopFile=path.join(temp,'desktop.json');await fs.writeFile(desktopFile,JSON.stringify(desktop));
 let unexpectedDownload=false;page.once('download',()=>{unexpectedDownload=true;});
 await page.locator('#import-file').setInputFiles(desktopFile);await page.getByText('已合并学习备份',{exact:true}).waitFor();
 await page.waitForFunction(()=>document.querySelector('#save-status')?.textContent==='已保存到本机');
 assert.equal(unexpectedDownload,false);
 await page.locator('[data-page=wrong]').tap();await page.locator('#search').fill(second.id);assert((await page.locator('#stem').textContent()).includes(second.stem));
 results.push('电脑版备份导入手机并合并，错题本可见，导入时不弹多余下载');

 // Short exam: timer bar stays reachable, answers survive reload.
 await page.locator('[data-page=exam]').tap();await page.locator('#start-short').tap();await page.locator('#timer').waitFor();
 await page.locator('label.option').first().tap();await page.waitForFunction(()=>document.querySelector('#save-status')?.textContent==='已保存到本机');
 await page.evaluate(()=>document.querySelector('#exam-map-buttons button:last-child').scrollIntoView({block:'end'}));
 const bar=await page.locator('.exam-bar').boundingBox();assert(bar.y>=0&&bar.y<5,'交卷栏应吸顶');
 await page.screenshot({path:path.join(out,'phone-exam.png')});
 await page.reload();await page.locator('#timer').waitFor();assert.equal(await page.locator('#exam-map-buttons .answered').count(),1);
 page.once('dialog',d=>d.accept());await page.locator('#finish').tap();await page.locator('.score').waitFor();
 results.push('短练计时栏吸顶、刷新续答、交卷计分');

 const se=await browser.newContext({...devices['iPhone SE']});const sp=await se.newPage();await sp.goto(base);await sp.locator('#stem').waitFor();
 assert.equal(await sp.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await sp.screenshot({path:path.join(out,'phone-se.png')});await se.close();
 results.push('iPhone SE 375px 无横向溢出');

 assert.deepEqual(errors,[]);results.push('无 JS 错误');
 assert.deepEqual(external,[]);results.push('无外部网络请求');
 console.log(JSON.stringify({ok:true,results,artifacts:out},null,2));
}finally{await browser?.close();proc.kill();}
