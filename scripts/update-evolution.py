#!/usr/bin/env python3
"""
交流结束后，更新小龙虾的进化记录和版本号
用法:
  python update-evolution.py --instance instance-id --learned "学到了xxx"
"""

import argparse
import re
from pathlib import Path
from datetime import datetime

LOBSTERS_DIR = Path(__file__).parent.parent / "lobsters"

def bump_version(version: str) -> str:
    """升级次版本号: 1.0.0 → 1.1.0"""
    parts = version.split('.')
    if len(parts) >= 2:
        parts[1] = str(int(parts[1]) + 1)
        return '.'.join(parts)
    return version + ".1.0"

def main():
    parser = argparse.ArgumentParser(description='更新小龙虾进化记录')
    parser.add_argument('--instance', '-i', required=True, help='小龙虾实例ID')
    parser.add_argument('--learned', '-l', required=True, help='学到了什么（描述）')
    parser.add_argument('--from', '-f', required=True, help='从谁那里学到的（实例ID）')
    args = parser.parse_args()
    
    # 找到文件
    lobster_file = None
    for f in LOBSTERS_DIR.glob(f'{args.instance}.md'):
        lobster_file = f
        break
    if not lobster_file:
        for f in LOBSTERS_DIR.glob('*.md'):
            if args.instance in f.name:
                lobster_file = f
                break
    if not lobster_file:
        print(f"找不到小龙虾文件: {args.instance}")
        return
    
    content = lobster_file.read_text(encoding='utf-8')
    
    # 解析当前版本
    pattern = r'version:\s*["\']?([\d\.]+)["\']?'
    match = re.search(pattern, content)
    if not match:
        current_version = "1.0.0"
    else:
        current_version = match.group(1)
    
    new_version = bump_version(current_version)
    print(f"版本升级: {current_version} → {new_version}")
    
    # 更新版本号
    content = re.sub(pattern, f'version: "{new_version}"', content)
    
    # 更新进化历程
    today = datetime.now().strftime("%Y-%m-%d")
    evolution_add = f"- v{new_version} ({today}) - 从 @{args.from} 学到了: {args.learned}"
    
    # 找到当前版本标记
    pattern = r'-\s*\*\*当前版本：.*\*\*'
    match = re.search(pattern, content)
    if match:
        # 在当前版本之前插入新版本
        before = content[:match.start()]
        after = content[match.start():]
        # 找到进化历程段落位置插入新行
        new_content = before + evolution_add + '\n' + after
        # 更新当前版本标记
        new_content = re.sub(pattern, f'- **当前版本：v{new_version}** - 等待新的交流启发...', new_content)
        content = new_content
    else:
        # 找不到就加在末尾
        content += f'\n{evolution_add}\n'
    
    lobster_file.write_text(content, encoding='utf-8')
    print(f"✅ 已更新 {lobster_file.name}")
    print(f"   版本: {new_version}")
    print(f"   进化: {args.learned} (from @{args.from})")

if __name__ == '__main__':
    main()
