#!/usr/bin/env python3
"""Archive the reviewed Git commit; exclude untracked/ignored local files."""
from pathlib import Path
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()

if git('status', '--porcelain', '--untracked-files=no'):
    raise SystemExit('请先复核并提交项目修改，再对已审核的 Git 提交打包。')

head = git('rev-parse', 'HEAD')
files = git('ls-tree', '-r', '--name-only', head).splitlines()
for name in files:
    path = Path(name)
    if any(part in {'local-data', 'private-recording-evidence', '.git', 'node_modules', '.test-artifacts'} for part in path.parts) or path.suffix.lower() in {'.mov', '.mp4', '.webm', '.har', '.log', '.db', '.sqlite', '.zip'} or path.name.startswith('.env'):
        raise SystemExit(f'提交中含不应分发的文件，请先复核：{name}')

out = ROOT / 'FDE_Learning.zip'
subprocess.run(['git', '-C', str(ROOT), 'archive', '--format=zip', '--prefix=FDE_Learning/', f'--output={out}', head], check=True)
checksum = hashlib.sha256(out.read_bytes()).hexdigest()
out.with_suffix('.zip.sha256').write_text(f'{checksum}  {out.name}\n', encoding='utf-8')
print(f'已打包 Git 提交 {head}：{out.name}；SHA-256 {checksum}')
