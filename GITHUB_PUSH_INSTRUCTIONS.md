# Instructions to Push to GitHub

The repository at https://github.com/Jmanjw93/Sports_App.git exists and is currently empty. Follow these steps to push your code:

## Prerequisites
1. **Install Git** (if not already installed):
   - Download from: https://git-scm.com/download/win
   - During installation, make sure to select "Add Git to PATH"
   - Restart your terminal after installation

## Steps to Push

### Option 1: Using Git Bash (Recommended)
1. Open **Git Bash** (installed with Git)
2. Navigate to your project:
   ```bash
   cd /c/Users/wyetw/sports-analytics-app
   ```

3. Initialize git (if not already initialized):
   ```bash
   git init
   ```

4. Add all files:
   ```bash
   git add .
   ```

5. Create initial commit:
   ```bash
   git commit -m "Initial commit: Sports analytics app with bright happy theme"
   ```

6. Add remote repository:
   ```bash
   git remote add origin https://github.com/Jmanjw93/Sports_App.git
   ```

7. Rename branch to main:
   ```bash
   git branch -M main
   ```

8. Push to GitHub:
   ```bash
   git push -u origin main
   ```

### Option 2: Using PowerShell/Command Prompt
If Git is installed but not in PATH, you may need to use the full path:
- Common Git installation path: `C:\Program Files\Git\bin\git.exe`

1. Open PowerShell or Command Prompt
2. Navigate to project:
   ```powershell
   cd C:\Users\wyetw\sports-analytics-app
   ```

3. Use full path to git (if needed):
   ```powershell
   & "C:\Program Files\Git\bin\git.exe" init
   & "C:\Program Files\Git\bin\git.exe" add .
   & "C:\Program Files\Git\bin\git.exe" commit -m "Initial commit: Sports analytics app with bright happy theme"
   & "C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/Jmanjw93/Sports_App.git
   & "C:\Program Files\Git\bin\git.exe" branch -M main
   & "C:\Program Files\Git\bin\git.exe" push -u origin main
   ```

### Option 3: Using GitHub Desktop
1. Download GitHub Desktop: https://desktop.github.com/
2. Sign in with your GitHub account
3. Click "Add" → "Add Existing Repository"
4. Select the `sports-analytics-app` folder
5. Click "Publish repository" and select the `Sports_App` repository

## Authentication
When you push, GitHub may ask for authentication:
- **Personal Access Token**: Recommended for HTTPS
  - Create one at: https://github.com/settings/tokens
  - Select scopes: `repo` (full control of private repositories)
- **SSH Key**: Alternative method
  - Set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

## Troubleshooting

### If you get "remote origin already exists":
```bash
git remote remove origin
git remote add origin https://github.com/Jmanjw93/Sports_App.git
```

### If you need to force push (use with caution):
```bash
git push -u origin main --force
```

### If you get authentication errors:
- Make sure you're signed in to GitHub
- Use a Personal Access Token instead of password
- Or set up SSH keys

## Files to Push
The `.gitignore` file is already configured to exclude:
- `node_modules/`
- `.next/`
- `__pycache__/`
- `.env` files
- Other build artifacts

All source code and configuration files will be pushed.




