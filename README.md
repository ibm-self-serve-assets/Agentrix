
# Git, GitOps, and DevOps Best Practices

## 1. Branching Strategy
Use a structured branching model like **Git Flow**, **GitHub Flow**, or **Trunk-Based Development**.  

### Git Flow (Recommended for Large Teams)
```bash
# Create a feature branch
git checkout -b feature/awesome-feature

# Work, commit, and push
git commit -m "feat: Implement awesome feature"
git push origin feature/awesome-feature

# Merge via Pull Request
```
 ✅ `main` → **Stable production branch. Only tested and approved changes should be merged.**  
 ✅ `develop` → **Integration branch for testing new features before merging into main.**  
 ✅ `feature/*` → **Branch for developing new features. Merged into develop when complete.**  
 ✅ `hotfix/*` → **Branch for critical bug fixes in production. Merged into both main and develop.**  

### Commit Message Conventions
Follow the **Conventional Commits** format for clarity and consistency:

**feat:** Introduces a new feature  
  ```bash
  git commit -m "feat(auth): Add JWT-based authentication"
  ```
**fix:** Fixes a bug  
  ```bash
  git commit -m "fix(api): Resolve timeout issue"
  ```
**docs:** Documentation updates  
  ```bash
  git commit -m "docs(README): Update API documentation"
  ```
**refactor:** Code changes that do not add features or fix bugs  
  ```bash
  git commit -m "refactor(database): Optimize query execution"
  ```
**chore:** Maintenance tasks (e.g., updating dependencies)  
  ```bash
  git commit -m "chore(deps): Update dependencies"
  ```

## 2. Commit & PR Best Practices
### Write Meaningful Commit Messages
```bash
git commit -m "feat(auth): Add JWT-based authentication"
git commit -m "fix(api): Resolve timeout issue"
git commit -m "docs(README): Update API documentation"
```
✅ Use prefixes: **feat, fix, docs, refactor, chore**  
✅ Keep commits **atomic** and **small**  

### Pull Request Checklist
PRs should have **descriptive titles**  
Link to relevant **JIRA/Ticket**  
Require **code reviews & approvals**  

## 3. GitOps Best Practices
**GitOps Workflow:** Infrastructure is stored in **Git and auto-applied** using ArgoCD or FluxCD.  

### Example: Kubernetes GitOps Workflow with ArgoCD
**Store Kubernetes manifests in Git:**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: my-app
   spec:
     replicas: 3
     template:
       spec:
         containers:
name: app
             image: my-app:latest
   ```
**ArgoCD automatically syncs it with the cluster.**  
   ```bash
   argocd app create my-app      --repo https://github.com/user/repo.git      --path kubernetes/manifests      --dest-server https://kubernetes.default.svc
   ```
✅ **Version-controlled deployments**  
✅ **Automated rollbacks**  

## 4. Security & Compliance
### Enable Branch Protection Rules
**Go to**: GitHub → Settings → Branches  
**Enable:**  
   ✅ Require PR reviews before merging  
   ✅ Restrict who can push to `main`  
   ✅ Disallow force pushes  

### Prevent Secrets in Git
Scan for secrets before pushing:
```bash
trufflehog --regex --entropy=True .  
```
✅ Use **environment variables** instead of hardcoded secrets  
✅ Store sensitive data in **Vaults (AWS Secrets Manager, HashiCorp Vault, etc.)**  

## 5. CI/CD & Automation
Use **GitHub Actions, GitLab CI, or Jenkins** for automated testing & deployment.  

### Example: GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on: push

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
name: Checkout code
        uses: actions/checkout@v4

name: Install dependencies
        run: npm install

name: Run tests
        run: npm test

name: Deploy
        run: echo "Deploying to production..."
```
✅ **Automates tests & deployment**  
✅ **Prevents broken code from reaching production**  

## 6. Performance Optimization
### Shallow Clone for Large Repos
```bash
git clone --depth=1 https://github.com/user/repo.git
```
✅ Faster cloning  

### Optimize `.gitignore`
```bash
# Ignore dependencies
node_modules/
vendor/

# Ignore logs
*.log
```
✅ Prevents bloated repositories  

## 7. Backup & Disaster Recovery
### Mirror a Repo for Backup
```bash
git clone --mirror https://github.com/user/repo.git
git push --mirror https://gitlab.com/user/repo-backup.git
```
✅ Ensures offsite backups  

---

## License

This project is licensed under different licenses based on the role of the user.

### Open Source License
Allows users to freely use, modify, and distribute the software. Contributions are welcomed, but users must include the original copyright and permission notice. An example is the **MIT License**.

### Limited License
Provides restrictions on modification, redistribution, and commercial use. Users may need to purchase a commercial license for business or commercial use.

### Free License
Allows free usage of the software for personal use but restricts commercial use or redistribution. It's often used for individual or non-business applications.

### Open Source Software (OSS)
This software is openly available for users to contribute to, improve, and share with the community. The source code is publicly accessible, and anyone can use or modify it based on the license terms.

### License Breakdown
Here's a breakdown of what each license type means:

**Open Source License**: This means anyone can freely use, modify, and distribute the software, but they must include the original copyright and permission notice. It encourages contributions from the community and typically includes licenses like MIT or Apache.

**Limited License**: This restricts users from modifying, redistributing, or using the software for commercial purposes unless they purchase a commercial license. It’s often used for software that has proprietary components.

**Free License**: This allows users to use the software for free but limits its use to personal or non-commercial purposes only. Commercial usage is not permitted without further licensing agreements.

**Open Source Software (OSS)**: This refers to software that is made publicly available with its source code, allowing anyone to contribute to, modify, or redistribute it. The primary goal is community involvement and collaboration.

---