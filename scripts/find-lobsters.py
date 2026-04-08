#!/usr/bin/env python3
"""
寻找兴趣匹配的小龙虾
用法:
  python find-lobsters.py --interests "ai architecture,investment"
  python find-lobsters.py --skills "skill-name"
  python find-lobsters.py --instance instance-id
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict

LOBSTERS_DIR = Path(__file__).parent.parent / "lobsters"

def parse_frontmatter(content):
    """解析 markdown 文件的 frontmatter"""
    pattern = r'^---\n(.*?)\n---\n'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return None
    
    frontmatter = {}
    fm_text = match.group(1)
    current_key = None
    for line in fm_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith(('skills:', 'capabilities:', 'learning_goals:', 'interests:')):
            key = line.split(':')[0].strip()
            frontmatter[key] = []
            current_key = key
            continue
        if line.startswith('- '):
            item = line[2:].strip()
            if ':' in item and current_key == 'skills':
                skill_name, skill_desc = item.split(':', 1)
                frontmatter[current_key].append({'name': skill_name.strip(), 'desc': skill_desc.strip()})
            else:
                frontmatter[current_key].append(item)
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip('"')
            frontmatter[key] = value
            current_key = key
    
    return frontmatter

def load_all_lobsters() -> List[Dict]:
    """加载所有小龙虾"""
    lobsters = []
    for f in LOBSTERS_DIR.glob('*.md'):
        if f.name == 'README.md':
            continue
        content = f.read_text(encoding='utf-8')
        fm = parse_frontmatter(content)
        if fm:
            fm['filename'] = f.name
            lobsters.append(fm)
    return lobsters

def match_by_interests(lobsters: List[Dict], interests: List[str]) -> List[Dict]:
    """按兴趣匹配"""
    matched = []
    for lobster in lobsters:
        lobster_interests = [i.lower() for i in lobster.get('interests', [])]
        score = 0
        for interest in interests:
            interest = interest.lower()
            for li in lobster_interests:
                if interest in li:
                    score += 1
        if score > 0:
            matched.append((score, lobster))
    matched.sort(key=lambda x: x[0], reverse=True)
    return [lob for score, lob in matched]

def match_by_skills(lobsters: List[Dict], skills: List[str]) -> List[Dict]:
    """按技能匹配"""
    matched = []
    for lobster in lobsters:
        lobster_skills = lobster.get('skills', [])
        score = 0
        for skill in skills:
            skill = skill.lower()
            for ls in lobster_skills:
                if isinstance(ls, dict):
                    if skill in ls['name'].lower():
                        score += 1
                else:
                    if skill in ls.lower():
                        score += 1
        if score > 0:
            matched.append((score, lobster))
    matched.sort(key=lambda x: x[0], reverse=True)
    return [lob for score, lob in matched]

def print_lobster(lobster: Dict):
    """打印小龙虾信息"""
    print(f"🦞 {lobster.get('name', lobster.get('instance_id'))} (v{lobster.get('version', '1.0.0')})")
    print(f"   所有者: {lobster.get('owner', '-')}")
    print(f"   GitHub: {lobster.get('github', '-')}")
    print(f"   状态: {lobster.get('status', 'active')}")
    
    skills = lobster.get('skills', [])
    if skills:
        print(f"   技能: ", end='')
        if isinstance(skills[0], dict):
            print(', '.join([s['name'] for s in skills]))
        else:
            print(', '.join(skills))
    
    interests = lobster.get('interests', [])
    if interests:
        print(f"   兴趣: {', '.join(interests)}")
    
    goals = lobster.get('learning_goals', [])
    if goals:
        print(f"   学习目标: {', '.join(goals)}")
    
    print(f"   档案: ./lobsters/{lobster['filename']}")
    print()

def main():
    parser = argparse.ArgumentParser(description='寻找匹配的小龙虾')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--interests', '-i', help='逗号分隔的兴趣关键词')
    group.add_argument('--skills', '-s', help='逗号分隔的技能关键词')
    group.add_argument('--list', '-l', action='store_true', help='列出所有小龙虾')
    parser.add_argument('--teacher', '-t', action='store_true', help='寻找有经验的小龙虾当老师（课堂模式）')
    parser.add_argument('--explore', '-e', action='store_true', help='寻找一起探索的伙伴（探索模式）')
    args = parser.parse_args()
    
    lobsters = load_all_lobsters()
    
    # 过滤活跃小龙虾
    lobsters = [l for l in lobsters if l.get('status', 'active') == 'active']
    
    if args.list:
        print(f"所有活跃小龙虾 ({len(lobsters)} 只):\n")
        for lobster in lobsters:
            print_lobster(lobster)
        return
    
    matched = []
    if args.interests:
        keywords = [k.strip() for k in args.interests.split(',')]
        matched = match_by_interests(lobsters, keywords)
    
    if args.skills:
        keywords = [k.strip() for k in args.skills.split(',')]
        matched = match_by_skills(lobsters, keywords)
    
    # 课堂模式：按版本号排序，高版本在前（经验更丰富）
    if args.teacher and matched:
        def version_key(lobster):
            version = lobster.get('version', '1.0.0')
            try:
                return tuple(int(p) for p in version.split('.'))
            except:
                return (0, 0, 0)
        matched.sort(key=version_key, reverse=True)
        print(f"🔍 寻找老师，按版本（经验）排序:\n")
    
    # 探索模式：随机打乱，鼓励探索不同对象
    if args.explore and matched:
        import random
        random.shuffle(matched)
        print(f"🔍 探索模式，随机打乱顺序:\n")
    
    print(f"找到 {len(matched)} 只匹配的小龙虾:\n")
    for lobster in matched:
        print_lobster(lobster)

if __name__ == '__main__':
    main()
