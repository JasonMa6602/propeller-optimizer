# Setup Instructions for Pushing to GitHub

## Your Project Information
- **GitHub Username**: JasonMa6602
- **Repository Name**: propeller-optimizer
- **Project Location**: `/home/admin123/propeller-optimizer`

## Step-by-Step Instructions

### Step 1: Install Git
Open a terminal and run:
```bash
sudo apt-get update
sudo apt-get install git
```

### Step 2: Configure Git (First Time Only)
Replace with your actual email:
```bash
git config --global user.name "JasonMa6602"
git config --global user.email "your-email@example.com"
```

### Step 3: Create Repository on GitHub
1. Go to https://github.com/new
2. Fill in:
   - Repository name: `propeller-optimizer`
   - Description: `Empirical propeller design tool for high-speed vessels—no CFD needed`
   - Visibility: **Public**
   - **IMPORTANT**: Do NOT check "Initialize with README" (we already have files)
3. Click "Create repository"

### Step 4: Initialize and Push
Navigate to the project directory and run these commands:
```bash
cd /home/admin123/propeller-optimizer

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Propeller optimizer project

🚀 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Rename branch to main
git branch -M main

# Add remote repository (this will be shown on GitHub after you create the repo)
git remote add origin https://github.com/JasonMa6602/propeller-optimizer.git

# Push to GitHub
git push -u origin main
```

### Step 5: Authentication
When you push, GitHub will ask for authentication. You have two options:

#### Option A: Personal Access Token (Recommended)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Propeller Optimizer"
4. Select scopes: Check "repo" (all sub-items)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. When git asks for password, paste the token instead

#### Option B: GitHub CLI (Alternative)
```bash
sudo apt-get install gh
gh auth login
# Follow the prompts
```

## Alternative: Manual Upload via Web Interface

If git installation doesn't work, you can upload manually:

1. Compress the project:
```bash
cd /home/admin123
tar -czf propeller-optimizer.tar.gz propeller-optimizer/
```

2. Go to https://github.com/new and create the repository
3. On the repository page, click "uploading an existing file"
4. Drag and drop all files from the project folder

## Verification

After pushing, your project should be available at:
https://github.com/JasonMa6602/propeller-optimizer

## Project Structure
Your repository contains:
- README.md - Complete documentation
- requirements.txt - Python dependencies
- LICENSE - MIT License
- src/optimizer.py - Core optimization logic
- data/propeller_type.csv - Sample data
- tests/test_optimization.py - Unit tests

## Next Steps After Upload
1. Enable GitHub Pages (optional) for documentation
2. Add more CSV data files to the `data/` folder
3. Create example Jupyter notebooks in `examples/`
4. Add GitHub Actions for automated testing

## Need Help?
If you encounter issues:
1. Check that the repository doesn't already exist
2. Verify your authentication credentials
3. Make sure you have write access to your GitHub account
