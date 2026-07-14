---
summary: "MemGit 记忆系统架构全景 — AI 的入口地图"
read_when:
  - 会话启动时（第一个读）
write_rules: |
  结构说明文件，不需频繁更新
  架构变化时更新此文件，同时追加 CHANGELOG.md
---

# MemGit 记忆架构

> AI 启动后先读这个文件，理解整个记忆系统，然后再按索引加载具体内容。

## 目录结构

```
memories/
├── MEMORY-ARCHITECTURE.md          # 本文件 — 架构总览（先读）
├── CHANGELOG.md                    # 架构演化记录
├── SKILL.md                        # 执行流程定义（仓库内备份）
├── scripts/memgit.py               # 管理脚本
├── IDENTITY.md                     # 用户身份（必读）
├── INDEX.md                        # 知识文件索引
│
├── knowledge/                      # 个人记忆
│   ├── events.md                   # 近期事件（时间段）
│   ├── system-signals.md           # 系统自学习信号
│   ├── principles.md               # 价值观原则
│   ├── habits.md                   # 习惯风格
│   ├── investments.md              # 投资
│   ├── learning.md                 # 学习
│   ├── life.md                     # 生活
│   └── goals.md                    # 目标
│
├── projects/                       # 项目记忆
│   ├── INDEX.md                    # 项目索引
│   ├── <project-name>.md           # 项目决策+进度
│   └── archive/                    # 已归档
│
├── library/                        # 代码/资料（AI 按需读）
│   └── <topic>/                    # 按技术栈分类
│
└── strategies/                     # 记忆维护策略
    ├── INDEX.md                    # 策略索引
    ├── system-control.md           # 控制规则（启动必读）
    ├── self-growth.md              # 合并/压缩（按需）
    ├── proactive-usage.md          # 主动使用（按需）
    └── emotional-awareness.md      # 情绪感知（按需）
```

## 启动加载流程（详见 SKILL.md）

```
config → git pull → ARCHITECTURE → system-control → IDENTITY
→ events → 自检 → INDEX → projects → knowledge 渐进读 → 启动摘要
```

## 每种内容的读取策略

| 内容类型 | 什么时候读 | 读多少 |
|---------|-----------|--------|
| IDENTITY.md | 每次会话 | 全文 |
| events.md | 每次会话 | 全文（很薄） |
| INDEX.md | 每次会话 | 「常用」层，不够再看「全部」 |
| knowledge/ 文件 | 话题相关时 | Summary → H2 跳读 |
| projects/ 文件 | 提及项目时 | Summary |
| library/ 文件 | 需要代码参考时 | 按 H2 跳读 |
| strategies/ 文件 | 按需（system-control.md 除外） | 按场景 |

## 新记忆类型的自适应协议

当 AI 发现一段信息**不属于任何现有类别**时：

1. **提出**："这个信息（描述内容）不属于现有类别，建议新建 `knowledge/xxx.md`，用于记录（用途）。是否创建？"
2. **等用户确认**（不改架构不经用户同意）
3. **实现**：按模板创建文件 → 写 write_rules → 注册到 INDEX.md → 追加 CHANGELOG.md
4. **反思**：如果同一类新类别的创建请求出现 3 次以上，AI 主动提议将该类别纳入初始模板
