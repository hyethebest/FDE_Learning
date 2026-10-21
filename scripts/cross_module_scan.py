#!/usr/bin/env python3
"""Low threshold candidates for independent AI review, never a semantic-validity assertion."""
import json,re,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
qs=json.loads((ROOT/'data/questions.json').read_text())
def grams(text,n):
 text=re.sub(r'[\W_]','',text)
 return {text[i:i+n] for i in range(max(0,len(text)-n+1))}
def jac(a,b):return len(a&b)/len(a|b) if a|b else 0
stems=[grams(q['stem'],3) for q in qs]
answers=[grams(''.join(q['options'][k] for k in q['answer']),2) for q in qs]
sources=[{s['url'] for s in q['sources']} for q in qs]
rows=[]
for i,j in itertools.combinations(range(len(qs)),2):
 if qs[i]['module']==qs[j]['module']:continue
 stem=jac(stems[i],stems[j]);answer=jac(answers[i],answers[j])
 if stem>=.26 or answer>=.5 or (answer>=.42 and sources[i]&sources[j]):
  rows.append({'ids':[qs[i]['id'],qs[j]['id']],'stems':[qs[i]['stem'],qs[j]['stem']],'stemSimilarity':round(stem,3),'answerSimilarity':round(answer,3),'sharedSources':sorted(sources[i]&sources[j])})
report={'published':len(qs),'purpose':'仅筛查候选；同答案不等于同题，同源不等于重复。由审校判断实质认知任务。','candidates':rows}
(ROOT/'research/cross-module-candidates.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
for row in rows:print(json.dumps(row,ensure_ascii=False))
print('candidates',len(rows))
