// On-device storage for static hosting (e.g. iPhone home-screen app).
// IndexedDB is used instead of localStorage: exam history stores question
// snapshots and can outgrow localStorage's ~5MB quota.
const DB='fde-cid-study',STORE='kv',STATE='progress';
let opened=null;
function open(){
  if(opened)return opened;
  opened=new Promise((resolve,reject)=>{
    if(typeof indexedDB==='undefined'){reject(new Error('当前浏览器不支持本机存储，请使用 Safari 打开'));return;}
    const req=indexedDB.open(DB,1);
    req.onupgradeneeded=()=>req.result.createObjectStore(STORE);
    req.onsuccess=()=>{const db=req.result;db.onversionchange=()=>{db.close();opened=null;};resolve(db);};
    req.onerror=()=>{opened=null;reject(new Error('无法打开本机存储：'+(req.error?.message||'未知错误')));};
    req.onblocked=()=>{opened=null;reject(new Error('本机存储被其他窗口占用，请关闭其他标签页后重试'));};
  });
  return opened;
}
const done=tx=>new Promise((resolve,reject)=>{tx.oncomplete=resolve;tx.onabort=tx.onerror=()=>reject(new Error('本机保存失败：'+(tx.error?.message||'存储空间可能不足')));});
export async function readState(){
  const db=await open();const tx=db.transaction(STORE,'readonly');const req=tx.objectStore(STORE).get(STATE);
  await done(tx);return req.result??null;
}
// Mirrors server.py: reject a write based on a stale revision, otherwise bump it.
export async function writeState(state){
  const db=await open();const tx=db.transaction(STORE,'readwrite');const kv=tx.objectStore(STORE);
  let revision=null,conflict=false;
  const get=kv.get(STATE);
  get.onsuccess=()=>{
    const current=get.result?.revision||0;
    if((state.revision||0)!==current){conflict=true;tx.abort();return;}
    revision=current+1;kv.put({...state,revision},STATE);
  };
  try{await done(tx);}catch(error){if(conflict)throw new Error('另一窗口已更新记录。请先导出当前记录，再刷新合并。');throw error;}
  return revision;
}
export async function requestPersistence(){
  try{if(navigator.storage?.persist&&!(await navigator.storage.persisted()))return await navigator.storage.persist();return true;}catch{return false;}
}
