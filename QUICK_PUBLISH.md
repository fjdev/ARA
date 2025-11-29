# Quick Reference: Publishing ARA to GitHub

## 🚀 Fast Track (5 Commands)

```bash
# 1. Navigate to ARA directory
cd /Users/floriandevries/Repos/Tools/ara

# 2. Initialize git and commit
git init
git add .
git commit -m "Initial release: ARA v1.0.0"
git branch -M main

# 3. Create repository on GitHub (via web)
# → Go to https://github.com/new
# → Name: ara
# → Visibility: Public
# → DO NOT initialize with README/License/.gitignore
# → Click "Create repository"

# 4. Connect and push
git remote add origin https://github.com/fjdev/ara.git
git push -u origin main

# 5. Create version tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

**Done!** Now create a GitHub Release via the web UI.

---

## 📋 Essential Settings After Publishing

### Security (CRITICAL)
1. **Enable 2FA** on your GitHub account
2. Settings → Security → Enable:
   - ✅ Dependabot alerts
   - ✅ Secret scanning
   - ✅ Push protection

### Repository Setup
1. **Add topics**: azure, rbac, python, cli-tool, security-audit
2. **Add description**: "Professional Azure role assignment exporter"
3. **Set website**: (if you have docs site)

### Release Creation
1. Go to Releases → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - Azure Role Assignment Exporter`
4. Description: Copy from `RELEASE_CHECKLIST.md`
5. Click "Publish release"

---

## 🔐 Authentication Options

### Option A: HTTPS with Personal Access Token (PAT)
```bash
# Create PAT: GitHub Settings → Developer settings → Personal access tokens
# Scopes: repo (full control)
# Use PAT as password when pushing
```

### Option B: SSH (Recommended)
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
# Copy public key:
cat ~/.ssh/id_ed25519.pub

# Change remote to SSH
git remote set-url origin git@github.com:fjdev/ara.git
```

---

## ✅ Pre-Push Verification

```bash
# Verify tests pass
python3 tests/run_tests.py

# Test the tool works
./ara --scope test-mg

# Check for sensitive data
git diff --cached | grep -i "token\|password\|secret"

# Verify .gitignore excludes results
git status | grep results

# Ready to push!
```

---

## 🎯 Common Commands

```bash
# Check repository status
git status

# View commit history
git log --oneline

# Create a new release
git tag -a v1.1.0 -m "Release v1.1.0: Added feature X"
git push origin v1.1.0

# Update remote if repo renamed
git remote set-url origin https://github.com/fjdev/new-name.git

# Undo last commit (if not pushed)
git reset --soft HEAD~1

# View remote URL
git remote -v
```

---

## 📞 Quick Help

- **Full guide**: See `GITHUB_PUBLISHING_GUIDE.md`
- **TODO items**: See `TODO.md`
- **Release checklist**: See `RELEASE_CHECKLIST.md`

---

**Estimated time to publish**: 15 minutes
**Skill level required**: Basic git/GitHub knowledge
**Risk level**: Low (public repo, open source)

🚀 **Let's publish!**
