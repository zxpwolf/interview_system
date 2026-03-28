# 交互式 技能考察系统

🎓 **针对岗位需求的交互式技能测评与练习系统**

---

## 📋 项目简介

是一个交互式技能考察系统，专为 DBA 岗位设计，提供：

- ✅ **技能等级测评** - AWS/Python/数据库三大领域
- ✅ **专项练习** - 针对性强化训练
- ✅ **错题集管理** - 自动记录、间隔复习
- ✅ **进度跟踪** - 等级变化、掌握率统计

---

## 🚀 快速开始

### 安装依赖

```bash
cd /Users/Wolf/.openclaw/workspace/projects/BayerDBA
pip install -r requirements.txt
```

### 启动系统

```bash
# 主菜单模式
python scripts/assess.py

# 直接测评指定技能
python scripts/assess.py --skill aws       # AWS 技能测评
python scripts/assess.py --skill python    # Python 技能测评
python scripts/assess.py --skill database  # 数据库技能测评
```

---

## 📊 技能领域

### 1. AWS 云技能 (35%)

| 子领域 | 题目数 | 考察重点 |
|--------|--------|----------|
| IAM & 权限 | 5 题 | 角色、策略、跨账号访问 |
| 安全 | 5 题 | KMS、Security Groups、GuardDuty |
| 计算 | 5 题 | EC2、Auto Scaling、Lambda |
| 存储 | 5 题 | S3、EBS、EFS |
| 网络 | 5 题 | VPC、子网、NAT、Transit Gateway |

### 2. Python 技能 (30%)

| 子领域 | 题目数 | 考察重点 |
|--------|--------|----------|
| API 调用 | 5 题 | requests、认证、错误处理、异步 |
| 脚本开发 | 5 题 | JSON、argparse、logging、subprocess |
| 运维自动化 | 5 题 | boto3、定时任务、断点续传 |

### 3. 数据库技能 (35%)

| 子领域 | 题目数 | 考察重点 |
|--------|--------|----------|
| 权限管理 | 5 题 | GRANT/REVOKE、角色、列级权限 |
| 安全管理 | 5 题 | SSL/TLS、TDE、SQL 注入、审计 |
| 备份管理 | 5 题 | 备份类型、PITR、RPO/RTO |
| 性能优化 | 5 题 | 索引、EXPLAIN、锁机制 |

---

## 🎯 等级划分

| 等级 | 分数范围 | 描述 |
|------|----------|------|
| L1 - 初级 | 0-40 分 | 基础概念了解，需要系统学习 |
| L2 - 中级 | 41-70 分 | 掌握核心技能，可独立完成常规任务 |
| L3 - 高级 | 71-85 分 | 深入理解，能解决复杂问题 |
| L4 - 专家 | 86-100 分 | 精通领域，可指导他人 |

---

## 📖 使用流程

### 技能测评流程

```
1. 选择技能领域 (AWS/Python/数据库)
   ↓
2. 回答 10 道随机题目
   ↓
3. 即时反馈 (正确/错误 + 解析)
   ↓
4. 错题自动加入错题集
   ↓
5. 生成等级评估 + 学习建议
```

### 错题复习流程

```
1. 选择"错题复习"
   ↓
2. 系统筛选到期错题 (1 天/3 天后)
   ↓
3. 重新作答
   ↓
4. 连续 2 次正确 → 标记为"已掌握"
   ↓
5. 错误 → 1 天后再次复习
```

---

## 📁 项目结构

```
BayerDBA/
├── PROJECT_PLAN.md          # 项目规划
├── README.md                # 本文档
├── requirements.txt         # Python 依赖
├── config/
│   ├── skills.yaml          # 技能树配置
│   └── levels.yaml          # 等级定义
├── questions/
│   ├── aws_cloud.yaml       # AWS 题库 (30 题)
│   ├── python_skills.yaml   # Python 题库 (15 题)
│   └── database_skills.yaml # 数据库题库 (20 题)
├── scripts/
│   ├── assess.py            # 技能测评脚本
│   ├── practice.py          # 专项练习脚本 (TODO)
│   ├── review.py            # 错题复习脚本 (TODO)
│   └── progress.py          # 进度查看脚本 (TODO)
├── data/
│   ├── user_progress.json   # 用户进度
│   ├── mistake_book.json    # 错题集
│   └── history.json         # 练习历史
└── reports/
    └── progress_report.md   # 进度报告
```

