# Install Node.js

Node.js is required to run the frontend. Here's how to install it:

## Quick Install

1. **Download Node.js**:
   - Go to: https://nodejs.org/
   - Click "Download Node.js (LTS)" - this is the recommended version
   - The LTS version is stable and well-supported

2. **Install Node.js**:
   - Run the downloaded installer (.msi file)
   - Click "Next" through the installation wizard
   - **Important**: Make sure "Add to PATH" is checked (it should be by default)
   - Click "Install"

3. **Verify Installation**:
   - Close and reopen your PowerShell/terminal
   - Run: `node --version`
   - You should see something like: `v20.x.x` or `v18.x.x`

4. **Install Frontend Dependencies**:
   ```powershell
   cd frontend
   npm install
   cd ..
   ```

5. **Run the Application**:
   - See RUN_APPLICATION.md for complete instructions

## Alternative: Using Chocolatey (if you have it)

```powershell
choco install nodejs-lts
```

## Troubleshooting

### "node is not recognized" after installation
- Close and reopen your terminal/PowerShell
- Restart your computer if needed
- Check that Node.js was added to PATH during installation

### Installation Issues
- Make sure you download from the official site: https://nodejs.org/
- Try the LTS (Long Term Support) version
- Run the installer as Administrator if needed

Once Node.js is installed, come back and we'll install the frontend dependencies!

