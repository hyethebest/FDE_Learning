export const MODULES = [
  ['M1','AI 与生成式 AI 基础',10],['M2','ADP 产品定位与能力边界',7],['M3','ADP 核心功能与应用搭建',22],['M4','场景理解与方案设计',25],['M5','行业解决方案与案例落地',15],['M6','交付实施、评测与运维',11],['M7','安全合规与责任 AI',10]
];
export const isCorrect = (given, correct) => Array.isArray(given) && given.length === correct.length && [...given].sort().join('|') === [...correct].sort().join('|');
export function currentRecord(state, question) {
  const old=state.records[question.id]||{attempts:[],favorite:false};
  const version=question.review?.contentHash || question.version || '2026-10-09';
  const attempts=old.attempts.filter(a=>a.questionVersion===version);
  const result={...old,attempts,lastCorrect:undefined,due:undefined,streak:0};
  for(const a of attempts)result.streak=a.correct?result.streak+1:0;
  const last=attempts.at(-1);
  if(last){result.lastCorrect=last.correct;result.due=last.at+(last.correct?[1,3,7,14,30][Math.min(result.streak-1,4)]*86400000:600000);}
  return result;
}
export function recordAnswer(state, question, answers, now=Date.now()) {
  const old = state.records[question.id] || {attempts:[], streak:0, favorite:false};
  old.streak=currentRecord(state,question).streak;
  const correct = isCorrect(answers, question.answer);
  old.attempts.push({at:now,answers:[...answers],correct,questionVersion:question.review?.contentHash || question.version || '2026-10-09'});
  old.streak = correct ? (old.streak||0)+1 : 0;
  old.due = now + (correct ? [1,3,7,14,30][Math.min(old.streak-1,4)]*86400000 : 600000);
  old.lastCorrect = correct;
  state.records[question.id] = old;
  return correct;
}
export function shuffle(array, random=Math.random) {
  const result = [...array]; for(let i=result.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[result[i],result[j]]=[result[j],result[i]];}return result;
}
export const EXAM_PROFILES = {
 full:{single:40,multiple:20,minutes:90,singlePoints:1.5,multiplePoints:2,label:'60题完整练习'},
 short:{single:10,multiple:5,minutes:25,singlePoints:6,multiplePoints:8,label:'15题短练（本地计分）'}
};
export function makeExam(questions, now=Date.now(), random=Math.random, mode='full') {
  const profile=EXAM_PROFILES[mode];if(!profile)throw new Error('未知练习模式');
  questions=questions.filter(q=>!q.quality || q.quality.examUse==='eligible');
  const single = questions.filter(q=>q.type==='single'), multiple=questions.filter(q=>q.type==='multiple');
  if(single.length<profile.single||multiple.length<profile.multiple) throw new Error(`可组卷题库不足 ${profile.single} 道单选和 ${profile.multiple} 道多选，暂不能组卷。`);
  // Largest-remainder target by official module proportions; fill from remaining pool if necessary.
  const choose = (pool,n) => {
    const picked=[]; const targets=MODULES.map(([id,,weight])=>({id,n:Math.floor(n*weight/100),r:n*weight/100%1}));
    let remaining=n-targets.reduce((a,x)=>a+x.n,0);
    [...targets].sort((a,b)=>b.r-a.r).slice(0,remaining).forEach(t=>t.n++);
    targets.forEach(t=>picked.push(...shuffle(pool.filter(q=>q.module===t.id),random).slice(0,t.n)));
    picked.push(...shuffle(pool.filter(q=>!picked.includes(q)),random).slice(0,n-picked.length));
    return shuffle(picked,random);
  };
  const selected=[...choose(single,profile.single),...choose(multiple,profile.multiple)];
  return {id:'exam-'+now,mode,startedAt:now,deadline:now+profile.minutes*60000,ids:selected.map(q=>q.id),snapshot:structuredClone(selected),answers:{},index:0};
}
export function gradeExam(exam, byId, now=Date.now()) {
  const profile=EXAM_PROFILES[exam.mode||'full'];if(!profile)throw new Error('未知练习模式');
  let points=0,correct=0; const results=[];
  const frozen=new Map((exam.snapshot||[]).map(q=>[q.id,q]));
  for(const id of exam.ids){const q=frozen.get(id)||byId.get(id);if(!q)throw new Error('试卷题目缺失，请恢复原题库版本后交卷');const ok=isCorrect(exam.answers[id]||[],q.answer);if(ok){correct++;points+=q.type==='single'?profile.singlePoints:profile.multiplePoints;}results.push({id,correct:ok,answers:exam.answers[id]||[],question:structuredClone(q)});}
  return {id:exam.id,mode:exam.mode||'full',bankVersion:exam.bankVersion||'legacy',startedAt:exam.startedAt,finishedAt:now,points,correct,total:exam.ids.length,results};
}
const choiceList=value=>Array.isArray(value)&&value.length<=5&&new Set(value).size===value.length&&value.every(k=>['A','B','C','D','E'].includes(k));
const object=value=>value&&typeof value==='object'&&!Array.isArray(value);
function validateQuestion(q){
  if(!object(q)||!['id','stem','topic','difficulty','explanation'].every(k=>typeof q[k]==='string')||!['single','multiple'].includes(q.type)||!object(q.options)||!['ABCD','ABCDE'].includes(Object.keys(q.options).sort().join(''))||!Object.values(q.options).every(v=>typeof v==='string')||!choiceList(q.answer)||(q.type==='single'?q.answer.length!==1:q.answer.length<2||q.answer.length>=Object.keys(q.options).length)||q.answer.some(k=>!Object.hasOwn(q.options,k))||!object(q.distractors)||!Object.values(q.distractors).every(v=>typeof v==='string')||!Array.isArray(q.sources)||!q.sources.length)throw new Error('备份题目快照无效');
  for(const source of q.sources){if(!object(source)||!['url','title','section','fact','verifiedAt','version'].every(k=>typeof source[k]==='string')||!/^https:\/\/(cloud\.tencent\.com|adp\.tencent\.com)\//.test(source.url))throw new Error('备份题目来源无效');}
}
export function validateBackup(value){
  if(!object(value)||value.schemaVersion!==1||!object(value.records)||!Array.isArray(value.sessions))throw new Error('不是受支持的学习备份');
  for(const [id,r] of Object.entries(value.records)){if(['__proto__','constructor','prototype'].includes(id)||!object(r)||!Array.isArray(r.attempts))throw new Error('备份题目记录无效：'+id);for(const a of r.attempts){if(!object(a)||!Number.isFinite(a.at)||typeof a.correct!=='boolean'||!choiceList(a.answers))throw new Error('备份答题记录无效：'+id);}}
  for(const s of value.sessions){
    if(s.mode!==undefined&&!EXAM_PROFILES[s.mode])throw new Error('备份历史练习模式无效');
    if(!object(s)||typeof s.id!=='string'||!Number.isFinite(s.points)||s.points<0||s.points>100||!Number.isFinite(s.finishedAt)||!Number.isFinite(s.startedAt)||!Number.isInteger(s.total)||!Number.isInteger(s.correct)||s.correct<0||s.correct>s.total||!Array.isArray(s.results)||s.total!==s.results.length)throw new Error('备份考试历史无效');
    for(const r of s.results){if(!object(r)||typeof r.id!=='string'||!choiceList(r.answers)||typeof r.correct!=='boolean')throw new Error('备份考试复盘无效');if(r.question){validateQuestion(r.question);if(r.question.id!==r.id)throw new Error('备份历史题目ID不一致');}}
  }
  if(value.activeExam){
    const x=value.activeExam;const profile=EXAM_PROFILES[x.mode||'full'];if(!profile)throw new Error('备份练习模式无效');const count=profile.single+profile.multiple;
    if(!object(x)||typeof x.id!=='string'||!Number.isFinite(x.startedAt)||!Array.isArray(x.ids)||x.ids.length!==count||!x.ids.every(id=>typeof id==='string')||new Set(x.ids).size!==count||!Number.isFinite(x.deadline)||!Number.isInteger(x.index)||x.index<0||x.index>=count||!object(x.answers)||Object.entries(x.answers).some(([id,a])=>!x.ids.includes(id)||!choiceList(a)))throw new Error('备份试卷无效');
    if(x.snapshot!==undefined){if(!Array.isArray(x.snapshot)||x.snapshot.length!==count||new Set(x.snapshot.map(q=>q?.id)).size!==count)throw new Error('备份题目快照无效');for(const q of x.snapshot){validateQuestion(q);if(!x.ids.includes(q.id))throw new Error('备份快照与试卷不一致');}}
  }
  return value;
}
function recalculateRecord(record){
  let streak=0;for(const a of record.attempts)streak=a.correct?streak+1:0;
  const last=record.attempts.at(-1);record.streak=streak;
  if(last){record.lastCorrect=last.correct;record.due=last.at+(last.correct?[1,3,7,14,30][Math.min(streak-1,4)]*86400000:600000);}
  return record;
}
export function mergeBackup(current,incoming,{recoverActive=false}={}){
  validateBackup(incoming); const merged=structuredClone(current);
  for(const [id,r] of Object.entries(incoming.records)){
    const old=merged.records[id]; if(!old){merged.records[id]=recalculateRecord(structuredClone(r));continue;}
    const attempts=[...old.attempts,...r.attempts].filter((a,i,arr)=>arr.findIndex(b=>b.at===a.at&&b.questionVersion===a.questionVersion&&JSON.stringify(b.answers)===JSON.stringify(a.answers))===i).sort((a,b)=>a.at-b.at);
    const latest=(r.attempts.at(-1)?.at||0)>(old.attempts.at(-1)?.at||0)?r:old;
    merged.records[id]=recalculateRecord({...latest,attempts,favorite:!!(old.favorite||r.favorite)});
  }
  merged.sessions=[...current.sessions,...incoming.sessions].filter((s,i,arr)=>arr.findIndex(t=>t.id===s.id)===i);
  const completed=new Set(merged.sessions.map(s=>s.id));
  if(merged.activeExam&&completed.has(merged.activeExam.id))merged.activeExam=null;
  if(incoming.activeExam&&!completed.has(incoming.activeExam.id)&&(!merged.activeExam||(recoverActive&&merged.activeExam.id===incoming.activeExam.id)))merged.activeExam=structuredClone(incoming.activeExam);
  return merged;
}
