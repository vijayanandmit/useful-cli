There are 6 levels of making Claude Code run autonomously, and most people are stuck on Level 1.

Level 1: Kill the permission prompts. Run claude --dangerously-skip-permissions. One flag. Now it stops asking “Can I edit this file?” every 30 seconds while you’re checking Slack.

Level 2: Context window management. Claude Code now supports 1M tokens. Use /clear between tasks. Run /compact at 60% usage instead of waiting for auto-compaction to fire at 90% when the model is already forgetting your instructions.

Level 3: Subagents. The reason it stops at 15 minutes: everything runs in one context window. Subagents run in separate contexts. Build a looping todo command, each task executes in its own window. Builds, tests, and git operations never touch the main conversation. 2+ hours autonomous with zero intervention.

Level 4: Ralph Wiggum loop. Official Anthropic plugin. Claude works, tries to exit, a Stop hook blocks the exit, re-feeds the same prompt. Each iteration sees modified files and git history from previous runs. One developer ran 27 hours straight, 84 tasks completed. Geoffrey Huntley ran one for three months and built a programming language with a working LLVM compiler.

Level 5: Karpathy’s AutoResearch. On March 7, Karpathy pushed a 630-line script to GitHub and went to sleep. Woke up to 100+ ML experiments completed overnight. 25K stars in five days. The difference from Ralph: structured eval loops. Define a metric, run, measure, analyze failures, improve, repeat. One Claude Code port took model accuracy from 0.44 to 0.78 R² across 22 autonomous experiments.

Level 6: VPS + OpenClaw for 24/7. Your laptop lid closing kills everything. Run Claude Code on a VPS inside tmux. Detach, close your laptop, come back tomorrow to a finished diff. OpenClaw (247K GitHub stars) takes it further: a persistent gateway connecting LLMs to your real tools, running 24/7 across messaging, email, git, and calendars. Jensen Huang at GTC called it “probably the most important release of software ever.”

Here’s guides for each level:

Level 1: https://youtu.be/4nthc76rSl8?si=Y-5WJihaCu5Gzj6T

Level 2: https://youtu.be/59gy_24KIVE?si=wby921k8IxkOCoBD

Level 3: https://www.news.aakashg.com/p/pm-os

Level 4: https://www.news.aakashg.com/p/ralph-wiggum

Level 5: https://www.news.aakashg.com/p/autoresearch-guide-for-pms

Level 6: https://www.news.aakashg.com/p/naman-pandey2-podcast

The unlock at every level is the same: give Claude a way to verify its own work.