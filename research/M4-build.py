import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S={
'flow':('126433','使用流程','2026-07-03','第二至五步'),
'connect':('115872','连接器与工具介绍','2026-07-16','核心概念'),
'rag':('132211','Agentic RAG','2026-08-21','适用场景及工作流引导'),
'schema':('123555','知识库 Schema','2026-09-16','下架说明'),
'db':('119291','数据库','2026-08-21','新建数据库及数据表操作'),
'time':('138380','时效性检索','2026-09-18','功能生效逻辑及功能说明'),
'param':('112962','参数提取节点','2026-01-26','节点功能及收集参数'),
'card':('115756','选项卡节点','2026-01-13','节点功能及常见问题'),
'file':('123744','文件收集节点','2025-09-25','文件收集及输出变量'),
' text':('126594','文本收集节点','2025-12-19','文本收集节点与参数提取节点的区别'),
'llm':('112963','大模型节点','2026-08-18','模型及多模态输入'),
'intent':('115747','大模型意图识别节点','2026-02-10','节点功能及意图模式'),
'qa':('112964','大模型知识问答节点','2026-03-31','用户问题及提示词'),
'search':('112966','知识检索节点','2026-03-31','节点功能及检索规则'),
'code':('112967','代码节点','2026-06-01','节点功能及代码'),
'sub':('115749','工作流节点','2026-01-29','节点功能及工作流输入输出'),
'agent':('122554','Agent 节点','2026-02-12','节点功能及引用Agent'),
'aggregate':('117358','变量聚合节点','2025-08-17','节点功能及聚合'),
'condition':('112970','条件判断节点','2026-01-16','设置条件'),
'loop':('115750','循环节点','2026-04-28','循环方式及使用场景建议'),
'batch':('119290','批处理节点','2026-01-26','节点功能及批处理设置')}
S['text']=S.pop(' text')
S.update({
'newtool':('117855','新建工具','2026-08-20','基本信息、配置工具及校验工具'),
'mcp':('115873','新建连接器','2026-05-27','MCP服务端要求'),
'doc':('112702','文档概述','2026-09-16','导入文档与网页限制'),
'kb':('123551','什么是知识库','2025-09-22','知识库数据类型与层级'),
'faq':('112703','问答','2026-02-06','新建问答与从文档生成'),
'memory':('138162','记忆库','2026-09-15','隔离维度、类型与绑定规则'),
'graph':('128202','知识图谱 GraphRAG','2026-02-12','适用场景及图谱构建'),
'parse':('127312','知识处理模型设置','2026-01-13','知识处理模型说明'),
'meta':('138240','元数据设置','2026-09-18','使用场景及元数据与标签检索区别'),
'skill':('134602','Skills 文件规范','2026-07-20','description与目录结构'),
'publish':('104209','应用发布概述','2026-10-09访问版本','触发器及服务状态')})
S.update({
'skilltypes':('129561','Skills介绍','2026-07-14','Skills的三种类别'),
'skilluse':('129563','使用Skills','2026-09-10','三种使用场景'),
'free':('122598','自由转交','2026-06-15','转交描述及转交关系配置'),
'collab':('122556','工作流编排','2026-01-22','功能定位及设置方式'),
'pe':('122553','Plan-and-Execute协同','2025-09-22','功能定位与对话测试'),
'split':('122551','文档切分设置','2026-08-04','切分规则及对比'),
'intervene':('119287','解析切分干预','2025-12-30','调整切分结果'),
'struct':('119288','智能结构化解析','2025-12-29','结构化特征及检索方式'),
'compare':('116451','文档对比任务','2025-12-29','功能说明及问答操作')})
S.update({
'sse':('129202','对话端接口文档（HTTP SSE）','2026-09-18','参数说明及文本事件'),
'ws':('129365','对话端接口文档（WebSocket）','2026-09-18','通道特征与连接Token'),
'oldsse':('105561','对话端接口文档（HTTP SSE，旧版）','2026-06-04','下线警告'),
'http':('112968','工具节点','2026-01-06','调用方式、输出变量与异步调用'),
'async':('126856','工作流的异步调用','2026-02-10','适用场景与等待输入'),
'package':('130990','应用包导出与导入','2026-06-30','导出范围与目标环境配置'),
'retrieve':('123554','知识库设置概览','2026-02-06','检索召回设置及文档到期时间'),
'eval':('104208','应用评测','2026-01-20','基准评测与对比评测')})
S.update({
'modelrole':('112876','模型介绍','2026-05-06','标准模式与Multi-Agent模式'),
'prompt':('120901','提示词模板','2026-02-11','变量及复用'),
'claw':('131653','基于Claw模式创建数据分析助手','2026-06-30','模式定位及提示词')})
rows=[]
for p in sorted((ROOT/'research').glob('M4-items-*.txt')):
    for line in p.read_text().splitlines():
        if not line.strip() or line.startswith('#'): continue
        parts=line.split('|')
        assert len(parts)==8,(p,line, len(parts))
        src,topic,stem,opts,ans,expl,wrongs,fact=parts
        choices=opts.split(';'); reasons=wrongs.split(';')
        assert len(choices)==len(reasons)==4,(stem,choices,reasons)
        letters='ABCD'; answers=list(ans)
        assert len(answers) in [1,2,3]
        assert all(reasons[i] for i,k in enumerate(letters) if k not in answers),stem
        shift=len(rows)%4
        old=dict(zip(letters,choices)); old_reasons=dict(zip(letters,reasons))
        order=letters[shift:]+letters[:shift]
        remap={k:letters[i] for i,k in enumerate(order)}
        choices=[old[k] for k in order]
        reasons=[old_reasons[k] for k in order]
        answers=sorted(remap[k] for k in answers)
        code,title,version,section=S[src.split("+")[0]]
        rows.append(dict(id=f'FDE-M4-{len(rows)+1:03}',module='M4',topic=topic,type='single' if len(ans)==1 else 'multiple',stem=stem,options=dict(zip(letters,choices)),answer=answers,explanation=expl,distractors={k:reasons[i] for i,k in enumerate(letters) if k not in answers},difficulty='进阶' if len(ans)==1 else '综合',sources=[dict(url='https://cloud.tencent.com/document/product/1759/'+code,title=title,section=section,fact=fact,verifiedAt='2026-10-09',version=version)],review=dict(status='draft',author='solution_design',reviewer=None,notes=['原创场景推理；待独立审校'])))
