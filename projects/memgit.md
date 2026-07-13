---
summary: "MemGit — Git 驱动的 AI 长期记忆系统"
status: active
tech_stack: [Python, Markdown, Git]
repo: "https://github.com/Yol-l/MemGit"
docs: "https://github.com/Yol-l/MemGit (文档在仓库 README 和 skill 文件中)"
created: 2026-07-13
write_rules: |
  只记录项目级决策和经验教训
  不记录代码细节（代码在仓库里）
  里程碑完成时更新 status
  项目结束时移入 archive/
---

# MemGit 项目

## Summary

Git 驱动的 AI 长期记忆系统，任何人 fork 仓库 + 运行 setup 即可使用。核心目标：记长期有用的事，不做短期会话记录。

## 架构决策

### 2026-07-13: 记忆结构只存长期信息
- **Decision**: 去掉 sessions/ 目录，只保留 IDENTITY.md + knowledge/ 下的长期知识文件
- **Rationale**: 重要的留下，过时的忘掉，不记流水账

### 2026-07-13: SKILL.md 只放运行时逻辑
- **Decision**: 安装指南、自成长规则等放到按需加载的文件中
- **Rationale**: 减少 context 浪费

### 2026-07-13: 写入触发不用硬编码映射表
- **Decision**: 依赖 AI 理解力判断信息归属，不用对照表
- **Rationale**: AI 连信息该放哪都判断不了的话，系统就没意义了

### 2026-07-13: 动态 INDEX.md，不限制文件数量
- **Decision**: INDEX.md 改为 AI 自动维护的索引表
- **Rationale**: 用户的记忆需求不可预测，不应预设分类

### 2026-07-13: 自成长规则（压缩 + 冲突处理）
- **Decision**: H2 超 30 行自动压缩；新旧矛盾标记 superseded
- **Rationale**: 记忆的质量比数量重要

### 2026-07-13: 渐进式读取策略
- **Decision**: INDEX 判断相关度 → 只读 Summary → 需要细节才跳 H2
- **Rationale**: 结构化文件格式支持 AI 按需跳读

### 2026-07-14: 记忆合并规则（5 种合并方式）
- **Decision**: 追加、更新、纠正、进度、归并
- **Rationale**: 每种更新场景对应一种操作，不混用

### 2026-07-14: 五大缺陷修复
- **Decision**: 存档二次压缩 / INDEX 分层 / 认证降级 / 冲突保留双方 / 即时同步 INDEX

### 2026-07-14: 约束规则补全
- **Decision**: 文件创建门槛 / superseded 即时归档 / 条目加日期 / 删除规则 / 通知汇总

### 2026-07-14: 策略目录独立
- **Decision**: 策略文件从 skill 迁移到记忆仓库的 strategies/ 目录
- **Rationale**: AI 查询方便，用户可自行修改，可分享给他人

### 2026-07-14: 项目记忆独立目录
- **Decision**: projects/ 目录与 knowledge/ 分离，项目文档不放入记忆仓库
- **Rationale**: 项目文档量大，属于项目仓库，不属于记忆仓库

## 经验教训

- (2026-07-14) SKILL.md 不能膨胀，策略要外置到按需加载的文件
- (2026-07-14) 不能把 AI 自己的设计原则写到用户的价值观文件里
- (2026-07-14) 通知用户时不能用文件名和内部规则，要自然语言

## 当前状态

- 进行中：策略完善、多用户测试
- 下一步：实际使用验证
