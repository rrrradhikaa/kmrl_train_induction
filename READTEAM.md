# Team Guide for KMRL Train Induction Project (README_TEAM.md)

Welcome! This guide is for complete beginners. Follow it to collaborate cleanly with Git and GitHub.

---

## 1) Install and Set Up Git (first time only)

- Download & install Git: https://git-scm.com/downloads  
- Configure your identity in a terminal (PowerShell or VS Code terminal):

~~~bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
~~~

---

## 2) Clone the Repository (first time on your machine)

Replace <your-repo-url> with your repo’s HTTPS URL.

~~~bash
git clone https://github.com/<your-repo-url>.git
cd kmrl_train_induction
~~~

---

## 3) Daily Start: Sync with the Latest Code

Always start your workday by updating the integration branch.

~~~bash
git checkout dev
git pull origin dev
~~~

---

## 4) Create a Feature Branch (one branch per task)

Branch name format: feature/<task-name>  
Examples: feature/ui-dashboard, feature/backend-api, feature/data-pipeline

~~~bash
git checkout dev
git checkout -b feature/<task-name>
~~~

---

## 5) Make Your Changes

- Edit code, UI, data, or docs as per your assigned task.
- See what changed:

~~~bash
git status
~~~

---

## 6) Commit Your Work (Conventional Commits)

- Use this format for commit messages:
- type(scope): short description


**Types:** feat, fix, docs, style, refactor, test, chore  
**Scopes (examples):** ui, api, data, ml, readme, contributing

**Examples:**
- feat(ui): build train status dashboard
- fix(api): correct mileage balancing logic
- docs(readme): add setup instructions

Commands:

~~~bash
git add .
git commit -m "feat(ui): build train status dashboard"
~~~

For bigger changes, you can add a longer body:

~~~bash
git commit -m "feat(api): add scheduling endpoint" -m "Implements initial route and validation for train induction."
~~~

---

## 7) Push Your Branch to GitHub

~~~bash
git push origin feature/<task-name>
~~~

---

## 8) Open a Pull Request (PR)

1. Go to your repository on GitHub → **Pull requests** → **New pull request**.  
2. Set **Base** = dev, **Compare** = your feature branch.  
3. Fill in this template:

**Summary of changes**  
- What you built/changed.

**Related issue**  
- e.g., Closes #12

**Testing instructions**  
- Steps to run and verify.

4. Submit the PR for review.

---

## 9) Code Review & Updates

- A teammate (usually M1 as lead) reviews your PR.
- If updates are requested, make changes and push again:

~~~bash
git add .
git commit -m "fix(ui): adjust layout per review"
git push origin feature/<task-name>
~~~

- Once approved, the PR will be merged into **dev**.

---

## 10) After Merge: Sync Again

Keep your local copy up to date:

~~~bash
git checkout dev
git pull origin dev
~~~

---

## 11) Branch Rules (Important)

- **Never** push directly to **main** or **dev**.  
- **Always** create a feature branch from **dev**.  
- Merge via **Pull Requests** only (no direct merges).

Protected branches (set by M1 in GitHub Settings → Branches):
- main: production-ready, stable code only
- dev: integration branch for approved features

---

## 12) Using Issues & Project Board (Kanban)

- Create an **Issue** for each task (title, description, labels).
- Link Issues to the **Project** board and move them:
  - Backlog → Ready → In Progress → In Review → Done
- When your PR merges, move the card to **Done**.

**Example Issue (for M4):**
- Title: Implement mileage balancing rule  
- Description: Implement algorithm to distribute mileage evenly across fleet.  
- Labels: enhancement, algorithm, backend  
- Assignee: (assign once collaborators are added)

---

## 13) Common Git Commands (Cheat Sheet)

~~~bash
# See branches
git branch -a

# Switch branch
git checkout <branch-name>

# Create new feature branch from dev
git checkout dev
git checkout -b feature/<task-name>

# Stage and commit changes
git add .
git commit -m "feat(scope): message"

# Push to GitHub
git push origin feature/<task-name>

# Pull latest changes
git pull origin dev

# See status & recent commits
git status
git log --oneline --graph --decorate -n 15
~~~

---

## 14) FAQ / Troubleshooting

**Q: My file exists on GitHub main but not locally.**  
A: Switch to main and pull:
~~~bash
git checkout main
git pull origin main
~~~

**Q: I accidentally committed to the wrong branch.**  
A: Create a new branch from current state and push it, or cherry-pick/checkout the file into the correct branch. Ask M1 if unsure.

**Q: I can’t assign issues to teammates.**  
A: Only collaborators can be assigned. M1 must invite them under **Settings → Collaborators & teams**. After they accept, you can assign.

---

## 15) Team Norms

- Small, focused commits with clear messages.  
- One PR per feature/fix.  
- Keep branches short-lived; merge early & often.  
- Be kind in reviews; ask questions; document decisions.

---

By following this guide, our team keeps the repo clean, avoids conflicts, and ships faster. Welcome aboard!
