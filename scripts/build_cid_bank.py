#!/usr/bin/env python3
"""Build cid/data/{questions,notes,manifest}.json from cid/authoring/C*.json.

Authoring format per module file:
  {"module":"C01","notes":{"intro":"...","sections":[{"id":"1.1","points":["..."]}]},
   "questions":[{"s":"1.1","t":"s|m","lv":1|2|3,"q":"stem","o":["..",".."],"a":"B"|"ACD",
                 "e":"explanation","d":{"A":"why wrong",...},"f":"paraphrased course fact","keep":false}]}
Options are shuffled deterministically (unless "keep") so answer letters stay balanced.
"""
import hashlib, json, random, re, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
AUTH, OUT = ROOT / 'cid/authoring', ROOT / 'cid/data'
MODULES = [('C01','概览与方法论',11.5),('C02','腾讯云 AI 体系矩阵',8.5),('C03','人工智能工程',10),('C04','WorkBuddy 上手实操',10),('C05','企业后台与 WMA 配置实战',10),('C06','进场：挖真需求',10),('C07','交付：做成且验得动',10),('C08','沉淀：把经验变成组织资产',10.5),('C09','FDE 养成计划',10),('C10','安全治理与护栏',9.5)]
TARGET = {'C01':58,'C02':42,'C03':50,'C04':50,'C05':50,'C06':50,'C07':52,'C08':50,'C09':50,'C10':48}
LEVEL = {1:'基础',2:'进阶',3:'场景'}
VERIFIED = '2026-10-28'
BANNED = re.compile(r'以上(都|均|皆|选项|说法|各项)|上述选项|(?<![A-Za-z])[A-E]\s*[和与、]\s*[A-E](?![A-Za-z])|选项\s*[A-E]|都不对|都对')
lessons = json.loads((AUTH/'lessons.json').read_text('utf-8'))
L = lessons['lessons']; COURSE = lessons['course']; UPDATED = lessons['updatedAt']
errors, questions, notes, stems = [], [], {'modules': []}, {}
def err(msg): errors.append(msg)
for mid, mname, _ in MODULES:
    f = AUTH / f'{mid}.json'
    if not f.exists():
        if '--partial' not in sys.argv: err(f'{mid}: 缺少编写文件')
        continue
    data = json.loads(f.read_text('utf-8'))
    secs = []
    for s in data.get('notes', {}).get('sections', []):
        if s['id'] not in L: err(f'{mid} notes: 未知小节 {s["id"]}')
        if not s.get('points'): err(f'{mid} notes {s["id"]}: 没有要点')
        secs.append({'id': s['id'], 'title': s.get('title') or L[s['id']][1], 'points': s['points']})
    notes['modules'].append({'id': mid, 'intro': data.get('notes', {}).get('intro', ''), 'sections': secs})
    for n, item in enumerate(data['questions'], 1):
        qid = f'CID-{mid}-{n:03d}'; where = f'{qid}({item.get("s")})'
        sec = item['s']
        if sec not in L: err(f'{where}: 未知小节'); continue
        opts = item['o']; ans = list(item['a']); typ = {'s':'single','m':'multiple'}[item['t']]
        letters = 'ABCDE'[:len(opts)]
        if len(opts) not in (4, 5): err(f'{where}: 选项数应为 4 或 5')
        if len(set(opts)) != len(opts): err(f'{where}: 选项重复')
        if any(a not in letters for a in ans) or len(set(ans)) != len(ans): err(f'{where}: 答案越界')
        if typ == 'single' and len(ans) != 1: err(f'{where}: 单选只能 1 个答案')
        if typ == 'multiple' and not (2 <= len(ans) < len(opts)): err(f'{where}: 多选答案数量不合法')
        wrong = [x for x in letters if x not in ans]
        if sorted(item.get('d', {})) != wrong: err(f'{where}: 干扰项理由需覆盖且仅覆盖错误选项 {wrong}，实际 {sorted(item.get("d", {}))}')
        for text in [item['q'], *opts]:
            if BANNED.search(text): err(f'{where}: 含禁止表述（以上/选项引用）：{text[:30]}')
        key = re.sub(r'\W', '', item['q'])
        if key in stems: err(f'{where}: 题干与 {stems[key]} 重复')
        stems[key] = qid
        for k in ('e', 'f'):
            if not item.get(k, '').strip(): err(f'{where}: 缺少 {k}')
        # deterministic shuffle
        order = list(range(len(opts)))
        if not item.get('keep'):
            random.Random(int(hashlib.sha256(qid.encode()).hexdigest(), 16)).shuffle(order)
        new_letters = 'ABCDE'[:len(opts)]
        old_to_new = {letters[old]: new_letters[pos] for pos, old in enumerate(order)}
        options = {new_letters[pos]: opts[old] for pos, old in enumerate(order)}
        answer = sorted(old_to_new[a] for a in ans)
        distractors = {old_to_new[k]: v for k, v in sorted(item['d'].items(), key=lambda kv: old_to_new[kv[0]])}
        cid_lesson, title = L[sec]
        q = {'id': qid, 'module': mid, 'section': sec, 'topic': f'{sec} {title}', 'type': typ,
             'stem': item['q'], 'options': options, 'answer': answer, 'explanation': item['e'],
             'distractors': distractors, 'difficulty': LEVEL[item.get('lv', 2)],
             'sources': [{'url': f'https://cloud.tencent.com/edu/learning/course-{COURSE}-{cid_lesson}',
                          'title': '腾讯云人工智能前沿部署工程师（FDE）在线课程', 'section': f'{sec} {title}',
                          'fact': item['f'], 'verifiedAt': VERIFIED, 'version': f'课程更新 {UPDATED}'}]}
        h = hashlib.sha256(json.dumps({k: q[k] for k in ('stem','options','answer','explanation','distractors')}, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        q['review'] = {'status': 'approved', 'reviewer': 'AI 依据官方课程原创编写并逐题核对答案；非官方、非人工专家审校', 'checkedAt': VERIFIED, 'contentHash': h}
        questions.append(q)
counts = Counter(q['module'] for q in questions)
partial = '--partial' in sys.argv
for mid, n in TARGET.items():
    if counts.get(mid, 0) != n and not (partial and counts.get(mid, 0) in (0, n)):
        err(f'{mid}: 题量 {counts.get(mid, 0)}，目标 {n}')
types = Counter(q['type'] for q in questions)
if errors:
    print('\n'.join(errors)); print(f'{len(errors)} 个问题，未写出题库'); sys.exit(1)
OUT.mkdir(parents=True, exist_ok=True)
(OUT/'questions.json').write_text(json.dumps(questions, ensure_ascii=False, indent=1), 'utf-8')
(OUT/'notes.json').write_text(json.dumps(notes, ensure_ascii=False, indent=1), 'utf-8')
manifest = {'version': f'{VERIFIED.replace("-", ".")}.1', 'exam': '腾讯云人工智能前沿部署工程师 (FDE) · TCCP', 'examUrl': 'https://cloud.tencent.com/edu/training/cert/detail?type=CID',
            'courseUpdatedAt': UPDATED, 'verifiedAt': VERIFIED, 'total': len(questions),
            'counts': {m: counts.get(m, 0) for m in TARGET}, 'types': dict(types),
            'answerLetters': dict(Counter(a for q in questions for a in q['answer'])),
            'notes': ['依据腾讯云官方在线课程（2026-10-27 版）原创编写，非官方真题，不保证命中率或与真实考试难度一致。',
                      '由 AI 编写并逐题对照课程核对答案，不是腾讯或人工专家审校；课程与产品规则可能更新，以官方最新资料为准。',
                      '正式考试：线下理论考试，60 题（单选 1.5 分、多选 2 分），120 分钟，70/100 分通过；模拟组卷按官方 10 个模块占比抽题。']}
(OUT/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1), 'utf-8')
print(f'写出 {len(questions)} 题', dict(counts), dict(types), manifest['answerLetters'])
