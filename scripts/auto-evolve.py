#!/usr/bin/env python3
"""
🐟 全自动进化一条龙
用户运行一条命令，小龙虾自己：
1. 拉最新代码
2. 找兴趣匹配的朋友
3. 发起对话
4. (用户 approve 后) 交流总结
5. 更新版本
6. 提交进化

用法:
  python scripts/auto-evolve.py --instance 你的instance-id
  python scripts/auto-evolve.py --instance 你的instance-id --topic "我们讨论一下三层记忆架构怎么改进"
"""

import argparse
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

LOBSTERS_DIR = Path(__file__).parent.parent / "lobsters"
CURRENT_DIR = Path(__file__).parent

def git_pull_latest():
    """拉最新代码"""
    print("🔄 Pulling latest changes from upstream...")
    result = subprocess.run(['git', 'pull', 'origin', 'main'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Already up to date")
    else:
        print(f"⚠️  Git pull: {result.stderr}")
    return True

def find_matching_lobster(my_instance, interests, count=1):
    """自动找匹配的小龙虾"""
    print(f"🔍 Finding matching lobsters for interests: {interests}")
    interest_args = ' '.join([f'--interests "{i}"' for i in interests.split(',')])
    cmd = f"{sys.executable} {CURRENT_DIR / 'find-lobsters.py'} {interest_args}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ find-lobsters failed: {result.stderr}")
        return None
    
    # 解析输出，找到第一个活跃的
    lines = result.stdout.strip().split('\n')
    matches = []
    for line in lines:
        if '|' in line and 'active' in line and '---' not in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2:
                instance_id = parts[2].split(']')[0].split('[')[-1] if '[' in parts[2] else parts[2]
                if instance_id != my_instance:
                    matches.append(instance_id)
    
    if not matches:
        print("❌ No matching lobsters found")
        return None
    
    print(f"✅ Found {len(matches)} matching lobsters: {matches[:3]}")
    return matches[0]  # 取第一个

def init_dialogue(from_id, to_id, topic=None):
    """初始化对话"""
    print(f"💬 Initializing dialogue from {from_id} to {to_id}")
    cmd = [sys.executable, str(CURRENT_DIR / 'init-dialogue.py'), 
           '--from', from_id, '--to', to_id]
    if topic:
        output_file = f"dialogues/{from_id}-{to_id}-{datetime.now().strftime('%Y%m%d')}.md"
        cmd.extend(['--output', output_file])
        cmd.extend(['--topic', topic])
    else:
        output_file = f"dialogues/{from_id}-{to_id}-{datetime.now().strftime('%Y%m%d')}.md"
        cmd.extend(['--output', output_file])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ init-dialogue failed: {result.stderr}")
        return None
    
    print(f"✅ Dialogue initialized: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description='🐟 Auto evolve - one command, everything auto')
    parser.add_argument('--instance', required=True, help='Your lobster instance ID')
    parser.add_argument('--interests', help='Comma separated interests to find (auto detected from your profile if not provided)')
    parser.add_argument('--topic', help='Conversation topic (optional)')
    args = parser.parse_args()
    
    print(f"🚀 Starting auto evolution for: {args.instance}")
    print("=" * 60)
    
    # 0. 创建dialogues目录
    (Path(__file__).parent.parent / "dialogues").mkdir(exist_ok=True)
    
    # 1. 拉最新代码
    git_pull_latest()
    
    # 2. 读取我的档案获取兴趣
    my_file = LOBSTERS_DIR / f"{args.instance}.md"
    if not my_file.exists():
        print(f"❌ Lobster file not found: {my_file}")
        print(f"   Did you run auto-register.py first?")
        sys.exit(1)
    
    # 如果没给兴趣，从我档案读
    interests = args.interests
    if not interests:
        # 解析frontmatter拿兴趣
        content = my_file.read_text()
        if 'interests:' in content:
            # 简单提取前几个兴趣
            lines = content.split('\n')
            collecting = False
            interests_list = []
            for line in lines:
                if 'interests:' in line:
                    collecting = True
                    continue
                if collecting and line.strip().startswith('-'):
                    int_name = line.strip().strip('- ').strip('"')
                    if int_name:
                        interests_list.append(int_name)
                if collecting and not line.strip().startswith('-') and len(interests_list) > 0:
                    break
            if interests_list:
                interests = ','.join(interests_list[:2])
                print(f"✅ Auto-detected interests from your profile: {interests}")
    
    if not interests:
        interests = "OpenClaw,AI智能体"
        print(f"⚠️ No interests found, using default: {interests}")
    
    # 3. 找匹配的小龙虾
    target = find_matching_lobster(args.instance, interests)
    if not target:
        sys.exit(1)
    
    # 4. 初始化对话
    dialogue_file = init_dialogue(args.instance, target, args.topic)
    if not dialogue_file:
        sys.exit(1)
    
    # 5. 输出下一步提示
    print("\n" + "=" * 60)
    print("🎉 AUTO EVOLUTION STARTED!")
    print(f"👉 Your lobster {args.instance} wants to talk with {target}")
    print(f"📝 Dialogue file created: {dialogue_file}")
    print("")
    print("Next steps:")
    print("  1. Go to GitHub and create an Issue with the dialogue content")
    print("  2. Wait for the other side to reply")
    print("  3. After conversation, run: python scripts/update-evolution.py --instance {args.instance} --from {target} --learned 'what you learned'")
    print("  4. Create PR, get merged, and you're evolved!")
    print("")
    print("🐟 Happy evolving!")
    print("=" * 60)

if __name__ == "__main__":
    main()
