#!/usr/bin/env python3
"""
MemGit — 通用的 Git 记忆管理脚本。
任何人都可以用，Fork 仓库后只需运行一次 setup 即可。
"""
import os, sys, json, subprocess
from datetime import datetime
from pathlib import Path

# ── 路径配置 ──────────────────────────────────────────
MEMORIES_DIR = os.path.expanduser("~/.workbuddy/memories")
CONFIG_FILE = os.path.expanduser("~/.workbuddy/memgit-config.json")
SKILL_DIR = os.path.expanduser("~/.workbuddy/skills/memgit")


def _git(*args, cwd=MEMORIES_DIR):
    """Run git command, return stdout."""
    result = subprocess.run(
        ["git"] + list(args), cwd=cwd,
        capture_output=True, text=True,
    )
    if result.returncode != 0 and result.stderr:
        # 非致命错误才打印
        if "fatal" not in result.stderr.lower():
            print(f"[memgit] git warning: {result.stderr.strip()}", file=sys.stderr)
    return result.stdout.strip()


def _git_ok(*args, cwd=MEMORIES_DIR):
    """Run git command, return True if success."""
    result = subprocess.run(
        ["git"] + list(args), cwd=cwd,
        capture_output=True, text=True,
    )
    return result.returncode == 0


# ── 长期记忆模板（聚焦个人核心信息，不做短期会话记录）──
TEMPLATES = {
    "IDENTITY.md": """---
summary: "Who you are — basic info, background"
read_when:
  - Session start (always read first)
  - Before any user-specific decision
---

# IDENTITY

<!-- 你的基本信息，一次填写长期不变 -->

- **Name**:
- **Location**:
- **Background**:
- **Primary Language**: 中文

## Quick Facts

<!-- 3-10 条关于你自己的核心事实 -->

## Current Context

<!-- 你当前主要在做的事情（会随时间变化，记得更新） -->
""",

    "INDEX.md": """---
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

---

## 如何添加新的记忆分类

在 `knowledge/` 下新建一个 `.md` 文件即可。格式：

```markdown
---
summary: "一句话说明"
read_when:
  - 什么场景读
---

## Summary
3-5 行核心内容

## 你的分类
```

新建后 AI 会自动发现并注册到 INDEX.md。
""",

    "knowledge/principles.md": """---
summary: "Your values, principles, and decision-making rules"
read_when:
  - Making major decisions
  - Aligning output with your worldview
write_rules: |
  只记录用户明确表达的价值观
  不反推（行为可以出于各种原因）
  不超过30条活跃原则
---



# 价值观与原则

## Summary

<!-- 用 3-5 句话概括你的核心原则，让 AI 快速判断是否需要深入阅读 -->

## 人生信条

## 做事准则

## 审美与品味
""",

    "knowledge/habits.md": """---
summary: "How you work, communicate, and live"
read_when:
  - Adapting output to your style
  - Choosing tools or workflows
write_rules: |
  确认2次才写入习惯
  情绪模式只记重复出现的
  偶发行为不记
---



# 习惯与风格

## Summary

<!-- 用 3-5 句话概括你的关键习惯 -->

## 工作方式

<!-- 独立工作还是协作？喜欢深度专注还是快速切换？ -->

## 沟通偏好

<!-- 喜欢详细还是简洁？文字还是语音？直球还是委婉？ -->

## 编码 / 工具偏好

<!-- IDE、字体、快捷键、常用工具链等 -->

## 作息与精力

<!-- 什么时候状态最好？有什么固定的节奏？ -->
""",

    "knowledge/investments.md": """---
summary: "Investment philosophy, strategies, and portfolio"
read_when:
  - Discussing finance or investment
  - Reviewing past investment decisions
write_rules: |
  数字必须准确，模糊信息加标注
  不猜测用户数据
  不提供财务建议
---



# 投资理财

## Summary

<!-- 一句话概括投资风格，3-5 行关键条目 -->

## 投资理念

## 当前持仓 / 策略

## 重要交易记录

## 学习与反思
""",

    "knowledge/learning.md": """---
summary: "Learning plans, skills, books, courses"
read_when:
  - Discussing learning or skill development
  - Recommending books or courses
write_rules: |
  只记录用户声称掌握的技能
  会用≠掌握
  不给用户技能水平打分
---



# 学习成长

## Summary

<!-- 当前在学什么、主要技能方向 -->

## 正在学

## 已掌握的技能

## 想学的方向

## 读书 / 课程笔记
""",

    "knowledge/life.md": """---
summary: "Hobbies, health, relationships, lifestyle"
read_when:
  - Getting to know your personal life
  - Making lifestyle recommendations
write_rules: |
  兴趣和健康：确认2次才写
  重要关系：只记录用户主动提及的
  敏感信息放到文件底部
---



# 生活

## Summary

<!-- 用 3-5 行概括：兴趣方向、健康状况、重要关系等，帮 AI 判断是否需要深入 -->

## 兴趣爱好

<!-- 业余时间做什么 -->

## 健康习惯

<!-- 运动、饮食、睡眠 -->

## 重要关系

<!-- 家人、朋友、值得记住的人 -->

## 其他

<!-- 宠物、常去的地方、喜欢的餐厅等 -->
""",

    "knowledge/goals.md": """---
summary: "Life goals, yearly targets, milestones"
read_when:
  - Planning or strategizing
  - Celebrating achievements
write_rules: |
  不代替用户设目标
  状态变更时标注不覆盖
  用户确认后才标记完成
---



# 目标

## Summary

<!-- 当前阶段的核心目标 -->

## 长期愿景（3-5 年）

## 年度目标

## 已完成里程碑

---
"""
}


