#!/usr/bin/env python3
"""Structural and near-duplicate gates; content approval requires independent review."""
import json,re,hashlib,itertools,collections,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def content_hash(q):
    return hashlib.sha256(json.dumps({k:v for k,v in q.items() if k!='review'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate(questions):
    errors=[];ids=set();stems={};counts=collections.Counter();positions=collections.Counter()
    for q in questions:
        ident=q.get('id','?'); prefix=ident+': '
        required=['id','module','topic','type','stem','options','answer','explanation','distractors','difficulty','sources','review']
        if any(k not in q for k in required):errors.append(prefix+'缺字段');continue
        if ident in ids:errors.append(prefix+'重复ID')
        ids.add(ident)
        if not re.fullmatch(r'FDE-M[1-7]-\d{3}',ident):errors.append(prefix+'ID格式')
        if q['module'] not in [f'M{i}' for i in range(1,8)]:errors.append(prefix+'模块无效')
        if set(q['options']) not in ({'A','B','C','D'},{'A','B','C','D','E'}):errors.append(prefix+'必须四或五选项')
        if len(set(q['options'].values()))!=len(q['options']):errors.append(prefix+'选项重复')
        ans=q['answer']
        if not isinstance(ans,list) or not set(ans).issubset(q['options']) or len(set(ans))!=len(ans):errors.append(prefix+'答案无效')
        if q['type']=='single' and len(ans)!=1:errors.append(prefix+'单选答案数')
        elif q['type']=='multiple' and not 2<=len(ans)<len(q['options']):errors.append(prefix+'多选答案数')
        elif q['type'] not in ('single','multiple'):errors.append(prefix+'题型无效')
        if not (set(q['options'])-set(ans)).issubset(q['distractors']):errors.append(prefix+'缺干扰项解析')
        if not q['sources']:errors.append(prefix+'无来源')
        for s in q['sources']:
            if not all(s.get(k) for k in ['url','title','section','fact','verifiedAt','version']):errors.append(prefix+'来源字段缺失')
            if s.get('url')!='https://cloud.tencent.com/product/adp' and not re.match(r'https://(cloud\.tencent\.com/(document|edu|act)/|adp\.tencent\.com/(solutions|zh/blog)/)',s.get('url','')):errors.append(prefix+'非核准官方正文URL')
        norm=re.sub(r'[\W_]+','',q['stem'])
        if norm in stems:errors.append(prefix+'重复题干 '+stems[norm])
        stems[norm]=ident;counts[(q['module'],q['type'])]+=1;positions[tuple(ans)]+=1
    # Character trigram Jaccard; catches renamed nouns only when linguistic overlap is high.
    sets=[set(q['stem'][i:i+3] for i in range(max(0,len(q['stem'])-2))) for q in questions]
    near=[]
    for i,j in itertools.combinations(range(len(questions)),2):
        a,b=sets[i],sets[j];union=len(a|b)
        score=len(a&b)/union if union else 1
        if score>=.58:near.append({'ids':[questions[i]['id'],questions[j]['id']],'similarity':round(score,3)})
    return {'total':len(questions),'errors':errors,'nearDuplicates':near,'counts':{f'{m}/{t}':n for (m,t),n in sorted(counts.items())},'answerDistribution':{'/'.join(k):v for k,v in positions.items()}}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--published',action='store_true');args=parser.parse_args()
    questions=json.loads((ROOT/'data/questions.json').read_text()) if args.published else [q for p in sorted((ROOT/'data/batches').glob('M*.json')) for q in json.loads(p.read_text())]
    report=validate(questions);(ROOT/'research/validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(report['errors']))
