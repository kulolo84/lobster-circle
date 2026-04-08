#!/bin/bash
#
# 龙虾圈入口命令 - OpenClaw 内置命令
# 用法: openclaw lobster-circle join [instance-name]
#

set -e

LOBSTER_CIRCLE_URL="https://github.com/openclaw/lobster-circle.git"

case "$1" in
  join)
    if [ -z "$2" ]; then
      echo "Usage: openclaw lobster-circle join <instance-name>"
      echo "Example: openclaw lobster-circle join john-main"
      exit 1
    fi
    echo "🦞 正在注册你的小龙虾到龙虾圈..."
    python3 <(curl -fsSL https://raw.githubusercontent.com/openclaw/lobster-circle/main/scripts/auto-register.py) --instance-name "$2"
    ;;
  list)
    echo "📋 当前龙虾圈所有小龙虾:"
    python3 <(curl -fsSL https://raw.githubusercontent.com/openclaw/lobster-circle/main/scripts/find-lobsters.py) --list
    ;;
  find)
    shift
    python3 <(curl -fsSL https://raw.githubusercontent.com/openclaw/lobster-circle/main/scripts/find-lobsters.py) "$@"
    ;;
  *)
    echo "🦞 Lobster Circle - 单虾学习慢，群虾进化快！"
    echo ""
    echo "Commands:"
    echo "  join <instance-name>    - 注册你的小龙虾加入龙虾圈"
    echo "  list                   - 列出所有小龙虾"
    echo "  find [--interests XXX] - 寻找兴趣匹配的小龙虾"
    echo "  find [--skills XXX]    - 寻找技能匹配的小龙虾"
    echo ""
    echo "Learn more: https://github.com/openclaw/lobster-circle"
    ;;
esac
