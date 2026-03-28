#!/usr/bin/env python3
"""
BayerDBA 交互式技能测评系统

使用方法:
    python scripts/assess.py          # 主菜单
    python scripts/assess.py --skill aws      # AWS 技能测评
    python scripts/assess.py --skill python   # Python 技能测评
    python scripts/assess.py --skill database # 数据库技能测评
"""

import argparse
import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
QUESTIONS_DIR = PROJECT_ROOT / 'questions'
DATA_DIR = PROJECT_ROOT / 'data'
REPORTS_DIR = PROJECT_ROOT / 'reports'

# 确保数据目录存在
DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# 数据文件
USER_PROGRESS_FILE = DATA_DIR / 'user_progress.json'
MISTAKE_BOOK_FILE = DATA_DIR / 'mistake_book.json'
HISTORY_FILE = DATA_DIR / 'history.json'


def load_questions(skill: str) -> List[Dict[str, Any]]:
    """加载题库"""
    question_files = {
        'aws': 'aws_cloud.yaml',
        'python': 'python_skills.yaml',
        'database': 'database_skills.yaml',
    }
    
    if skill not in question_files:
        print(f"❌ 未知技能：{skill}")
        return []
    
    file_path = QUESTIONS_DIR / question_files[skill]
    if not file_path.exists():
        print(f"❌ 题库文件不存在：{file_path}")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 YAML (按题目分割)
    questions = []
    current_question = {}
    
    for line in content.split('\n'):
        if line.startswith('### '):
            if current_question:
                questions.append(current_question)
            current_question = {'id': line[4:].strip()}
        elif line.startswith('**'):
            # 解析加粗字段
            if '**难度:**' in line:
                current_question['difficulty'] = line.split('**难度:**')[1].strip()
            elif '**题目:**' in line:
                current_question['question'] = line.split('**题目:**')[1].strip()
            elif '**正确答案:**' in line:
                current_question['answer'] = line.split('**正确答案:**')[1].strip()
            elif '**解析:**' in line:
                current_question['explanation'] = line.split('**解析:**')[1].strip()
            elif '**知识点:**' in line:
                current_question['knowledge_points'] = line.split('**知识点:**')[1].strip()
            elif '**标签:**' in line:
                current_question['tags'] = line.split('**标签:**')[1].strip()
        elif line.strip().startswith(('A.', 'B.', 'C.', 'D.')):
            if 'options' not in current_question:
                current_question['options'] = {}
            parts = line.strip().split('. ', 1)
            if len(parts) == 2:
                current_question['options'][parts[0]] = parts[1]
    
    if current_question:
        questions.append(current_question)
    
    return questions


