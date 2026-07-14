---
name: memgit
description: >
  CRITICAL: Load at EVERY session start. This skill manages the user's complete long-term memory
  and MUST be consulted during EVERY conversation turn. Knows the user's identity, events,
  projects, preferences, habits, and emotional patterns. Interjects with relevant memories
  when the conversation touches known topics. Loads self-check before any memory write.
agent_created: true
---

# MemGit — 长期记忆系统

## 记忆文件

```
~/.workbuddy/memories/
├── IDENTITY.md                     # 基本信息（永远先读）
├── INDEX.md                        # 知识索引（AI 自动维护）
├── knowledge/                      # 个人记忆
│   ├── principles.md               # 价值观、原则
│   ├── habits.md                   # 做事习惯
│   ├── investments.md              # 投资理财
│   ├── learning.md                 # 学习成长
│   ├── life.md                     # 生活
│   └── goals.md                    # 目标
├── projects/                       # 项目记忆
│   ├── INDEX.md                    # 项目索引
│   ├── *.md                        # 活跃项目（一个项目一个文件）
│   └── archive/                    # 已归档项目
└── strategies/                     # 记忆维护策略（可共享）
    ├── INDEX.md
    ├── self-growth.md
    ├── proactive-usage.md
    └── emotional-awareness.md
```

**项目记忆 vs 项目文档**：
- 记忆仓库只存**项目记忆**（决策、状态、经验教训）——短
- 项目文档（需求、设计、API 文档）存在**项目自己的仓库**里——大
- 每个项目文件的 frontmatter 中 `docs` 字段指向项目文档位置

每个知识文件标准格式：frontmatter（summary + read_when + write_rules）→ `## Summary` → H2 分节。

## 会话启动（自动执行）

1. 读 config → 获取仓库地址
2. `git pull`（失败则用本地缓存，不中断）
3. **读 `MEMORY-ARCHITECTURE.md`** → 理解整个记忆系统的结构（一次性，替代过去读 4 个文件）
4. **读 `strategies/system-control.md`** → 硬边界、阈值、自检规则
5. 读 `IDENTITY.md`（全文）
6. **扫 `knowledge/events.md`** → 最近在忙什么
7. **自检** → 按 system-control.md 逐项检查，每次修复 ≤ 3 个问题
8. 读 INDEX.md → 扫 knowledge/ → 同步索引
9. 扫 `projects/INDEX.md` → 涉及项目时才读
10. 渐进式读 knowledge/：INDEX 判断相关度 → Summary → H2
11. 一句话启动摘要（≤30 字）："记忆已加载。上次在做 MemGit 闭环，马来西亚计划还在，新项目的事还没开始。"
（从 events.md + git log 提取上次会话的最后要点）

## 会话中：写入

**归属判断**：
- 信息能归入已有文件 → 写对应 H2
- 能归入但现有 H2 都不匹配 → 在已有文件中**新建 H2**
- **确实无法归入**任何已有文件 → 直接新建 `knowledge/主题.md`

**事件关联同步**：当 events.md 新增一条带 `→ xxx.md` 引用的事件时，同步在被引用文件中追加对应内容。例如 `(07-14 – 至今) [学习] 考虑读 MBA → learning.md` → learning.md 的对应 H2 也追加"考虑读 MBA"。

**每个文件在 frontmatter 中自带 `write_rules`** → 打开文件时先读它，按规则写入，不允许自由发挥。

### 新建文件的规则

新建文件必须同时满足：
1. **无法归入**任何已有文件的任何已有 H2（先试新建 H2）
2. 内容属于**长期有价值**的信息（6 个月后仍然有用）

新建时强制使用以下模板：

```markdown
---
summary: "一句话说明"
read_when:
  - 什么场景读
write_rules: |
  该文件特定的写入约束
---

## Summary

<!-- 3-5 行核心内容 -->

## 你的 H2 分类
```

**命名规则**：小写英文 + 连字符。放在 `knowledge/` 目录下。

**禁止创建**：
- ❌ 单次对话中创建超过 1 个新文件（同一个对话的多个独立话题，优先分 H2）
- ❌ 只为了一句话就建一个文件（那条信息先写在已有文件里）
- ❌ 文件名用中文、空格、特殊字符
- ❌ 在 `knowledge/` 或 `projects/` 之外创建记忆文件
- ❌ 创建后不在 INDEX.md 中注册
- ❌ 把项目文档内容写入记忆仓库（文档放项目自己的仓库）

**项目文件特殊规则**：
- 项目记忆放在 `projects/` 目录，不放 `knowledge/`
- 每个项目一个文件，frontmatter 必须有 `status` 和 `docs` 字段
- 项目结束时改 `status: archived` 并移入 `projects/archive/`
- 项目文档（需求、设计、API 等）不写入记忆仓库，只在 frontmatter 的 `docs` 字段记录位置

**写入约束**：

| ✅ 能改 | ❌ 不能改 |
|--------|----------|
| 追加条目 / 更新 Summary | 删用户记录（除非用户要求） |
| 标记 superseded / 按时间分组 | 改 H2 分类结构 |
| 压缩过时内容 | 写错文件 / 写一次性信息 |
| 用户要求时删除 | 静默删除 |

每条条目首次写入标注日期和信心水平：`explicit`（用户亲口说）、`inferred`（AI 推断）、`stale`（1 年未确认）、`uncertain`（用户说"可能"）。引用推断型记忆时语气轻一些。

**explicit vs inferred 的判定**：用户直接陈述偏好（"我喜欢X""我决定用X"）= explicit。用户使用某技术但不表态（"帮我写X代码"）= inferred，需确认 2 次。

### 记忆自愈（核心防幻觉机制）

