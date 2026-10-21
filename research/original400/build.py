from review import *
import notes_a,notes_b,notes_c,refinements
from collections import Counter
import shutil
APP=BASE.parent/'app';OUT=BASE.parent.parent/'outputs';DEST=APP/'research/original400';DEST.mkdir(parents=True,exist_ok=True)
VERSION='2026.10.13.3';DATE='2026-10-13'
def read(name):return json.loads((BASE/'before'/name).read_text())
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def content(q):return {k:v for k,v in q.items() if k!='review'}
def digest(q):return hashlib.sha256(json.dumps(content(q),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
rounds=read('rounds.json');r=rounds['rounds'][0];ids=set(r['retainedCoreIds']);assert set(reviews)==ids and len(ids)==400
bank=copy.deepcopy(old);audit=read('quality.json');aud={x['id']:x for x in audit['questions']};ledger=[];changes=[]
for q in bank:
 ident=q['id']
 if ident not in ids:continue
 original=by[ident];p=copy.deepcopy(patches.get(ident,{}));teaching=p.pop('teachingNote',None)
 if teaching and 'explanation' not in p:p['explanation']=q['explanation']+' 判断要点：'+teaching.replace('保留','')
 q.update(p)
 fields=[k for k in content(q) if q[k]!=original[k]];changed=bool(fields)
 assert changed==(reviews[ident]['decision']=='revise'),ident
 meta={'date':DATE,'version':VERSION,'action':'修订' if changed else '保留','finding':reviews[ident]['finding'],'reviewer':'同一助手逐题内容复核；不是独立审校','sourceScope':'重点官方资料重新读取，其余沿用既有来源证据；各来源日期未统一刷新'}
 q['review']['previousReview']=copy.deepcopy(original['review'])
 q['review'].update({'reviewer':meta['reviewer'],'checkedAt':DATE,'recheck':meta,'contentHash':digest(q)})
 a=aud[ident];a['previousAudit']=copy.deepcopy(a)
 a.update({'reviewer':meta['reviewer'],'verifiedAt':DATE,'contentHash':digest(q),'questionHash':digest(q),'original400Review':meta,'rationale':reviews[ident]['finding']+' 本次单助手复核，难度与真实考试的等值性未验证。'})
 row={'id':ident,'module':q['module'],'topic':q['topic'],'decision':meta['action'],'finding':meta['finding'],'changedFields':fields,'beforeHash':digest(original),'afterHash':digest(q),'sourceUrls':[s['url'] for s in q['sources']]};ledger.append(row)
 if changed:changes.append({**row,'before':{k:original[k] for k in fields},'after':{k:q[k] for k in fields}})
assert len(changes)==118
assert all(q==by[q['id']] for q in bank if q['id'] not in ids)
summary={'version':VERSION,'date':DATE,'reviewed':400,'revised':len(changes),'retained':400-len(changes),'reviewer':'同一助手逐题内容复核；非独立审校','modules':{m:{'reviewed':sum(x['module']==m for x in ledger),'revised':sum(x['module']==m for x in changes)} for m in ['M1','M2','M3','M4','M5','M6','M7']},'fieldCounts':dict(Counter(k for x in changes for k in x['changedFields'])),'scope':'全部400题的题干、选项、答案、解析及干扰项理由逐题检查；重点官方页面重新读取，不等于96个历史来源全部再次联网验证。'}
r.update({'version':VERSION,'recheckedOriginalIds':r['retainedCoreIds'],'revisedOriginalIds':[x['id'] for x in changes],'originalReview':summary})
manifest=read('manifest.json');manifest.update({'version':VERSION,'original400Review':summary})
manifest['notes'][1]='核心500题：原400题全部逐题复核（118修订、282保留），加此前重写100题；其余458仅学习、42待修订。'
manifest['notes'].append('原400题本次为单助手复核，保留逐题理由和118题字段差异；来源日期按实际核对记录保留。')
write(APP/'data/questions.json',bank)
audit.update({'version':VERSION,'checkedAt':DATE,'reviewerType':'原400题本次单助手内容复核（118修订）；另100题此前单助手课程核对；旧独立AI审校仅为历史记录','bankSha256':hashlib.sha256((APP/'data/questions.json').read_bytes()).hexdigest()})
for name,d in [('quality.json',audit),('manifest.json',manifest),('rounds.json',rounds)]:write(APP/'data'/name,d)
export={'version':VERSION,'notice':'原创训练题：原400题本次逐题复核，其中118修订、282保留；另100题此前课程校准重写。均非本次独立审校或官方题。','count':500,'questions':[q for q in bank if q['id'] in r['coreIds']]}
write(APP/'data/core500-export.json',export);write(OUT/'FDE核心500题_第一次优化.json',export)
write(DEST/'review-ledger.json',{'summary':summary,'questions':ledger});write(DEST/'item-changes.json',changes)
write(OUT/'原400题逐题复核记录.json',{'summary':summary,'questions':ledger});write(OUT/'原400题修订差异.json',changes)
for f in BASE.glob('*.py'):shutil.copy2(f,DEST/f.name)
shutil.copytree(BASE/'before',DEST/'before',dirs_exist_ok=True)
print(json.dumps(summary,ensure_ascii=False,indent=2))
