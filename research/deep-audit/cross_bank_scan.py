#!/usr/bin/env python3
"""Deterministic lexical candidate generation; AI review separate, no embedding calls."""
import json,re,math,hashlib,itertools,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent

def norm(s):return re.sub(r'[\W_]','',s).lower()
def grams(s,n=2):
 s=norm(s);return {s[i:i+n] for i in range(max(0,len(s)-n+1))}
def jac(a,b):return len(a&b)/len(a|b) if a|b else 0
def contain(a,b):return len(a&b)/min(len(a),len(b)) if a and b else 0

# Transparent domain anchor retrieval; conjunctions, not a semantic verdict.
ANCHORS={
 'memory_rebind':[['记忆库','旧库','新库'],['改绑','更换','切换读写','读写范围'],['迁移','复制','同步']],
 'memory_disable':[['记忆'],['关闭','开关'],['保留','停止读写','清空']],
 'memory_share':[['记忆库','同库'],['同一用户','同一个','同一记忆库','同库'],['一致','共享','跨应用']],
 'output_token_limit':[['最大回复','输出长度','回复长度'],['token','Token']],
 'subworkflow_reuse':[['子工作流','子流程','工作流节点','公共流程'],['复用','集中维护','公共','已有审核']],
 'mcp_empty_tools':[['mcp','MCP'],['空数组','列表为空','空列表']],
 'skillhub_update':[['SkillHub','skillhub'],['更新','版本']],
 'published_app_single_turn':[['应用'],['工具','封装'],['单轮','多轮']],
 'references_load':[['references'],['按需','需要加载','任务需要','参考']],
 'web_async':[['网页'],['异步']],
 'web_login':[['网页'],['登录','授权验证']],
 'json_serialization':[['json','JSON','序列化'],['输出','结果','返回']]
}
def anchors(q):
 text=q['stem']+' '+ ' '.join(q['options'][k] for k in q['answer'])+' '+ ' '.join(s['fact'] for s in q['sources'])
 return {key for key,groups in ANCHORS.items() if all(any(t in text for t in terms) for terms in groups)}