# Compound questions cite each participating component fact separately.
item_lines=[line for p in sorted((ROOT/'research').glob('M4-items-*.txt')) for line in p.read_text().splitlines() if line.strip() and not line.startswith('#')]
for q,line in zip(rows,item_lines):
    for key in line.split('|')[0].split('+')[1:]:
        code,title,version,section=S[key]
        q['sources'].append(dict(url='https://cloud.tencent.com/document/product/1759/'+code,title=title,section=section,fact=line.split('|')[-1],verifiedAt='2026-10-09',version=version))
rows[9]['sources'].append(dict(url='https://cloud.tencent.com/document/product/658/137832',title='腾讯云 ADP 前沿部署工程师 (FDE) 认证考试指南',section='知识点占比与考核重点',fact='2026-09-10考纲仍列知识库Schema。',verifiedAt='2026-10-09',version='2026-09-10'))
rows[11]['sources'][0]['section']='注意：生成费用'
# Audit fix: each citation states a fact directly supported by its own page.
rows[177]['sources'][1]['fact']='条件判断支持 if-else 分支，表达式可引用祖先节点输出变量或固定值，并按判断结果路由后续分支。'
tail_path=ROOT/'research/M4-tail-safety.json'
if tail_path.exists():
    tail=json.loads(tail_path.read_text())
    assert len(rows)==200, 'Main author quota must remain 200 before tail merge'
    assert isinstance(tail,list) and len(tail)==50, 'Tail must be complete before merge'
    assert [q['id'] for q in tail]==[f'FDE-M4-{i:03}' for i in range(201,251)]
    assert sum(q['type']=='single' for q in tail)==33
    assert sum(q['type']=='multiple' for q in tail)==17
    rows.extend(tail)
assert len({x['id'] for x in rows})==len(rows)
assert len({x['stem'] for x in rows})==len(rows)
(ROOT/'data/batches/M4.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('M4',len(rows),'single',sum(x['type']=='single' for x in rows),'multiple',sum(x['type']=='multiple' for x in rows))
