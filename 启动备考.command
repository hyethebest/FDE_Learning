#!/bin/zsh
cd -- "${0:A:h}"
FDE_PYTHON=$(command -v python3)
if [[ -z "$FDE_PYTHON" ]]; then
  echo '未检测到 Python 3。请安装 Python 3 后重新打开此文件。'
  read
  exit 1
fi
FDE_HEALTH=$(curl -fsS http://127.0.0.1:8765/api/health 2>/dev/null)
if [[ -n "$FDE_HEALTH" ]]; then
  if print -r -- "$FDE_HEALTH" | "$FDE_PYTHON" -c 'import json,sys; d=json.load(sys.stdin);sys.exit(0 if d.get("app")=="fde-study" and d.get("root")==sys.argv[1] else 1)' "$PWD"; then
    open http://127.0.0.1:8765
    exit 0
  fi
  echo '8765 端口已有另一目录或旧版服务。请先保存当前答题并关闭旧服务，再打开此启动文件。不会自动结束任何进程。'
  read
  exit 1
fi
(sleep 1; open http://127.0.0.1:8765) &
"$FDE_PYTHON" server.py
