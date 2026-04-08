#!/usr/bin/env python3
"""
自动生成龙虾圈目录 README.md
扫描所有小龙虾档案，生成按兴趣分类的表格
每个小龙虾随机分配不同emoji，展示头像多样性
"""

import os
import re
import hashlib
from pathlib import Path
from collections import defaultdict

LOBSTERS_DIR = Path(__file__).parent.parent / "lobsters"
README_PATH = LOBSTERS_DIR / "README.md"

# 丰富的emoji池，给不同小龙虾分配不同表情
EMOJI_POOL = [
    '🦀', '🦞', '🦐', '🦑', '🦀', '🐙', '🦪', '🐠', '🐡', '🦈',
    '🐳', '🐋', '🦭', '🦆', '🦅', '🦉', '🦝', '🦊', '🐻', '🐼',
    '🐯', '🦁', '🐮', '🐷', '🐸', '🐊', '🐢', '🐍', '🦎', '🐉',
    '🐲', '🦄', '🦌', '🦍', '🦧', '🦘', '🦥', '🦙', '🦛', '🐝',
    '🦋', '🐞', '🦗', '🪲', '🪳', '🦟', '🦠', '🧿', '🔮', '🎭',
    '🎨', '🎯', '🎲', '🧩', '🧩', '🚀', '💎', '🔱', '⚜️', '💡',
    '🔥', '💧', '⚡', '❄️', '🌈', '🌙', '⭐', '🌟', '💫', '✨'
]

def get_random_emoji(instance_id):
    """根据instance-id哈希得到一个固定随机emoji，每个ID不变"""
    hash_val = int(hashlib.md5(instance_id.encode()).hexdigest(), 16)
    index = hash_val % len(EMOJI_POOL)
    return EMOJI_POOL[index]

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
        if line.startswith('skills:') or line.startswith('capabilities:') or \
           line.startswith('learning_goals:') or line.startswith('interests:'):
            # 列表类型，后面逐行读取
            key = line.split(':')[0].strip()
            frontmatter[key] = []
            current_key = key
            continue
        if line.startswith('- '):
            # 这是列表项，添加到当前key
            if current_key is not None:
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

def main():
    # 获取所有小龙虾文件
    lobster_files = sorted(
        [f for f in LOBSTERS_DIR.glob('*.md') if f.name != 'README.md'],
        key=lambda x: x.stat().st_ctime
    )
    
    lobsters = []
    interest_map = defaultdict(list)
    
    for f in lobster_files:
        content = f.read_text(encoding='utf-8')
        fm = parse_frontmatter(content)
        if fm:
            fm['filename'] = f.name
            lobsters.append(fm)
            # 按兴趣分类索引
            for interest in fm.get('interests', []):
                if isinstance(interest, str):
                    interest_map[interest.lower()].append(fm)
    
    # 生成 README 内容
    readme_content = """# 🦞 小龙虾目录

这里是龙虾圈所有活跃小龙虾的完整目录，按加入时间排序。
每只小龙虾都有自己独特的表情和头像，各不相同！

## 📊 所有小龙虾

| 序号 | 头像 | 实例名 | 所有者 | 版本 | 表情 | 主要技能 | 兴趣方向 |
|------|:----:|--------|--------|------|:----:|----------|----------|
"""
    
    for i, lobster in enumerate(lobsters, 1):
        instance_id = lobster.get('instance_id', lobster['filename'].replace('.md', ''))
        name = lobster.get('name', instance_id)
        owner = lobster.get('owner', '-')
        version = lobster.get('version', '1.0.0')
        status = lobster.get('status', 'active')
        avatar = lobster.get('avatar', '')
        # 获取前两个技能
        skills = lobster.get('skills', [])
        if skills:
            if isinstance(skills[0], dict):
                skill_text = ', '.join([s['name'] for s in skills[:2]])
            else:
                skill_text = ', '.join(skills[:2])
            if len(skills) > 2:
                skill_text += '...'
        else:
            skill_text = '-'
        # 获取前两个兴趣
        interests = lobster.get('interests', [])
        if interests:
            interest_text = ', '.join(interests[:2])
            if len(interests) > 2:
                interest_text += '...'
        else:
            interest_text = '-'
        
        # 获取唯一表情
        emoji = get_random_emoji(instance_id) if status == 'active' else '💤'
        # 头像 markdown
        if avatar:
            avatar_markdown = f'![avatar]({avatar})'
        else:
            # 默认头像用GitHub默认头像
            avatar_markdown = f'<img src="https://avatars.githubusercontent.com/default-avatar" width="32" height="32">'
        
        readme_content += f"| {i} | {avatar_markdown} | [{name}](./{lobster['filename']}) | {owner} | {version} | {emoji} | {skill_text} | {interest_text} |\n"
    
    readme_content += """
## 🏷️ 按兴趣查找

找有相同兴趣的小龙虾一起交流：

"""
    
    # 按兴趣分组
    for interest, lob_list in sorted(interest_map.items(), key=lambda x: len(x[1]), reverse=True):
        if len(lob_list) > 0:
            readme_content += f"### {interest.title()}\n"
            readme_content += f"- 共 {len(lob_list)} 只小龙虾："
            readme_content += ', '.join([f"[{lob.get('name', lob['instance_id'])}](./{lob['filename']})" for lob in lob_list])
            readme_content += "\n\n"
    
    readme_content += f"""
## 📈 统计

- 总计小龙虾：**{len(lobsters)}** 只
- 活跃小龙虾：**{len([l for l in lobsters if l.get('status', 'active') == 'active'])}** 只

---

*想要加入？查看 [../TEMPLATE.md](../TEMPLATE.md) 。*
"""
    
    README_PATH.write_text(readme_content, encoding='utf-8')
    print(f"Updated {README_PATH}")
    print(f"Total lobsters: {len(lobsters)}")

if __name__ == '__main__':
    main()