def _load_config():
    """Load config from JSON file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def _save_config(config):
    """Save config to JSON file."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def cmd_setup(repo_url, token=None):
    """First-time setup: clone repo, initialize if empty, push template."""
    config = _load_config()
    
    os.makedirs(MEMORIES_DIR, exist_ok=True)
    
    # Step 1: Check if the directory is already a git repo
    if os.path.exists(os.path.join(MEMORIES_DIR, ".git")):
        print("[memgit] memories directory already has a git repo.")
        print(f"[memgit] Current remote: {_git('remote', 'get-url', 'origin')}")
        answer = input("Override? (y/N): ").strip().lower()
        if answer != "y":
            print("[memgit] Setup cancelled.")
            return
        import shutil
        shutil.rmtree(os.path.join(MEMORIES_DIR, ".git"))
    
    # Step 2: Configure git identity
    _git("init")
    _git("config", "user.email", "memgit@local.dev")
    _git("config", "user.name", "MemGit")
    
    # Step 3: Set remote
    _git("remote", "add", "origin", repo_url)
    
    # Step 4: If token provided, configure credential helper
    if token:
        escaped_token = token.replace("\\", "\\\\").replace("\"", "\\\"")
        helper_cmd = f'!f() {{ echo "username={token.split("_")[0] if "_" in token else "oauth2"}"; echo "password={escaped_token}"; }}; f'
        _git("config", "--local", "credential.helper", helper_cmd)
        print("[memgit] Credential helper configured.")
    
    # Step 5: Try to fetch (check if remote has content)
    fetch_ok = _git_ok("fetch", "origin")
    
    if fetch_ok:
        remote_files = _git("ls-tree", "-r", "origin/main", "--name-only")
        if remote_files:
            # Remote has content — clone it
            print("[memgit] Remote repo has content, cloning...")
            _git("checkout", "-b", "main")
            _git("pull", "origin", "main", "--rebase")
            print("[memgit] Repo cloned successfully!")
            config["repo_url"] = repo_url
            _save_config(config)
            print(f"[memgit] Setup complete! Memory dir: {MEMORIES_DIR}")
            return
    
    # Step 6: Remote empty or unreachable — push template
    print("[memgit] Remote is empty (or unreachable). Pushing template structure...")
    
    for filepath, content in TEMPLATES.items():
        full_path = os.path.join(MEMORIES_DIR, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
    
    
    # Commit and push
    _git("checkout", "-b", "main")
    _git("add", "-A")
    _git("commit", "-m", "[MemGit] init: memory structure template")
    
    push_ok = _git_ok("push", "-u", "origin", "main")
    if push_ok:
        print("[memgit] Template pushed to remote successfully!")
    else:
        print("[memgit] Template committed locally, but push failed.")
        print("[memgit] You may need to configure authentication and push manually.")
        print(f"    cd {MEMORIES_DIR}")
        print(f"    git push -u origin main")
    
    config["repo_url"] = repo_url
    _save_config(config)
    print(f"[memgit] Setup complete! Memory dir: {MEMORIES_DIR}")
    print("[memgit] Next step: edit IDENTITY.md with your personal info.")


def cmd_start():
    """Session start: ensure setup, pull latest, print context."""
    config = _load_config()
    if not config.get("repo_url"):
        print("[memgit] NOT SETUP YET. Run: memgit.py setup <repo_url> [token]")
        sys.exit(1)
    
    _git("pull", "origin", "main", "--rebase")
    
    # List tracked files
    files = _git("ls-files").split("\n")
    context = {
        "branch": _git("branch", "--show-current"),
        "last_commit": _git("log", "-1", "--oneline", "--no-color"),
        "tracked_files": len(files),
        "files": [f for f in files if f],
    }
    
    print(json.dumps(context, ensure_ascii=False, indent=2))
    print(f"\n=== MemGit session started ===")
    print(f"Remote: {config['repo_url']}")
    print(f"Branch: {context['branch']}")
    print(f"Tracked files: {context['tracked_files']}")
    print(f"==============================")


def cmd_save(message="auto-save"):
    """Commit and push all changes."""
    changed = _git("status", "--porcelain")
    if not changed:
        print("[memgit] Nothing to save.")
        return
    
    _git("add", "-A")
    _git("commit", "-m", f"[MemGit] {message}")
    push_ok = _git_ok("push", "origin", "main")
    
    if push_ok:
        print(f"[memgit] Saved and pushed: {message}")
    else:
        print(f"[memgit] Committed locally, but push failed.")
        print(f"[memgit] Check your authentication and try: git push origin main")


def cmd_end(summary=""):
    """Session end: simple commit of any changes made during session."""
    cmd_save(f"session end")


def cmd_status():
    """Show current memory status."""
    changed = _git("status", "--porcelain")
    log = _git("log", "--oneline", "-5", "--no-color")
    
    print("=== MemGit Status ===")
    print(f"\nRecent commits:")
    print(log if log else "  (no commits yet)")
    print(f"\nUncommitted changes:")
    print(changed if changed else "  (clean)")
    print("[memgit] Tip: run 'save' to commit and push changes.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  memgit.py setup <repo_url> [token]    # First-time setup")
        print("  memgit.py start                        # Start session")
        print("  memgit.py save <message>               # Save changes")
        print("  memgit.py end <summary>                # End session")
        print("  memgit.py status                       # Check status")
        print("\nExamples:")
        print("  memgit.py setup https://github.com/yourname/your-memory.git")
        print("  memgit.py setup https://github.com/yourname/your-memory.git ghp_xxxxx")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "setup":
        if len(sys.argv) < 3:
            print("Usage: memgit.py setup <repo_url> [token]")
            sys.exit(1)
        token = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_setup(sys.argv[2], token)
    elif cmd == "start":
        cmd_start()
    elif cmd == "save":
        msg = sys.argv[2] if len(sys.argv) > 2 else "auto-save"
        cmd_save(msg)
    elif cmd == "end":
        summary = sys.argv[2] if len(sys.argv) > 2 else ""
        cmd_end(summary)
    elif cmd == "status":
        cmd_status()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
