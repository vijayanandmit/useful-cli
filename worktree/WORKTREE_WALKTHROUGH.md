# Git worktree walkthrough (hands-on)

This repo already has a second worktree created for you:

- Main worktree (your current one): `/Users/vijay/git/useful-cli`
- Demo worktree: `/tmp/useful-cli-wt-demo` on branch `wt-demo`

## 1) See what exists

From anywhere inside the repo:

```sh
git worktree list
git branch --all --verbose
```

## 2) Make a change in the demo worktree (isolated checkout)

```sh
cd /tmp/useful-cli-wt-demo
git status
echo "demo: $(date)" >> WT_DEMO.txt
git add WT_DEMO.txt
git commit -m "demo: change from worktree"
```

Notice: your main worktree still stays on `master` and won’t suddenly change files.

## 3) Look at the same repo from the main worktree

```sh
cd /Users/vijay/git/useful-cli
git status
git log --oneline --decorate -5
```

The commit exists (same repo), but it’s on branch `wt-demo`.

## 4) Merge back (one common workflow)

```sh
cd /Users/vijay/git/useful-cli
git switch master
git merge --no-ff wt-demo
```

## 5) Remove the worktree when done

```sh
git worktree remove /tmp/useful-cli-wt-demo
git branch -d wt-demo
git worktree prune
```

If you forget to remove it and the folder disappears, `git worktree prune` cleans stale metadata.

## 6) Pattern to practice

Create multiple concurrent worktrees for parallel tasks:

```sh
git worktree add -b wt/feature-a /tmp/useful-cli-wt-feature-a
git worktree add -b wt/feature-b /tmp/useful-cli-wt-feature-b
```

Then work in each directory independently, commit there, merge from your main worktree.

