# PowerShell script to push repository to GitHub
# Make sure git is installed and in your PATH

Write-Host "Initializing git repository..." -ForegroundColor Green

# Initialize git if not already initialized
if (-not (Test-Path .git)) {
    git init
    Write-Host "Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "Git repository already initialized" -ForegroundColor Yellow
}

# Add all files
Write-Host "Adding all files..." -ForegroundColor Green
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "Committing changes..." -ForegroundColor Green
    git commit -m "Initial commit: Sports analytics app with bright happy theme"
} else {
    Write-Host "No changes to commit" -ForegroundColor Yellow
}

# Add remote origin
Write-Host "Adding remote origin..." -ForegroundColor Green
git remote remove origin 2>$null
git remote add origin https://github.com/Jmanjw93/Sports_App.git

# Rename branch to main
Write-Host "Renaming branch to main..." -ForegroundColor Green
git branch -M main

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

Write-Host "Done! Repository pushed to GitHub" -ForegroundColor Green




