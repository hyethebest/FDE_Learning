// AI FDE (type=CID) bank at cid/: study, notes, exam, and isolation from the ADP app on the same origin.
// Usage: sh scripts/build_static.sh && node tests/cid.browser.mjs
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
const port=Number(process.env.FDE_CID_TEST_PORT||8880);assert(port!==8765);
const temp=await fs.mkdtemp(path.join(tmpdir(),'fde-cid-'));
await fs.cp(path.join(root,'_site'),path.join(temp,'FDE_Learning'),{recursive:true});
const proc=spawn('python3',['-m','http.server',String(port),'--bind','127.0.0.1','--directory',temp],{stdio:'ignore'});
const site=`http://127.0.0.1:${port}/FDE_Learning/`,base=site+'cid/';
for(let i=0;i<50;i++){try{if((await fetch(base)).ok)break;}catch{}await new Promise(r=>setTimeout(r,100));}
const bank=JSON.parse(await fs.readFile(path.join(root,'cid/data/questions.json'),'utf8'));
const results=[];let browser;
const saved=p=>p.waitForFunction(()=>document.querySelector('#save-status')?.textContent==='已保存到本机');
const dbRead=(p,name)=>p.evaluate(n=>new Promise(r=>{const q=indexedDB.open(n);q.onupgradeneeded=()=>{};q.onsuccess=()=>{const db=q.result;if(!db.objectStoreNames.contains('kv')){r(null);return;}const g=db.transaction('kv').objectStore('kv').get('progress');g.onsuccess=()=>r(g.result||null);};}),name);
try{
 browser=await chromium.launch({headless:true});
 for(const device of ['iPhone 13','Pixel 7']){
  const context=await browser.newContext({...devices[device],acceptDownloads:true});const page=await context.newPage();
  const errors=[],external=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  page.on('request',r=>{if(!r.url().startsWith(site)&&!r.url().startsWith('data:'))external.push(r.url());});
  await page.goto(base);await page.locator('#stem').waitFor();
  assert.equal(await page.title(),'AI FDE 备考');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  assert.equal(await page.locator('[data-page=notes]').count(),1);
  // Answer a known question and check explanation + course source.
  const q=bank.find(x=>x.type==='single');
  await page.locator('#search').fill(q.id);await page.locator('#stem').waitFor();
  await page.locator(`label.option:has(input[value=${q.answer[0]}])`).tap();await page.locator('#submit').tap();
  await page.locator('.explanation').waitFor();
  assert((await page.locator('.explanation h2').textContent()).includes('回答正确'));
  assert.equal(await page.locator('.sources a').first().getAttribute('href'),q.sources[0].url);
  assert((await page.locator('.sources h3').textContent()).includes('课程依据'));
  await saved(page);
  if(device==='iPhone 13')await page.screenshot({path:path.join(out,'cid-explanation.png'),fullPage:true});
  results.push(`${device}：作答、解析、课程依据链接正常`);
  // Notes → practise one section.
  await page.locator('[data-page=notes]').tap();await page.locator('.notes-module').first().waitFor();
  const note=page.locator('details.note').first();await note.locator('summary').tap();
  const sec=await note.locator('.practice-section').getAttribute('data-section');
  const expected=bank.filter(x=>x.section===sec).length;
  if(device==='iPhone 13')await page.screenshot({path:path.join(out,'cid-notes.png')});
  await note.locator('.practice-section').tap();await page.locator('#stem').waitFor();
  assert((await page.locator('.section-chip').textContent()).includes(sec));
  assert.equal(await page.locator('.question-meta span').nth(1).textContent(),`1 / ${expected}`);
  await page.goBack();assert.equal(await page.locator('.nav-button.active').getAttribute('data-page'),'notes');
  results.push(`${device}：要点速览展开小节并跳到本节 ${expected} 题，返回键回到要点`);
  // Full mock exam: 60 questions, 120 minutes.
  await page.locator('[data-page=exam]').tap();
  assert((await page.locator('.exam-facts').textContent()).includes('120'));
  await page.locator('#start-exam').tap();await page.locator('#timer').waitFor();
  assert.equal(await page.locator('#exam-map-buttons button').count(),60);
  assert(/^(119|120):/.test(await page.locator('#timer').textContent()));
  page.once('dialog',d=>d.accept());await page.locator('#finish').tap();await page.locator('.score').waitFor();
  results.push(`${device}：60 题 120 分钟模拟可开考、交卷`);
  // Storage is separate from the ADP app on the same origin.
  const cidState=await dbRead(page,'fde-cid-study');assert(cidState.records[q.id]);assert.equal(cidState.sessions.length,1);
  await page.goto(site);await page.locator('#stem').waitFor();
  const adpState=await dbRead(page,'fde-study');assert(!adpState||!Object.keys(adpState.records).some(id=>id.startsWith('CID-')));
  results.push(`${device}：与 ADP 题库的学习记录互不混用`);
  // Offline: each app keeps its own worker/cache.
  await page.goto(base);await page.locator('#stem').waitFor();await page.evaluate(()=>navigator.serviceWorker.ready);
  await page.reload();await page.locator('#stem').waitFor();
  await page.goto(site);await page.locator('#stem').waitFor();await page.evaluate(()=>navigator.serviceWorker.ready);await page.reload();await page.locator('#stem').waitFor();
  const caches=await page.evaluate(()=>caches.keys());assert(caches.some(k=>k.startsWith('fde-cid-')));assert(caches.some(k=>k.startsWith('fde-study-')));
  await context.setOffline(true);
  await page.goto(base);await page.locator('#stem').waitFor();assert.equal(await page.title(),'AI FDE 备考');
  await page.goto(site);await page.locator('#stem').waitFor();assert.notEqual(await page.title(),'AI FDE 备考');
  await context.setOffline(false);
  results.push(`${device}：断网后两个题库各自离线可用，缓存互不覆盖`);
  // A backup from the other exam is refused.
  await page.goto(base);await page.locator('#stem').waitFor();await page.locator('[data-page=backup]').tap();
  const adpBackup=path.join(temp,'adp.json');await fs.writeFile(adpBackup,JSON.stringify({schemaVersion:1,revision:1,records:{'FDE-M1-001':{attempts:[],favorite:true}},sessions:[],activeExam:null,settings:{}}));
  await page.locator('#import-file').setInputFiles(adpBackup);await page.getByText('这是另一门考试（ADP FDE）的备份，不能导入本题库',{exact:true}).waitFor();
  results.push(`${device}：拒绝导入另一门考试的备份`);
  assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
  results.push(`${device}：无 JS 错误、无外部请求`);
  await context.close();
 }
 console.log(JSON.stringify({ok:true,results,artifacts:out},null,2));
}finally{await browser?.close();proc.kill();}
