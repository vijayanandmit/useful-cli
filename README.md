## 🔄 Syncing Your Fork with the Original Repository

To bring the latest changes from the original repository (also called the "upstream") into your fork, follow these steps:

### 1. Add the Original Repository as Upstream

If you haven’t already, add the original repository as a remote called `upstream`:

```bash
git remote add upstream <original-repo-URL>
```

### 2. Fetch the Latest Changes from Upstream

Retrieve the latest commits from the original repository:

```bash
git fetch upstream
```

### 3. Merge Upstream Changes into Your Local Branch

Switch to your local `main` branch (or whichever branch you want to sync):

```bash
git checkout main
```

Merge the changes from `upstream/main` into your local branch:

```bash
git merge upstream/main
```

> ⚠️ If there are merge conflicts, Git will prompt you to resolve them manually. Use your code editor to fix the conflicts, then stage and commit the resolved files.

### 4. Push Changes to Your GitHub Fork

Finally, push the updated branch back to your GitHub fork:

```bash
git push
```

---

Following these steps ensures your fork stays up-to-date with the original repository.