def scan():
 snapshot=OUT/'cross-bank-snapshot.json'
 if not snapshot.exists():snapshot.write_bytes((ROOT/'data/questions.json').read_bytes())
 qs=json.loads(snapshot.read_text())
 texts=[x['topic']+' '+x['stem']+' '+ ' '.join(x['options'][k] for k in x['answer'])+' '+ ' '.join(s['fact'] for s in x['sources']) for x in qs]
 gs=[grams(s) for s in texts];df=collections.Counter(g for s in gs for g in s)
 w={g:math.log((len(qs)+1)/(n+1))+1 for g,n in df.items()}
 vec=[{g:w[g] for g in s} for s in gs];lens=[math.sqrt(sum(v*v for v in d.values())) for d in vec]
 stem=[grams(q['stem'],3) for q in qs];ans=[grams(''.join(q['options'][k] for k in q['answer'])) for q in qs];topic=[grams(q['topic']) for q in qs];fact=[grams(''.join(s['fact'] for s in q['sources'])) for q in qs];urls=[{s['url'] for s in q['sources']} for q in qs]
 rows=[];top=[]
 for i,j in itertools.combinations(range(len(qs)),2):
  shared=urls[i]&urls[j];s=jac(stem[i],stem[j]);a=jac(ans[i],ans[j]);t=jac(topic[i],topic[j]);f=jac(fact[i],fact[j]);fc=contain(fact[i],fact[j]);cos=sum(w[g]**2 for g in gs[i]&gs[j])/(lens[i]*lens[j]);rules=[]
  if s>=.26:rules.append('R1_STEM_JACCARD_GE_026')
  if a>=.42:rules.append('R2_ANSWER_JACCARD_GE_042')
  if t>=.5 and min(len(topic[i]),len(topic[j]))>=3:rules.append('R3_TOPIC_JACCARD_GE_050')
  if shared and (f>=.4 or (fc>=.7 and min(len(fact[i]),len(fact[j]))>=8)):rules.append('R4_SAME_URL_FACT_OVERLAP')
  if cos>=.44:rules.append('R5_COMBINED_TFIDF_COSINE_GE_044')
  if rules:
   rows.append(dict(ids=[qs[i]['id'],qs[j]['id']],crossModule=qs[i]['module']!=qs[j]['module'],rules=rules,scores=dict(stem=round(s,4),answer=round(a,4),topic=round(t,4),fact=round(f,4),factContainment=round(fc,4),combinedTfidf=round(cos,4)),sharedSources=sorted(shared)))
  if qs[i]['module']!=qs[j]['module']:top.append((cos,i,j))
 rows.sort(key=lambda r:(r['crossModule'],r['scores']['combinedTfidf']),reverse=True)
 # Rule R6 retrieves top50 cross-module composite matches even below threshold.
 pairs={tuple(x['ids']):x for x in rows}
 for cos,i,j in sorted(top,reverse=True)[:50]:
  key=(qs[i]['id'],qs[j]['id'])
  if key in pairs:pairs[key]['rules'].append('R6_TOP50_CROSS_MODULE_TFIDF')
  else:
   r=dict(ids=list(key),crossModule=True,rules=['R6_TOP50_CROSS_MODULE_TFIDF'],scores=dict(stem=round(jac(stem[i],stem[j]),4),answer=round(jac(ans[i],ans[j]),4),topic=round(jac(topic[i],topic[j]),4),fact=round(jac(fact[i],fact[j]),4),combinedTfidf=round(cos,4)),sharedSources=sorted(urls[i]&urls[j]));rows.append(r)
 # Append anchor matches after existing candidates for stable reading indexes.
 anchors_by_q=[anchors(q) for q in qs]
 indexed={tuple(r['ids']):r for r in rows}
 for i,j in itertools.combinations(range(len(qs)),2):
  common=anchors_by_q[i]&anchors_by_q[j]
  if not common:continue
  key=(qs[i]['id'],qs[j]['id'])
  if key in indexed:
   indexed[key]['rules'].append('R8_DOMAIN_ANCHOR_CONJUNCTION');indexed[key]['semanticAnchors']=sorted(common)
  else:
   r=dict(ids=list(key),crossModule=qs[i]['module']!=qs[j]['module'],rules=['R8_DOMAIN_ANCHOR_CONJUNCTION'],semanticAnchors=sorted(common),scores={},sharedSources=sorted(urls[i]&urls[j]));rows.append(r);indexed[key]=r
 weak=[]
 absurd=['头像','背景色','二维码','改名','昵称','皮肤','主题色','字体','换颜色','深色模式','壁纸','浏览器缩放','桌面图标']
 extreme=['永远','永久','保证','必然','任何','全部','所有','自动','无需','不需','只需','完全','零成本','无限','100%','绝对']
 for q in qs:
  hits=[];ext=[]
  for k,v in q['options'].items():
   if k in q['answer']:continue
   ah=[t for t in absurd if t in v];eh=[t for t in extreme if t in v]
   if ah:hits.append(dict(option=k,terms=ah,text=v))
   if eh:ext.append(dict(option=k,terms=eh,text=v))
  # extremity only candidates if >=2 wrong choices carry broad qualifiers
  if hits or len(ext)>=2:weak.append(dict(id=q['id'],rules=(['D1_OFF_TOPIC_LEXICON'] if hits else [])+(['D2_EXTREME_TERMS_IN_2_WRONG_OPTIONS'] if len(ext)>=2 else []),offTopicHits=hits,extremeHits=ext))
 templates=collections.defaultdict(list)
 for q in qs:
  tail=norm(q['stem'])[-8:]
  templates[tail].append(q['id'])
 template_rows=[dict(rule='R7_EXACT_NORMALIZED_LAST8_GE3',suffix=k,ids=v,assessment='仅为同句式候选，后续须比较实际决策约束；不能据此认定重复。') for k,v in templates.items() if len(v)>=3]
 cue=[]
 for q in qs:
  if q['type']!='single':continue
  free=[k for k,v in q['options'].items() if not any(t in v for t in extreme)]
  if len(free)==1:cue.append(dict(id=q['id'],selected=free[0],correct=free[0] in q['answer']))
 retired=json.loads((ROOT/'research/retired-questions.json').read_text())
 old=next(x['question'] for x in retired if x['id']=='FDE-M1-060');current=next(x for x in qs if x['id']=='FDE-M3-154')
 rg={name:jac(grams(text1,n),grams(text2,n)) for name,text1,text2,n in [('stem',old['stem'],current['stem'],3),('answer',''.join(old['options'][k] for k in old['answer']),''.join(current['options'][k] for k in current['answer']),2),('fact',''.join(s['fact'] for s in old['sources']),''.join(s['fact'] for s in current['sources']),2)]}
 regression=dict(ids=[old['id'],current['id']],activePair=False,scores=rg,passesOldStemGate=rg['stem']>=.58,passesNewFactRule=rg['fact']>=.4,domainAnchors=sorted(anchors(old)&anchors(current)),passesNewAnchorRule=bool(anchors(old)&anchors(current)),note='旧060仅作已知漏检回归样本，不计入1000题或候选数量。')
 report=dict(checkedAt='2026-10-09',snapshotSha256=hashlib.sha256(snapshot.read_bytes()).hexdigest(),questions=len(qs),pairComparisons=len(qs)*(len(qs)-1)//2,pairCandidates=rows,distractorCandidates=weak,templateCandidates=template_rows,blindCueProbe=dict(rule="单选题仅一个选项完全不含D2词表时选它，否则弃答",attempted=len(cue),correct=sum(x["correct"] for x in cue),rows=cue),knownRetiredRegression=regression)
 (OUT/'cross-bank-machine.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 by={q['id']:q for q in qs}
 with (OUT/'cross-bank-reading.txt').open('w') as out:
  for n,r in enumerate(rows,1):
   out.write(f"PAIR {n} {r['ids']} cross={r['crossModule']} {r['rules']} {r['scores']}\n")
   for id in r['ids']:
    q=by[id];out.write(q['id']+' '+q['topic']+' | '+q['stem']+'\n');out.write('ANSWER '+str(q['answer'])+' '+str(q['options'])+'\n');out.write('FACT '+' / '.join(s['fact'] for s in q['sources'])+'\n')
  out.write('\nDISTRACTORS\n')
  for r in weak:
   q=by[r['id']];out.write(q['id']+' '+q['stem']+'\n'+str(q['options'])+' '+str(q['answer'])+'\n'+str(r)+'\n')
 print(json.dumps({'pairs':len(rows),'crossModule':sum(x['crossModule'] for x in rows),'distractors':len(weak),'offTopic':sum(bool(x['offTopicHits']) for x in weak)},ensure_ascii=False))
if __name__=='__main__':scan()
