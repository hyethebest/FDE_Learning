import {validateBackup} from './core.js';
import {readState,writeState} from './device-db.js';
const KEY='fde-cid-recovery-v1',ARCHIVE='fde-cid-unmerged-v1';
const emptyState=()=>({schemaVersion:1,revision:0,records:{},sessions:[],activeExam:null,settings:{}});
// mode 'server': local server.py owns progress.json (desktop, unchanged behaviour).
// mode 'device': static hosting (iPhone home-screen app); progress lives in this browser's IndexedDB.
export class Store {
  constructor(){this.state=null;this.mode='server';this.queue=Promise.resolve();this.onStatus=()=>{};this.failed=false;this.pending=0;this.recoverySnapshot=null;}
  async load(){
    // The static build marks itself so phones never probe for a server that isn't there.
    const staticBuild=typeof document!=='undefined'&&document.querySelector('meta[name="fde-storage"]')?.content==='device';
    let response=null;if(!staticBuild){try{response=await fetch('./api/state');}catch{}}
    let disk;
    if(response&&response.status!==404){
      if(!response.ok)throw new Error((await response.json()).error);
      try{disk=await response.json();}catch{disk=undefined;}
    }
    if(disk===undefined){this.mode='device';this.state=validateBackup((await readState())||emptyState());return this.state;}
    this.state=validateBackup(disk);
    try{const archived=JSON.parse(localStorage.getItem(ARCHIVE)||'null'),cached=JSON.parse(localStorage.getItem(KEY)||'null');const candidate=archived||(cached&&cached.revision>=this.state.revision?cached:null);if(candidate&&JSON.stringify(candidate)!==JSON.stringify(this.state)){validateBackup(candidate);this.recoverySnapshot=candidate;try{localStorage.setItem(ARCHIVE,JSON.stringify(candidate));}catch{}}}catch{}
    return this.state;
  }
  cache(){if(this.mode==='device')return true;try{localStorage.setItem(KEY,JSON.stringify(this.state));return true;}catch{return false;}}
  async persist(snapshot){
    if(this.mode==='device')return writeState(snapshot);
    const res=await fetch('./api/state',{method:'PUT',headers:{'Content-Type':'application/json','X-FDE-Client':'offline-study'},body:JSON.stringify(snapshot)});
    const payload=await res.json();if(!res.ok)throw new Error(payload.error);
    return payload.revision;
  }
  save(){
    this.cache();this.pending++;this.onStatus('正在保存…');
    this.queue=this.queue.then(async()=>{
      const snapshot=structuredClone(this.state);
      this.state.revision=await this.persist(snapshot);this.failed=false;
      this.cached=this.cache();
    }).catch(error=>{this.failed=true;this.onStatus(error.message+' · 请导出备份',true);}).finally(()=>{this.pending--;if(this.pending)this.onStatus('正在保存…');else if(!this.failed)this.onStatus(this.cached?'已保存到本机':'已保存到本机；浏览器应急副本空间不足',false);});
    return this.queue;
  }
  clearRecovery(){this.recoverySnapshot=null;try{localStorage.removeItem(ARCHIVE);}catch{}}
  recovery(){if(this.recoverySnapshot)return this.recoverySnapshot;if(this.mode==='device')return null;try{return JSON.parse(localStorage.getItem(KEY)||'null');}catch{return null;}}
}
