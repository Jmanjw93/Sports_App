# Troubleshooting: npm install Not Working

## Problem: "npm is not recognized"

This means **Node.js is not installed** on your system.

## Solution: Install Node.js

### Step 1: Download Node.js

1. Go to: **https://nodejs.org/**
2. Click the big green button: **"Download Node.js (LTS)"**
   - LTS = Long Term Support (most stable version)
   - This will download a file like: `node-v20.x.x-x64.msi`

### Step 2: Install Node.js

1. **Run the downloaded installer** (.msi file)
2. Click **"Next"** through the installation wizard
3. **Important**: Make sure these are checked:
   - ✅ "Automatically install the necessary tools"
   - ✅ "Add to PATH" (should be checked by default)
4. Click **"Install"**
5. Wait for installation to complete
6. Click **"Finish"**

### Step 3: Restart Your Terminal

**CRITICAL**: After installing Node.js, you MUST:

1. **Close** your current PowerShell/terminal window completely
2. **Open a NEW** PowerShell/terminal window
3. Navigate back to your project:
   ```powershell
   cd C:\Users\wyetw\sports-analytics-app
   ```

### Step 4: Verify Installation

Test that Node.js is installed:

```powershell
node --version
```

You should see something like: `v20.x.x` or `v18.x.x`

```powershell
npm --version
```

You should see something like: `10.x.x` or `9.x.x`

### Step 5: Install Frontend Dependencies

Now you can run:

```powershell
cd frontend
npm install
```

This will take a few minutes. You'll see it downloading packages.

## Common Issues

### "node is not recognized" after installation
- **Solution**: Close and reopen your terminal
- If that doesn't work, restart your computer
- Make sure you downloaded from the official site: nodejs.org

### Installation fails
- Try running the installer as Administrator (right-click → Run as administrator)
- Make sure you have enough disk space
- Check Windows Defender isn't blocking it

### npm install is slow
- This is normal! It's downloading many packages
- First install can take 5-10 minutes
- Be patient and let it finish

### npm install shows errors
- Make sure you're in the `frontend` folder
- Check your internet connection
- Try: `npm install --verbose` to see more details

## Quick Checklist

- [ ] Downloaded Node.js from nodejs.org
- [ ] Installed Node.js (ran the .msi installer)
- [ ] Closed and reopened terminal
- [ ] Verified with `node --version`
- [ ] Verified with `npm --version`
- [ ] Navigated to `frontend` folder
- [ ] Ran `npm install`

## Still Having Issues?

1. Make sure you downloaded from the **official site**: https://nodejs.org/
2. Try the **LTS version** (not the Current version)
3. Restart your computer after installation
4. Check if Node.js is in your PATH:
   ```powershell
   $env:PATH -split ';' | Select-String node
   ```

Once Node.js is installed and verified, `npm install` will work!