def load_user_progress() -> Dict[str, Any]:
    """加载用户进度"""
    if not USER_PROGRESS_FILE.exists():
        return {
            'user_id': 'default',
            'created_at': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat(),
            'skills': {}
        }
    
    with open(USER_PROGRESS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_user_progress(progress: Dict[str, Any]):
    """保存用户进度"""
    progress['last_active'] = datetime.now().isoformat()
    with open(USER_PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def load_mistake_book() -> Dict[str, Any]:
    """加载错题集"""
    if not MISTAKE_BOOK_FILE.exists():
        return {'mistakes': []}
    
    with open(MISTAKE_BOOK_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_mistake_book(mistake_book: Dict[str, Any]):
    """保存错题集"""
    with open(MISTAKE_BOOK_FILE, 'w', encoding='utf-8') as f:
        json.dump(mistake_book, f, indent=2, ensure_ascii=False)


def save_history(record: Dict[str, Any]):
    """保存练习历史"""
    history = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    
    history.append(record)
    
    # 保留最近 1000 条
    if len(history) > 1000:
        history = history[-1000:]
    
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def get_level(score: int) -> str:
    """根据分数获取等级"""
    if score >= 86:
        return 'L4 - 专家'
    elif score >= 71:
        return 'L3 - 高级'
    elif score >= 41:
        return 'L2 - 中级'
    else:
        return 'L1 - 初级'


def run_assessment(skill: str, questions: List[Dict[str, Any]], progress: Dict[str, Any]):
    """运行技能测评"""
    print(f"\n{'='*60}")
    print(f"  📊 {skill.upper()} 技能等级测评")
    print(f"{'='*60}\n")
    
    # 随机选择 10 题
    if len(questions) < 10:
        print(f"⚠️  题库只有 {len(questions)} 题，将全部展示")
        selected_questions = questions
    else:
        selected_questions = random.sample(questions, 10)
    
    correct_count = 0
    answers = []
    
    for i, q in enumerate(selected_questions, 1):
        print(f"\n📝 题目 {i}/10")
        print(f"难度：{q.get('difficulty', '未知')}")
        print(f"\n{q.get('question', '')}\n")
        
        # 显示选项
        options = q.get('options', {})
        for key, value in sorted(options.items()):
            print(f"  {key}. {value}")
        
        # 获取答案
        while True:
            user_answer = input("\n你的答案 (A/B/C/D): ").strip().upper()
            if user_answer in ['A', 'B', 'C', 'D']:
                break
            print("请输入 A/B/C/D")
        
        # 判断正误
        correct_answer = q.get('answer', '')
        is_correct = user_answer == correct_answer
        
        if is_correct:
            print(f"\n✅ 正确！")
            correct_count += 1
        else:
            print(f"\n❌ 错误！正确答案是：{correct_answer}")
            print(f"\n💡 解析：{q.get('explanation', '')}")
            
            # 记录错题
            mistake = {
                'id': q.get('id', f'{skill}_{i}'),
                'skill': skill,
                'question': q.get('question', ''),
                'options': q.get('options', {}),
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'explanation': q.get('explanation', ''),
                'knowledge_points': q.get('knowledge_points', ''),
                'created_at': datetime.now().isoformat(),
                'review_at': (datetime.now() + timedelta(days=1)).isoformat(),
                'review_count': 0,
                'consecutive_correct': 0,
                'status': 'pending'
            }
            
            mistake_book = load_mistake_book()
            # 避免重复
            existing_ids = [m['id'] for m in mistake_book['mistakes']]
            if mistake['id'] not in existing_ids:
                mistake_book['mistakes'].append(mistake)
                save_mistake_book(mistake_book)
                print(f"📝 已加入错题集，将在 1 天后复习")
        
        # 保存历史
        save_history({
            'timestamp': datetime.now().isoformat(),
            'skill': skill,
            'question_id': q.get('id', ''),
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })
        
        # 询问是否继续
        if i < len(selected_questions):
            while True:
                cont = input("\n继续下一题？(y/n): ").strip().lower()
                if cont in ['y', 'yes', '是']:
                    break
                elif cont in ['n', 'no', '否']:
                    # 计算当前得分
                    score = int((correct_count / i) * 100)
                    print(f"\n{'='*60}")
                    print(f"  测评提前结束")
                    print(f"  当前得分：{correct_count}/{i} ({score}分)")
                    print(f"  等级：{get_level(score)}")
                    print(f"{'='*60}\n")
                    return
                else:
                    print("请输入 y/n")
    
    # 测评完成
    score = int((correct_count / len(selected_questions)) * 100)
    level = get_level(score)
    
    print(f"\n{'='*60}")
    print(f"  ✅ 测评完成！")
    print(f"{'='*60}")
    print(f"  📊 得分：{correct_count}/{len(selected_questions)} ({score}分)")
    print(f"  🏆 等级：{level}")
    print(f"{'='*60}\n")
    
    # 更新进度
    if skill not in progress['skills']:
        progress['skills'][skill] = {}
    
    progress['skills'][skill]['level'] = level
    progress['skills'][skill]['score'] = score
    progress['skills'][skill]['last_assessment'] = datetime.now().isoformat()
    progress['skills'][skill]['questions_answered'] = \
        progress['skills'][skill].get('questions_answered', 0) + len(selected_questions)
    
    save_user_progress(progress)
    
    # 学习建议
    print(f"📚 学习建议:\n")
    if score < 41:
        print("  基础较弱，建议从基础概念开始系统学习。")
        print("  推荐：官方文档 + 基础教程 + 动手实验")
    elif score < 71:
        print("  掌握核心概念，建议加强实践和深入理解。")
        print("  推荐：实战项目 + 专项练习 + 错题复习")
    elif score < 86:
        print("  水平较好，建议查漏补缺，攻克难点。")
        print("  推荐：高级主题 + 复杂场景 + 最佳实践")
    else:
        print("  非常优秀！建议保持学习，关注新技术。")
        print("  推荐：技术分享 + 指导他人 + 前沿探索")
    
    print()


def main_menu():
    """主菜单"""
    print(f"\n{'='*60}")
    print(f"  🎓 BayerDBA 技能考察系统")
    print(f"{'='*60}\n")
    
    progress = load_user_progress()
    
    while True:
        print("请选择技能领域:")
        print("  1. AWS 云技能 (IAM/安全/计算/存储/网络)")
        print("  2. Python 技能 (API/脚本/运维)")
        print("  3. 数据库技能 (权限/安全/备份/性能)")
        print("  4. 查看进度")
        print("  5. 错题复习")
        print("  6. 退出")
        print()
        
        choice = input("你的选择 (1-6): ").strip()
        
        if choice == '1':
            questions = load_questions('aws')
            if questions:
                run_assessment('aws', questions, progress)
        elif choice == '2':
            questions = load_questions('python')
            if questions:
                run_assessment('python', questions, progress)
        elif choice == '3':
            questions = load_questions('database')
            if questions:
                run_assessment('database', questions, progress)
        elif choice == '4':
            show_progress(progress)
        elif choice == '5':
            review_mistakes()
        elif choice == '6':
            print("\n👋 再见！欢迎下次再来练习~\n")
            break
        else:
            print("无效选择，请重新输入\n")


def show_progress(progress: Dict[str, Any]):
    """显示进度"""
    print(f"\n{'='*60}")
    print(f"  📊 学习进度")
    print(f"{'='*60}\n")
    
    print(f"用户：{progress.get('user_id', 'default')}")
    print(f"创建时间：{progress.get('created_at', '未知')[:10]}")
    print(f"最后活跃：{progress.get('last_active', '未知')[:10]}")
    print()
    
    skills = progress.get('skills', {})
    if not skills:
        print("  暂无测评记录，先做个测评吧~\n")
    else:
        for skill, data in skills.items():
            level = data.get('level', '未知')
            score = data.get('score', 0)
            answered = data.get('questions_answered', 0)
            last = data.get('last_assessment', '未知')[:10]
            
            print(f"  {skill.upper()}:")
            print(f"    等级：{level}")
            print(f"    分数：{score}")
            print(f"    答题数：{answered}")
            print(f"    最近测评：{last}")
            print()
    
    # 错题统计
    mistake_book = load_mistake_book()
    mistakes = mistake_book.get('mistakes', [])
    pending = len([m for m in mistakes if m['status'] == 'pending'])
    reviewing = len([m for m in mistakes if m['status'] == 'reviewing'])
    mastered = len([m for m in mistakes if m['status'] == 'mastered'])
    
    print(f"  错题集:")
    print(f"    待复习：{pending}")
    print(f"    复习中：{reviewing}")
    print(f"    已掌握：{mastered}")
    print()


def review_mistakes():
    """错题复习"""
    mistake_book = load_mistake_book()
    mistakes = mistake_book.get('mistakes', [])
    
    # 筛选待复习的错题
    now = datetime.now()
    due_mistakes = [
        m for m in mistakes
        if m['status'] in ['pending', 'reviewing']
        and datetime.fromisoformat(m['review_at']) <= now
    ]
    
    if not due_mistakes:
        print("\n🎉 暂无待复习的错题！\n")
        return
    
    print(f"\n{'='*60}")
    print(f"  📚 错题复习 ({len(due_mistakes)} 题待复习)")
    print(f"{'='*60}\n")
    
    for i, m in enumerate(due_mistakes, 1):
        print(f"\n📝 复习题 {i}/{len(due_mistakes)}")
        print(f"错题 ID: {m['id']}")
        print(f"复习次数：{m['review_count']}")
        print(f"\n{m['question']}\n")
        
        # 显示选项
        options = m.get('options', {})
        for key, value in sorted(options.items()):
            print(f"  {key}. {value}")
        
        while True:
            user_answer = input("\n你的答案 (A/B/C/D): ").strip().upper()
            if user_answer in ['A', 'B', 'C', 'D']:
                break
            print("请输入 A/B/C/D")
        
        is_correct = user_answer == m['correct_answer']
        
        if is_correct:
            print(f"\n✅ 正确！")
            m['consecutive_correct'] += 1
            
            if m['consecutive_correct'] >= 2:
                m['status'] = 'mastered'
                print(f"🎉 连续 2 次正确，已标记为已掌握！")
            else:
                m['status'] = 'reviewing'
                # 下次复习时间 (3 天后)
                m['review_at'] = (now + timedelta(days=3)).isoformat()
        else:
            print(f"\n❌ 错误！正确答案是：{m['correct_answer']}")
            print(f"\n💡 解析：{m['explanation']}")
            m['consecutive_correct'] = 0
            m['status'] = 'reviewing'
            # 下次复习时间 (1 天后)
            m['review_at'] = (now + timedelta(days=1)).isoformat()
        
        m['review_count'] += 1
        
        # 保存
        save_mistake_book(mistake_book)
        
        # 询问是否继续
        if i < len(due_mistakes):
            while True:
                cont = input("\n继续下一题？(y/n): ").strip().lower()
                if cont in ['y', 'yes', '是']:
                    break
                elif cont in ['n', 'no', '否']:
                    print("\n👋 复习结束，加油！\n")
                    return
                else:
                    print("请输入 y/n")
    
    print(f"\n{'='*60}")
    print(f"  ✅ 复习完成！")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BayerDBA 技能测评系统')
    parser.add_argument('--skill', choices=['aws', 'python', 'database'],
                       help='指定技能领域 (不指定则显示主菜单)')
    
    args = parser.parse_args()
    
    if args.skill:
        # 直接测评指定技能
        progress = load_user_progress()
        questions = load_questions(args.skill)
        if questions:
            run_assessment(args.skill, questions, progress)
    else:
        # 主菜单
        main_menu()
