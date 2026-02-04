# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository is a personal collection of:
- **LeetCode solutions** (Python) in the `leetcode/` directory
- **Command reference notes** (.txt files) for Git, Linux, SSH, VMware ESX
- **Shell scripts** for automated review/validation
- **Git worktree learning materials** in the `worktree/` directory

## Development Commands

### Python (LeetCode Solutions)

Run a single Python file:
```bash
python3 leetcode/kScores.py
```

Compile all Python files to check for syntax errors:
```bash
python3 -m compileall -q leetcode
```

### Review Script

Run the automated review script (checks git status, Python compilation):
```bash
./scripts/review.sh
```

This generates timestamped reports in `review-reports/` with:
- Current git branch and HEAD
- Git working tree status
- Python compilation results for `leetcode/`

Install as a launchd service (macOS):
```bash
./scripts/install-review-launchd.sh
```

Uninstall the service:
```bash
./scripts/uninstall-review-launchd.sh
```

## Architecture & Structure

### LeetCode Solutions (`leetcode/`)

Python solutions follow a consistent pattern:
- Each file is a standalone solution to a single LeetCode problem
- Files contain a `Solution` class with the main method
- Comprehensive docstrings explain the problem, approach, time/space complexity
- Optional `if __name__ == "__main__"` blocks for testing (may be commented out)
- Example structure: see `kScores.py` (simple sliding window) or `MinPairRemoval.py` (complex heap + linked-list simulation)

**Code style:**
- Type hints using `from typing import List, Tuple`
- Detailed inline comments for complex algorithms
- Docstrings include problem statement, approach description, and complexity analysis
- Sometimes include a `_naive_*` reference implementation for validation

### Reference Text Files

Plain text files (`.txt`) contain command snippets and notes:
- `git-github.txt`: GitHub CLI commands, repo creation
- `linux-top.txt`: System monitoring tools (iotop, htop, nvtop alternatives)
- `ssh-tunnel.txt`: SSH port forwarding examples
- `vmware-esx.txt`: VMware ESX commands
- `linux-network.txt`, `linux-dhcp-server.txt`: Linux networking

These are personal reference materials, not executable code.

### Scripts (`scripts/`)

Shell scripts for automation:
- `review.sh`: Main review script that generates reports
- `install-review-launchd.sh`, `uninstall-review-launchd.sh`: macOS launchd service management

Scripts use `set -euo pipefail` for safety and repo-relative paths.

### Worktree Learning (`worktree/`)

Materials for learning git worktree functionality:
- `AGENTS.md`: Instructions for AI agents (Codex skills system)
- `WORKTREE_WALKTHROUGH.md`: Likely contains git worktree tutorial content

## Git Workflow

Default branch: `master`

Standard workflow:
```bash
git add .
git commit -m "Description"

git push
```

Creating GitHub repos:
```bash
gh repo create --public <repo-name>
git remote add origin https://github.com/vijayanandmit/<repo-name>.git
git push --set-upstream origin master
```
