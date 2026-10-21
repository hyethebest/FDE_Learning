#!/usr/bin/env python3
"""Publish only independent approvals matching current question content hash."""
import json,sys
from pathlib import Path
from validate_bank import validate,content_hash
ROOT=Path(__file__).resolve().parents[1]
all_questions=[q for p in sorted((ROOT/'data/batches').glob('M*.json')) for q in json.loads(p.read_text())]
reviews={}
for p in sorted((ROOT/'research/reviews').glob('*.json'),key=lambda p:p.stat().st_mtime):
    items=json.loads(p.read_text());items=items if isinstance(items,list) else items.get('reviews',[])
    for item in items:reviews[(item['id'],item.get('contentHash'))]=item
approved=[];quarantined=[]
for q in all_questions:
    review=reviews.get((q['id'],content_hash(q)))
    if review and review['status']=='approved' and review['reviewer']!=q['review']['author']:
        q['review']={**q['review'],'status':'approved','reviewer':review['reviewer'],'notes':review['notes'],'checkedAt':review['checkedAt'],'contentHash':review['contentHash']}
        approved.append(q)
    else:quarantined.append({'id':q['id'],'reason':review['notes'] if review else ['缺少与当前内容匹配的独立审校'],'status':review['status'] if review else 'pending'})
report=validate(approved)
if report['errors']:
    print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit('结构检测失败，未发布')
(ROOT/'data/questions.json').write_text(json.dumps(approved,ensure_ascii=False,indent=2))
(ROOT/'research/quarantine.json').write_text(json.dumps(quarantined,ensure_ascii=False,indent=2))
manifest=json.loads((ROOT/'data/manifest.json').read_text());manifest.update(version=manifest.get('version','2026.10.09.1'),published=len(approved),drafts=len(quarantined),totalAuthored=len(all_questions),counts=report['counts'])
(ROOT/'data/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(ROOT/'research/published-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'published':len(approved),'quarantined':len(quarantined),'nearDuplicates':len(report['nearDuplicates'])},ensure_ascii=False))
