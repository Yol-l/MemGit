---
summary: "Memory index — AI auto-maintains this file"
read_when:
  - Session start (read right after IDENTITY.md)
---

# INDEX — 记忆导航图

> 此表格由 AI 自动维护。新增文件会自动出现在这里，删除文件会自动移除。

## 知识文件索引

| 文件 | Summary | 读取时机 |
|------|---------|---------|
| `knowledge/principles.md` | 价值观、做事原则、决策准则 | 涉及方向性判断时 |
| `knowledge/habits.md` | 工作习惯、沟通偏好、工具偏好 | 需要适配风格时 |
| `knowledge/investments.md` | 投资理念、策略、持仓 | 讨论投资话题时 |
| `knowledge/learning.md` | 学习计划、读书笔记、技能进展 | 涉及学习话题时 |
| `knowledge/life.md` | 兴趣爱好、健康习惯、重要关系 | 了解个人生活时 |
| `knowledge/goals.md` | 人生目标、年度目标、里程碑 | 讨论规划目标时 |
| `knowledge/projects-memgit.md` | MemGit 项目设计决策记录 | 继续迭代该技能时 |

---

## 如何添加新的记忆分类

在 `knowledge/` 下新建一个 `.md` 文件即可。例如：

```
knowledge/career.md    # 职业发展
knowledge/travel.md    # 旅行记录
knowledge/pets.md      # 养宠笔记
```

文件标准格式：

```markdown
---
summary: "一句话说明这文件记什么"
read_when:
  - 什么场景需要读
---

## Summary
3-5 行核心内容

## 你的分类
```

新建后 AI 在下一次会话启动时会自动发现并注册到 INDEX.md。
