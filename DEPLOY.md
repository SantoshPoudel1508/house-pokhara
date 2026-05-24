# GitHub Pages Deployment Guide

## Method 1 — Upload via GitHub Website (Easiest, No Terminal Needed)

### Step 1: Create a GitHub Account
1. Go to **github.com**
2. Click **Sign up**
3. Enter your email, create a password, choose a username
4. Verify your email

### Step 2: Create a New Repository
1. After logging in, click the **+** button (top right) → **New repository**
2. Repository name: `house-pokhara`  ← type this exactly
3. Description: `House building guide for our Pokhara home`
4. Select: **Public**
5. Check ✅ **Add a README file**
6. Click **Create repository**

### Step 3: Upload All Files
1. You will see your new repository page
2. Click **Add file** → **Upload files**
3. Drag the entire `house-pokhara` folder contents into the upload box
   - Upload all .html files
   - Upload the `css` folder (with style.css inside)
   - Upload the `js` folder (with app.js inside)
4. In the **Commit changes** box at the bottom, write: `Add complete house guide website`
5. Click **Commit changes**

### Step 4: Enable GitHub Pages
1. Go to your repository page
2. Click **Settings** (top menu, gear icon)
3. In the left sidebar, click **Pages**
4. Under **Source**, select **Deploy from a branch**
5. Under **Branch**, select **main** and select **/ (root)**
6. Click **Save**

### Step 5: Wait and Get Your Link
1. Wait 2–3 minutes
2. Refresh the **Pages** settings page
3. You will see: **"Your site is live at https://YOUR-USERNAME.github.io/house-pokhara/"**
4. Click that link — your website is live!

---

## Method 2 — Using Git (Terminal / Command Line)

### Prerequisites
- Install Git from git-scm.com
- Have a GitHub account (same as above)

### Commands
```bash
# 1. Navigate to your project folder
cd /path/to/house-pokhara

# 2. Initialize Git
git init

# 3. Add all files
git add .

# 4. Create first commit
git commit -m "Initial commit: Complete house guide website"

# 5. Set branch name
git branch -M main

# 6. Add GitHub as remote (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/house-pokhara.git

# 7. Push to GitHub
git push -u origin main
```

Then follow Step 4 above to enable GitHub Pages.

---

## Updating the Site Later

### Via Website:
1. Go to your repository on github.com
2. Click on the file you want to change
3. Click the ✏️ pencil icon (Edit)
4. Make your changes
5. Click **Commit changes**
6. Site updates automatically in 1–2 minutes

### Via Git:
```bash
git add .
git commit -m "Update: description of your change"
git push
```

---

## Custom Domain (Optional)
If you have a domain name (e.g., ourhouse.com):
1. In repository Settings → Pages → Custom domain
2. Enter your domain name
3. Follow GitHub's DNS setup instructions

---

## Sharing the Link
Your site will be at: **https://YOUR-USERNAME.github.io/house-pokhara/**

Share this link with your father, family members, or contractors.
It works on any device — phone, tablet, computer — without installing anything.
