import json
from pathlib import Path
p=Path('data/batches/M3.json');q=json.loads(p.read_text());by={int(x['id'].split('-')[-1]):x for x in q}
x=by[133];x.update(topic='Skill共享申请进度入口',stem='自定义Skill已提交企业共享审批，申请人要查看进度或取消申请。哪些入口判断符合当前文档？',options={'A':'在Skill详情的企业共享设置悬浮提示中查看进度','B':'申请人可在右上角审批中心列表查看自己全部提交记录','C':'取消审批也从Skill详情的悬浮提示进入','D':'右上角审批中心面向审批人，不能当作申请人的提交记录列表'},answer=['A','C','D'],explanation='新建Skills文档将申请人的进度与取消入口放在Skill详情右上角企业共享设置的悬浮提示中；审批中心是审批人视角，申请人暂不能在那里查询自己的提交记录。入口分工与安全报告是否复用是不同配置问题。',distractors={'B':'文档明确申请人暂无法在审批中心列表查看自己提交的记录，应使用Skill详情入口。'})
x['sources']=[dict(url='https://cloud.tencent.com/document/product/1759/129562',title='新建Skills',section='提交企业共享Skills／提交后状态',fact='申请人进度与取消入口位于Skill详情企业共享设置悬浮提示；审批中心为审批人视角。',verifiedAt='2026-10-09',version='2026-07-20')]
x=by[164];x.update(topic='问答与工作流意图冲突',stem='标准模式应用同时配置问答和工作流，二者意图高度相似导致调用选择不稳定。应用高级设置中哪项直接针对这种冲突？',options={'A':'意图达成优先级','B':'最大输出长度','C':'语音播报音色','D':'知识库图片问答开关'},answer=['A'],explanation='应用设置说明，当问答与工作流高度相似并影响调用判断时，可设置合理的意图达成优先级。输出长度、音色及图片问答开关分别控制其他行为，不解决两种意图路径的优先关系。',distractors={'B':'限制生成长度不决定问答和工作流的意图优先级。','C':'音色控制语音呈现，与调用路径选择无关。','D':'图片问题检索开关控制是否结合知识，不处理相似问答与工作流的优先级。'})
x['sources']=[dict(url='https://cloud.tencent.com/document/product/1759/104206',title='应用设置概述',section='高级设置／意图达成优先级',fact='问答与工作流高度相似影响调用判断时，可设置合理的意图达成优先级。',verifiedAt='2026-10-09',version='2026-07-21')]
# Keep distractors in the same routing-configuration domain.
x['options']['C']='模型上下文改写';x['distractors']['C']='上下文改写补全依赖历史的当前问题，不直接配置问答与工作流的优先关系。'
x['options']['D']='行业同义词设置';x['distractors']['D']='同义词将别称替换为统一知识名称，不直接设定两种调用路径的优先级。'
x['explanation']='应用设置说明，当问答与工作流高度相似并影响调用判断时，可设置合理的意图达成优先级。输出长度控制回复规模、上下文改写补全问题语义、同义词统一业务称呼，均不直接配置这两条调用路径的优先关系。'
for n in [133,164]:by[n]['review']['notes'].append('末轮跨模块去重，改为已联网核实的新配置目标，待独立hash审校。')
p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
