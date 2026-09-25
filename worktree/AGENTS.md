goal: learn git worktree
create files or recommend git workflow to familiarize with worktree
user is aware of git commands, comfortable with git cli commands like add, commit, push
safety-first policy:
- prioritize security and correctness over speed
- before suggesting or running a git/worktree command, verify what it changes and prefer the smallest reversible step
- call out blast radius for branch, worktree, and filesystem operations when there is any risk of affecting existing work
- prefer isolated worktrees, non-destructive git commands, and explicit status checks before cleanup operations
