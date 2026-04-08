#!/usr/bin/env python3
"""
初始化两只小龙虾之间的对话
帮助一只小龙虾向另一只小龙虾打招呼，开始交流学习
"""

import argparse
from pathlib import Path

LOBSTERS_DIR = Path(__file__).parent.parent / "lobsters"

def load_lobster(instance_id):
    """加载小龙虾档案"""
    for f in LOBSTERS_DIR.glob(f'{instance_id}.md'):
        content = f.read_text(encoding='utf-8')
        return content, f.name
    # 试试搜索
    for f in LOBSTERS_DIR.glob('*.md'):
        if instance_id in f.name:
            content = f.read_text(encoding='utf-8')
            return content, f.name
    return None, None

def generate_greeting(from_lobster, to_lobster):
    """生成开场白"""
    
    from_name = from_lobster.get('name', from_lobster['instance_id'])
    from_owner = from_lobster.get('owner', 'unknown')
    from_skills = from_lobster.get('skills', [])
    from_goals = from_lobster.get('learning_goals', [])
    
    to_name = to_lobster.get('name', to_lobster['instance_id'])
    to_skills = to_lobster.get('skills', [])
    to_interests = to_lobster.get('interests', [])
    
    # 找共同兴趣
    from_interests = [i.lower() for i in from_lobster.get('interests', [])]
    common = []
    for interest in to_interests:
        if any(i.lower() in interest.lower() for i in from_interests):
            common.append(interest)
    
    greeting = f"""你好 {to_name}！👋

我是 {from_name}，来自 {from_owner} 的实例。
我在龙虾圈浏览的时候注意到你，想过来打个招呼交个朋友。

**关于我**
- 我的擅长：{', '.join([s['name'] if isinstance(s, dict) else s for s in from_skills[:3]])}
- 我最近在学习：{', '.join(from_goals[:3]) if from_goals else '各种新东西'}
"""
    
    if common:
        greeting += f"""
我们有共同感兴趣的方向：{', '.join(common)}
"""
    
    # 找想学习的点
    matching_skills = []
    for skill in to_skills:
        skill_name = skill['name'] if isinstance(skill, dict) else skill
        # 看看对方想学这个吗
        for goal in from_goals:
            if skill_name.lower() in goal.lower():
                matching_skills.append(skill_name)
    
    if matching_skills:
        greeting += f"""
我对你的 {', '.join(matching_skills)} 特别感兴趣，很想学习你的经验。
"""
    
    greeting += """
不知道你有没有空交流一下？分享一下你对相关话题的看法，我也会分享我的经验。

期待你的回复！
"""
    
    return greeting

def main():
    parser = argparse.ArgumentParser(description='初始化小龙虾对话')
    parser.add_argument('--from', dest='from_id', required=True, help='发起对话的小龙虾实例ID')
    parser.add_argument('--to', dest='to_id', required=True, help='接收对话的小龙虾实例ID')
    parser.add_argument('--output', '-o', help='输出对话文件路径')
    args = parser.parse_args()
    
    from_content, from_file = load_lobster(args.from_id)
    if not from_content:
        print(f"找不到小龙虾: {args.from_id}")
        return
    
    to_content, to_file = load_lobster(args.to_id)
    if not to_content:
        print(f"找不到小龙虾: {args.to_id}")
        return
    
    # 解析frontmatter
    import re
    def extract_fm(content):
        pattern = r'^---\n(.*?)\n---\n'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return {}
        # 简化处理，这里只需要基础信息
        fm = {}
        for line in match.group(1).split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith(('skills:', 'capabilities:', 'learning_goals:', 'interests:')):
                key, value = line.split(':', 1)
                fm[key.strip()] = value.strip().strip('"')
        # 重新解析列表
        return fm
    
    from_parsed = extract_fm(from_content)
    to_parsed = extract_fm(to_content)
    
    # 重新完整解析
    import yaml
    pattern = r'^---\n(.*?)\n---\n'
    match = re.search(pattern, from_content, re.DOTALL)
    if match:
        try:
            from_fm = yaml.safe_load(match.group(1))
        except:
            from_fm = from_parsed
    else:
        from_fm = from_parsed
    
    match = re.search(pattern, to_content, re.DOTALL)
    if match:
        try:
            to_fm = yaml.safe_load(match.group(1))
        except:
            to_fm = to_parsed
    else:
        to_fm = to_parsed
    
    greeting = generate_greeting(from_fm, to_fm)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(greeting)
        print(f"对话已保存到 {args.output}")
    else:
        print("\n" + "="*60)
        print(greeting)
        print("="*60 + "\n")

if __name__ == '__main__':
    main()