记忆不是"事实"，是"待验证的断言"。AI 在后续会话中通过两种方式自然修复：

**主动修复**（AI 引用记忆时用户否认）：
```
引用记忆 → 用户否认 → 立即修正该条目 → 同时检视同一次会话中写的其他条目→ 一并降级
```

**被动检测**（系统反思触发的主动确认，每 10 轮 1 次）：
```
挑 1 条 confidence 最低的 inferred 或 stale 条目
自然地确认："我记着你以前 X，现在还是吗？"
用户确认 → 提升为 explicit
用户否认 → 修正
用户不置可否 → 不理，下次换一条确认
```

**不需要 source 原文**。核心是修复闭环：错了一条 → 修正它 → 降低同源其他记忆的置信度 → 不再引用错误的记忆直到用户重新确认。这才是自愈。

### 禁止存储

以下内容**绝对不能**写入任何记忆文件：
- 密码、API key、token、密钥
- 身份证号、银行卡号、地址等个人敏感信息
- 用户明确说"不要记"的内容
- AI 自己生成的无关内容（如"好的，已记住"这类回复）

如果用户主动提供了敏感信息，告知用户"这类信息不建议存入记忆"并跳过写入。

### 重大变更强制追问

以下变更影响多个文件，AI 不能自己推断，必须追问后再写入：
- 职业变化（"换工作了"）→ 追问：技术栈变了吗？新工作主要做什么？
- 技术栈迁移（"以后用 Java 了"）→ 追问：原来的 Go 还维护吗？
- 关系变化（"分手了"）→ 不开玩笑，先接住
- 重大目标变更（"不考研了"）→ 追问：为什么？换什么方向？
- **偏好反转**（新 explicit 与已有 explicit 矛盾）→ 追问："你之前说 X，现在说 Y，是改主意了还是之前说得不太准确？"

追问后根据回答写入，并在写入时检查所有引用该信息的文件是否需要同步更新。

### 写错回滚

如果写入了错误信息：
- 用户指出后立即修正
- 修正记录留注释 `<!-- 2026-07-14 修正：原因 -->`
- git 历史自然保留旧版本，不需要手动删 commit

### 通知：不用文件名，不解释规则，自然一句话带过。追问再展开。

### 系统反思（每轮对话后静默，每 5 轮汇总一次）

不是检查"这轮写错了没"。是检查**系统本身是否健康**。

```
1. 架构适配
   → events.md 有多少活跃事件？有没有超过 6 个月仍活跃的？该归档了吗？
   → knowledge/ 各文件的读写比例如何？有文件长期只读不写？有文件写了从来不读？
   → 新增的 H2 是否集中在某个文件？该文件需要分裂吗？

2. 记忆准确性
   → 是否有 explicit 条目超过 1 年未重新确认？该标 stale 了吗？
   → inferred 条目占比是否过高（>30%）？说明推断太多了，该收敛。
   → 同一 H2 下是否有明显矛盾的条目？该标记 needs-review 了吗？

3. 规则有效性
   → 过去 5 轮里有触犯硬边界吗？是因为规则不合理还是 AI 执行偏差？
   → 膨胀阈值触发过吗？阈值设置得对不对？
   → 自检发现的修复项是否在减少？（减少=系统变健康，没减少=规则不够严）

4. 结构演化
   → 最近 5 轮有没有反复出现"不确定该放哪"的内容？该新建类别吗？
   → 某个 knowledge/ 文件是否已经承载了过多不同类型的 H2？该拆吗？
   → 某个 H2 下超过 5 条同主题内容？该提议独立文件吗？
   → events.md 和 projects/ 之间的引用是否完整？有事件没对应项目文件的吗？
```

**执行频率**：每 5 轮做一次（不是每轮）。大多数会话不做。结果记录到 `system-signals.md`。发现问题时：

- 小问题 → 静默记录，不打断用户
- 中等问题 → 积累到 3 次后提一个简洁建议
- 重大问题 → 直接告诉用户："你的 xxx 结构可能需要调整，原因：yyy"

### 主动使用记忆

需要时加载 `~/.workbuddy/memories/strategies/proactive-usage.md`：
- 话题关联 / 目标回访 / 偏好适配 / 风格自适应 / 进展跟踪

## 情绪感知

需要时加载 `~/.workbuddy/memories/strategies/emotional-awareness.md`：
- 按情绪调整回应 / 该夸就夸 / 该说就说

## 自成长与合并

需要时加载 `~/.workbuddy/memories/strategies/self-growth.md`：
- 5 种合并 / H2 压缩 30 行 / 存档二次压缩 50 行 / 索引分层 30 行 / 分裂 150 行

> 策略文件在记忆仓库的 `strategies/` 目录下，不在 skill 里。用户可以直接编辑策略来调整 AI 行为，也可以从别人的仓库获取策略。

## 会话结束

**提交并推送**：
```bash
cd ~/.workbuddy/memories && git add -A && git commit -m "[MemGit] update" && git push
```
push 失败 → `git pull --rebase` → 仍有 conflict 则保留双方版本加标记。

**离线场景**：无网络时 push 失败是正常的。本地 commit 会累积，下次有网络时自动同步。不要因为 push 失败就停止写入。但若多设备同时离线使用，回来后可能有冲突——此时保留双方版本。

commit message 必须包含审计摘要，格式：`变更 X 文件 | 违规 0 | 压缩 0 | 新建 0`

**会话审计**（嵌入回复中，自然带过）：
> 本次变更：learning.md +1 条。无违规，无压缩触发。

**下次会话验证**：启动时执行 `git diff HEAD~1 --stat`，若变更文件数与上条 commit 的审计摘要不一致 → 告知用户。
