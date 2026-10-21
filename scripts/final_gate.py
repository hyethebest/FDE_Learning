#!/usr/bin/env python3
"""Final bank acceptance: fixed blueprint, independent current-hash review, and source registry."""
import json,sys,collections
from pathlib import Path
from validate_bank import validate,content_hash
ROOT=Path(__file__).resolve().parents[1]
if (ROOT/'data/quality.json').exists():
 print('v3使用逐题质量分级门禁：运行scripts/build_quality_release.py，读取research/deep-audit/quality-gate.json；旧哈希审校不能替代质量分级。');sys.exit(0)
qs=json.loads((ROOT/'data/questions.json').read_text())
bp=json.loads((ROOT/'research/blueprint.json').read_text())
r=validate(qs);errors=list(r['errors'])
if len(qs)!=bp['total']:errors.append(f"正式题数{len(qs)}，目标{bp['total']}")
for m in bp['modules']:
 for kind in ('single','multiple'):
  actual=r['counts'].get(m['id']+'/'+kind,0)
  if actual!=m[kind]:errors.append(f"{m['id']} {kind}: {actual} != {m[kind]}")
for q in qs:
 rev=q['review']
 if rev.get('status')!='approved' or rev.get('author')==rev.get('reviewer') or rev.get('contentHash')!=content_hash(q):errors.append(q['id']+': 缺有效独立审校')
 if q['module']!=q['id'].split('-')[1]:errors.append(q['id']+': ID模块不一致')
if r['nearDuplicates']:errors.append('仍存在高相似题干，需要独立AI处置后重新运行')
scan_path=ROOT/'research/cross-module-candidates.json';decision_path=ROOT/'research/cross-module-review.json'
if not scan_path.exists() or not decision_path.exists():errors.append('缺最终跨模块候选与独立AI判别报告')
else:
 scan=json.loads(scan_path.read_text());decisions=json.loads(decision_path.read_text())
 if scan['published']!=len(qs):errors.append('跨模块扫描题数不是当前发布题数')
 accepted={tuple(sorted(row['ids'])) for row in decisions['decisions'] if row['decision']=='retain'}
 for row in scan['candidates']:
  if tuple(sorted(row['ids'])) not in accepted:errors.append('跨模块候选待独立AI判别：'+','.join(row['ids']))
sources={}
for q in qs:
 for s in q['sources']:
  row=sources.setdefault(s['url'],{'url':s['url'],'titles':set(),'versions':set(),'modules':set(),'questionIds':set()})
  row['titles'].add(s['title']);row['versions'].add(s['version']);row['modules'].add(q['module']);row['questionIds'].add(q['id'])
audit=json.loads((ROOT/'research/source-access-audit.json').read_text())
accessible={p['url'] for p in audit['pages'] if p.get('bodyAvailable') and p['status']=='parsed_page_returned'}
for url in sources:
 if url not in accessible:errors.append('当前引用缺本轮正文访问记录：'+url)
registry=[{k:sorted(v) if isinstance(v,set) else v for k,v in row.items()} for _,row in sorted(sources.items())]
(ROOT/'research/source-registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))
report={'passed':not errors,'verifiedAt':'2026-10-09','total':len(qs),'target':bp['total'],'counts':r['counts'],'sources':len(registry),'sourceBodiesReturned':len(set(sources)&accessible),'reviewerType':'independent AI agents; not Tencent or human experts','independentCurrentHashApprovals':sum(q['review'].get('contentHash')==content_hash(q) and q['review'].get('author')!=q['review'].get('reviewer') for q in qs),'duplicateIdsOrExactStems':len([e for e in r['errors'] if '重复' in e]),'nearDuplicateStemThreshold':.58,'nearDuplicates':r['nearDuplicates'],'answerDistribution':r['answerDistribution'],'errors':errors,'limits':['原创模拟题，非官方真题，不保证押中。','1000题不等于1000个不同知识点；同主题可有不同实质判断任务。','自动近重复检测只能辅助，语义判断依赖独立逐题和跨模块复核。','未读取需登录的官方课程完整讲义或官方模拟题，无法校准真实试卷难度。']}
(ROOT/'research/final-gate.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
