#!/usr/bin/env python3
"""
AI游戏创作助手 - 基础实现
集成Aippy式AI游戏创作能力，让用户通过自然语言描述快速生成可玩小游戏
"""

import argparse
import json
import os
from typing import Dict, List
import hashlib


class AIGameCreator:
    """AI游戏创作助手核心类"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.games = self._load_games()
    
    def _load_templates(self) -> List[Dict]:
        """加载游戏模板"""
        templates = [
            {
                "id": "jumping-game",
                "name": "跳跃游戏模板",
                "description": "经典的跳跃类游戏，玩家控制角色跳跃躲避障碍物",
                "prompts": [
                    "创建一个跳跃游戏，玩家控制角色跳跃躲避障碍物",
                    "做一个马里奥式的跳跃闯关游戏"
                ]
            },
            {
                "id": "shooting-game", 
                "name": "射击游戏模板",
                "description": "射击类游戏，玩家控制角色射击敌人",
                "prompts": [
                    "做一个打僵尸的小游戏",
                    "创建一个射击游戏，玩家控制角色射击从右边来的敌人"
                ]
            },
            {
                "id": "puzzle-game",
                "name": "益智游戏模板",
                "description": "益智类游戏，玩家通过思考解决问题",
                "prompts": [
                    "做一个推箱子游戏",
                    "创建一个数字接龙游戏"
                ]
            },
            {
                "id": "collect-game",
                "name": "收集游戏模板",
                "description": "收集类游戏，玩家控制角色收集物品",
                "prompts": [
                    "做一个收集金币的游戏",
                    "创建一个跳跃收集水果的游戏"
                ]
            }
        ]
        return templates
    
    def _load_games(self) -> Dict:
        """加载已有游戏记录"""
        games_file = "games_record.json"
        if os.path.exists(games_file):
            with open(games_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_games(self):
        """保存游戏记录"""
        games_file = "games_record.json"
        with open(games_file, 'w', encoding='utf-8') as f:
            json.dump(self.games, f, ensure_ascii=False, indent=2)
    
    def create_game(self, description: str) -> Dict:
        """根据描述创建游戏"""
        game_id = hashlib.md5(description.encode()).hexdigest()[:8]
        
        # 这里是模拟，实际实现中会调用AI API
        game = {
            "id": game_id,
            "description": description,
            "type": self._detect_game_type(description),
            "created_at": self._get_current_time(),
            "status": "created",
            "code": self._generate_basic_game_code(description)
        }
        
        self.games[game_id] = game
        self._save_games()
        
        return game
    
    def remix_game(self, game_id: str, modifications: str) -> Dict:
        """Remix现有游戏"""
        if game_id not in self.games:
            raise ValueError(f"游戏 {game_id} 不存在")
        
        original_game = self.games[game_id]
        new_game_id = hashlib.md5((game_id + modifications).encode()).hexdigest()[:8]
        
        # 创建Remix版本
        remix_game = {
            "id": new_game_id,
            "description": f"Remix of {original_game['description']} - {modifications}",
            "type": original_game["type"],
            "created_at": self._get_current_time(),
            "status": "remixed",
            "parent_id": game_id,
            "modifications": modifications,
            "code": self._apply_modifications(original_game["code"], modifications)
        }
        
        self.games[new_game_id] = remix_game
        self._save_games()
        
        return remix_game
    
    def list_templates(self) -> List[Dict]:
        """列出所有模板"""
        return self.templates
    
    def _detect_game_type(self, description: str) -> str:
        """检测游戏类型（模拟）"""
        description = description.lower()
        
        if any(keyword in description for keyword in ["跳跃", "jump", "马里奥", "platform"]):
            return "jumping"
        elif any(keyword in description for keyword in ["射击", "打", "shoot", "僵尸", "zombie"]):
            return "shooting"
        elif any(keyword in description for keyword in ["益智", "puzzle", "推箱子", "数字"]):
            return "puzzle"
        elif any(keyword in description for keyword in ["收集", "collect", "金币", "水果"]):
            return "collect"
        else:
            return "casual"
    
    def _generate_basic_game_code(self, description: str) -> str:
        """生成基础游戏代码（HTML5）"""
        # 这是一个简化版本，实际实现会更复杂
        game_type = self._detect_game_type(description)
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Generated Game</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: Arial, sans-serif;
        }}
        #gameContainer {{
            width: 375px;
            height: 667px;
            background: #fff;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            position: relative;
        }}
        #gameCanvas {{
            width: 100%;
            height: 100%;
        }}
        #gameUI {{
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 10;
        }}
        .score {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
        .health {{
            width: 100px;
            height: 10px;
            background: #ddd;
            border-radius: 5px;
            overflow: hidden;
        }}
        .healthBar {{
            width: 100%;
            height: 100%;
            background: #4CAF50;
            transition: width 0.3s;
        }}
        #instructions {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.7);
            color: #fff;
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div id="gameContainer">
        <canvas id="gameCanvas"></canvas>
        <div id="gameUI">
            <div class="score">分数: <span id="scoreValue">0</span></div>
            <div class="health">
                <div class="healthBar" id="healthBar"></div>
            </div>
        </div>
        <div id="instructions">按空格键跳跃，躲避障碍物</div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // 游戏配置
        canvas.width = 375;
        canvas.height = 667;
        
        // 游戏状态
        let gameState = {{
            score: 0,
            health: 100,
            isPlaying: true
        }};
        
        // 玩家
        const player = {{
            x: 50,
            y: 500,
            width: 40,
            height: 60,
            velocityY: 0,
            isJumping: false
        }};
        
        // 障碍物数组
        let obstacles = [];
        
        // 游戏循环
        function gameLoop() {{
            if (!gameState.isPlaying) return;
            
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}
        
        function update() {{
            // 更新玩家
            player.velocityY += 0.8; // 重力
            player.y += player.velocityY;
            
            // 地面碰撞
            if (player.y > 500) {{
                player.y = 500;
                player.velocityY = 0;
                player.isJumping = false;
            }}
            
            // 生成障碍物
            if (Math.random() < 0.02) {{
                obstacles.push({{
                    x: canvas.width,
                    y: 500,
                    width: 30,
                    height: 40,
                    speed: 5
                }});
            }}
            
            // 更新障碍物
            obstacles.forEach((obstacle, index) => {{
                obstacle.x -= obstacle.speed;
                
                // 碰撞检测
                if (player.x < obstacle.x + obstacle.width &&
                    player.x + player.width > obstacle.x &&
                    player.y < obstacle.y + obstacle.height &&
                    player.y + player.height > obstacle.y) {{
                    gameState.health -= 20;
                    updateHealthBar();
                    obstacles.splice(index, 1);
                    
                    if (gameState.health <= 0) {{
                        gameState.isPlaying = false;
                        alert('游戏结束！得分: ' + gameState.score);
                        location.reload();
                    }}
                }}
                
                // 越界检测
                if (obstacle.x + obstacle.width < 0) {{
                    gameState.score += 10;
                    updateScore();
                    obstacles.splice(index, 1);
                }}
            }});
        }}
        
        function draw() {{
            // 清空画布
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // 绘制玩家
            ctx.fillStyle = '#4CAF50';
            ctx.fillRect(player.x, player.y, player.width, player.height);
            
            // 绘制障碍物
            ctx.fillStyle = '#FF5722';
            obstacles.forEach(obstacle => {{
                ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
            }});
            
            // 绘制地面
            ctx.fillStyle = '#8B4513';
            ctx.fillRect(0, 560, canvas.width, 107);
        }}
        
        function jump() {{
            if (!player.isJumping) {{
                player.velocityY = -15;
                player.isJumping = true;
            }}
        }}
        
        function updateScore() {{
            document.getElementById('scoreValue').textContent = gameState.score;
        }}
        
        function updateHealthBar() {{
            document.getElementById('healthBar').style.width = gameState.health + '%';
        }}
        
        // 键盘控制
        document.addEventListener('keydown', (e) => {{
            if (e.code === 'Space') {{
                e.preventDefault();
                jump();
            }}
        }});
        
        // 触控控制
        canvas.addEventListener('touchstart', (e) => {{
            e.preventDefault();
            jump();
        }});
        
        // 开始游戏
        gameLoop();
    </script>
</body>
</html>'''
    
    def _apply_modifications(self, original_code: str, modifications: str) -> str:
        """应用修改到游戏代码（模拟）"""
        # 这里是简化实现，实际会调用AI来理解修改意图并修改代码
        modified_code = original_code
        
        modifications = modifications.lower()
        
        if "连击" in modifications:
            # 添加连击系统
            modified_code = modified_code.replace(
                '// 游戏状态',
                '// 游戏状态\n        let comboCount = 0;\n        let comboTimer = null;'
            )
            modified_code = modified_code.replace(
                'gameState.score += 10;',
                'gameState.score += 10;\n                    comboCount++;\n                    clearTimeout(comboTimer);\n                    comboTimer = setTimeout(() => comboCount = 0, 2000);\n                    if (comboCount >= 3) gameState.score += 5;'
            )
        
        if "血量" in modifications:
            # 血量条已经在基础代码中
            pass
        
        return modified_code
    
    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description='AI游戏创作助手')
    parser.add_argument('command', choices=['create', 'remix', 'templates'], help='命令')
    parser.add_argument('--description', '-d', help='游戏描述')
    parser.add_argument('--template', '-t', help='使用模板')
    parser.add_argument('--game-id', '-g', help='游戏ID')
    parser.add_argument('--modifications', '-m', help='修改描述')
    
    args = parser.parse_args()
    
    creator = AIGameCreator()
    
    if args.command == 'create':
        if args.template:
            # 使用模板创建
            template = next((t for t in creator.templates if t['id'] == args.template), None)
            if template:
                description = template['prompts'][0]
                print(f"🎮 使用模板: {template['name']}")
                game = creator.create_game(description)
            else:
                print(f"❌ 找不到模板: {args.template}")
                return
        elif args.description:
            # 直接创建
            game = creator.create_game(args.description)
        else:
            print("❌ 请提供游戏描述或模板")
            return
        
        print(f"✅ 游戏创建成功！")
        print(f"📝 游戏ID: {game['id']}")
        print(f"🎯 游戏类型: {game['type']}")
        print(f"📄 代码已保存，可以导出为HTML文件运行")
        
        # 保存游戏文件
        game_file = f"game_{game['id']}.html"
        with open(game_file, 'w', encoding='utf-8') as f:
            f.write(game['code'])
        print(f"📦 游戏文件: {game_file}")
    
    elif args.command == 'remix':
        if not args.game_id or not args.modifications:
            print("❌ Remix需要游戏ID和修改描述")
            return
        
        remix_game = creator.remix_game(args.game_id, args.modifications)
        print(f"✅ Remix创建成功！")
        print(f"📝 Remix ID: {remix_game['id']}")
        print(f"🎯 原游戏: {remix_game['parent_id']}")
        print(f"✨ 修改: {remix_game['modifications']}")
        
        # 保存Remix文件
        remix_file = f"remix_{remix_game['id']}.html"
        with open(remix_file, 'w', encoding='utf-8') as f:
            f.write(remix_game['code'])
        print(f"📦 Remix文件: {remix_file}")
    
    elif args.command == 'templates':
        print("🎨 可用游戏模板:")
        print()
        for template in creator.templates:
            print(f"📌 {template['name']} ({template['id']})")
            print(f"   {template['description']}")
            print(f"   示例: {template['prompts'][0]}")
            print()
        print("💡 使用方法: molili ai-game-creator create --template <模板ID>")


if __name__ == "__main__":
    main()