---

## 💡 功能特性

### 1. 交互式测评

- 📝 选择题形式 (A/B/C/D)
- ✅ 即时正误判断
- 💡 详细知识点解析
- 🔄 可随时退出 (y/n 控制)

### 2. 错题集管理

- 📝 自动记录错题
- 🔄 间隔重复 (1 天、3 天、7 天)
- ✅ 掌握标记 (连续 2 次正确)
- 📊 状态跟踪 (pending/reviewing/mastered)

### 3. 进度跟踪

- 📈 各技能领域等级
- 📊 答题数量统计
- 📅 最近测评时间
- 🎯 学习建议

---

## 📊 数据格式

### 用户进度 (user_progress.json)

```json
{
  "user_id": "default",
  "created_at": "2026-03-08T11:40:00",
  "last_active": "2026-03-08T11:40:00",
  "skills": {
    "aws": {
      "level": "L2 - 中级",
      "score": 65,
      "last_assessment": "2026-03-08T11:40:00",
      "questions_answered": 10
    }
  }
}
```

### 错题集 (mistake_book.json)

```json
{
  "mistakes": [
    {
      "id": "aws_iam_001",
      "skill": "aws",
      "question": "题目内容...",
      "user_answer": "A",
      "correct_answer": "B",
      "explanation": "解析...",
      "review_at": "2026-03-09T11:40:00",
      "review_count": 0,
      "consecutive_correct": 0,
      "status": "pending"
    }
  ]
}
```

---

## 🎮 使用示例

### 示例 1: 主菜单模式

```bash
$ python scripts/assess.py

============================================================
  🎓 BayerDBA 技能考察系统
============================================================

请选择技能领域:
  1. AWS 云技能 (IAM/安全/计算/存储/网络)
  2. Python 技能 (API/脚本/运维)
  3. 数据库技能 (权限/安全/备份/性能)
  4. 查看进度
  5. 错题复习
  6. 退出

你的选择 (1-6): 1

============================================================
  📊 AWS 技能等级测评
============================================================

📝 题目 1/10
难度：L1

在 AWS IAM 中，以下哪种方式是授予 EC2 实例访问 S3 存储桶权限的最佳实践？

  A. 将 AWS Access Key 和 Secret Key 硬编码在应用程序中
  B. 创建 IAM 用户并将凭证存储在 EC2 实例的用户数据中
  C. 创建 IAM 角色并将其附加到 EC2 实例
  D. 使用根账户创建 Access Key 并传递给 EC2 实例

你的答案 (A/B/C/D): C

✅ 正确！

继续下一题？(y/n): y
...
```

### 示例 2: 直接测评

```bash
$ python scripts/assess.py --skill python

============================================================
  📊 PYTHON 技能等级测评
============================================================

📝 题目 1/10
难度：L2

处理 API 速率限制 (Rate Limiting) 的最佳做法是？
...
```

---

## 📈 后续开发计划

| 功能 | 状态 | 说明 |
|------|------|------|
| 技能测评 | ✅ 完成 | 三大领域测评 |
| 错题集 | ✅ 完成 | 自动记录 + 间隔复习 |
| 进度跟踪 | ✅ 完成 | 等级 + 统计 |
| 专项练习 | ⏳ 计划 | 按技能点针对性练习 |
| 报告生成 | ⏳ 计划 | PDF/Markdown 报告 |
| Web 界面 | ⏳ 计划 | 浏览器访问 |
| 多用户 | ⏳ 计划 | 用户登录 + 数据隔离 |

---

## 🤝 贡献

欢迎贡献题目或改进功能！

### 添加新题目

在对应题库文件中添加：

```yaml
### aws_new_001
**难度:** L2  
**题目:** 题目内容？

A. 选项 A  
B. 选项 B  
C. 选项 C  
D. 选项 D  

**正确答案:** A  
**解析:** 详细解析...  
**知识点:** 知识点...  
**标签:** tag1, tag2
```

---

## 📞 支持

- 项目规划：[PROJECT_PLAN.md](PROJECT_PLAN.md)
- 问题反馈：创建 Issue

---

*版本：v1.0*  
*创建时间：2026-03-08*
