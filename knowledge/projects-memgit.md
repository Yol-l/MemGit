---
summary: "MemGit 项目设计决策记录"
read_when:
  - 继续迭代 MemGit 时
  - 回顾设计思路时
---

# MemGit 项目

## Summary

MemGit 是一个 Git 驱动的 AI 长期记忆系统，任何人都可以通过 fork 模板仓库 + 运行 setup 来使用。核心设计目标是：记长期有用的事，不做短期会话记录。

## 架构决策

### 2026-07-13: 记忆结构只存长期信息
- **Context**: 最初包含 session 日志，后来发现短期信息没有保存价值
- **Decision**: 去掉 sessions/ 目录，只保留 IDENTITY.md + knowledge/ 下的长期知识文件
- **Rationale**: AI 的记忆应该像人脑一样——重要的留下，过时的忘掉，而不是记流水账

### 2026-07-13: SKILL.md 只放运行时逻辑
- **Context**: 最初把安装指南、自成长规则全塞在 SKILL.md 里，每次会话加载大量无用内容
- **Decision**: SKILL.md 只保留会话启动/写入/结束的运行时流程；初始化放到 references/setup-guide.md，自成长规则放到 references/self-growth.md
- **Rationale**: 减少 context 浪费，按需加载

### 2026-07-13: 写入触发不用硬编码映射表
- **Context**: 最开始在 SKILL.md 里写了 8 行的"话题→文件"映射表
- **Decision**: 删掉映射表，依赖 AI 自己的理解力，根据已读的 INDEX.md 判断信息归属
- **Rationale**: AI 连信息该放哪都判断不了的话，这个系统就没意义了

### 2026-07-13: 动态 INDEX.md，不限制文件数量
- **Context**: 最初硬编码 6 个知识文件，用户想加新类别需要手动改 INDEX.md
- **Decision**: INDEX.md 改为 AI 自动维护的索引表，新增的 knowledge/*.md 文件会被自动识别和注册
- **Rationale**: 用户的记忆需求不可预测，不应预设分类

### 2026-07-13: 自成长规则（压缩 + 冲突处理）
- **Context**: 记忆积累后会膨胀，需要机制来保持精简
- **Decision**: 每个 H2 超过 30 行自动压缩旧条目到存档区；新旧矛盾标记 superseded
- **Rationale**: 记忆的质量比数量重要，渐进式压缩保证长期可用

### 2026-07-13: 渐进式读取策略
- **Context**: 知识文件会越来越大，不能每次都全文读取
- **Decision**: 先读 INDEX.md 判断相关度 → 打开文件只读 ## Summary → 需要细节才跳 H2
- **Rationale**: 用结构化文件格式（Summary + H2）支持 AI 按需跳读，类似搜索引擎的结果页

### 2026-07-14: 记忆合并规则（5 种合并方式）
- **Context**: 长期记忆需要更新，但之前的规则只说了"写入"，没说"如何更新已有内容"
- **Decision**: 定义 5 种合并方式：追加、更新（旧标 superseded）、纠正（直接修正+注释）、进度（状态标记）、归并（合并同类偏好）
- **Rationale**: 长期记忆不是一次写入就完了，需要持续更新维护。每种更新场景对应一种操作，不混用

### 2026-07-14: 五大缺陷修复
- **Context**: 整体审查后发现 5 个问题：存档区无限膨胀、INDEX.md 线性膨胀、认证失败无降级、多设备 merge conflict、同步时机靠自觉
- **Decision**:
  1. 存档区超 50 行触发二次压缩，更旧的条目压缩为一行摘要
  2. INDEX.md 超 30 行拆分为「常用文件（5条）」+「全部文件」两层
  3. git pull 失败时用本地缓存继续，不中断会话
  4. push 失败时 pull --rebase，conflict 时保留双方版本
  5. 写入时立即更新 INDEX.md，不依赖下次会话扫描
- **Rationale**: 记忆系统要能长期运行，必须在设计时就考虑膨胀和故障场景
