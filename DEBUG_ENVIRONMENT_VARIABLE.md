# 🔍 Debug: Environment Variable Not Working

## Check What's Actually Happening

### Step 1: Check Browser Console

1. **Open your frontend:** `https://sports-7t1fit3av-jmanjw93s-projects.vercel.app`

2. **Open Developer Tools:** Press **F12**

3. **Go to "Console" tab** (not Elements)

4. **Type this command and press Enter:**
   ```javascript
   console.log(process.env.NEXT_PUBLIC_API_URL)
   ```

5. **What do you see?**
   - ✅ `https://sports-app-ncya.onrender.com` = Variable is set correctly
   - ❌ `undefined` = Variable is NOT set
   - ❌ `http://localhost:8001` = Variable is set to wrong value

---

### Step 2: Check Network Tab

1. **Stay in Developer Tools (F12)**

2. **Go to "Network" tab**

3. **Try to load games or make a prediction**

4. **Look at the failed request:**
   - What URL is it trying to connect to?
   - Is it `localhost:8001` or `https://sports-app-ncya.onrender.com`?

---

## Common Issues & Fixes

### Issue 1: Environment Variable Shows `undefined`

**Problem:** Variable not set in Vercel

**Fix:**
1. Go to: https://vercel.com/jmanjw93s-projects/sports-app/89Spn3nUXysiYX1wBJVbqQDf3HdW/settings/environment-variables
2. Verify `NEXT_PUBLIC_API_URL` exists
3. Verify value is: `https://sports-app-ncya.onrender.com` (no quotes, no trailing slash)
4. Make sure Production, Preview, Development are all checked
5. Click "Save"
6. **Redeploy** (very important!)

---

### Issue 2: Variable Set But Still Using localhost

**Problem:** Frontend wasn't redeployed after setting variable

**Fix:**
1. Go to: https://vercel.com/jmanjw93s-projects/sports-app/89Spn3nUXysiYX1wBJVbqQDf3HdW/deployments
2. Click three dots (⋯) on latest deployment
3. Click "Redeploy"
4. Wait for deployment to complete
5. Hard refresh browser: **Ctrl+F5** (Windows) or **Cmd+Shift+R** (Mac)

---

### Issue 3: Variable Set But Shows Wrong Value

**Problem:** Typo or wrong format

**Fix:**
1. Check the value in Vercel:
   - Should be: `https://sports-app-ncya.onrender.com`
   - Should NOT have: trailing slash, quotes, spaces
2. Delete the variable and add it again
3. Redeploy

---

### Issue 4: Browser Cache

**Problem:** Browser is using cached version

**Fix:**
1. Hard refresh: **Ctrl+F5** (Windows) or **Cmd+Shift+R** (Mac)
2. Or clear browser cache completely
3. Or try incognito/private window

---

## Step-by-Step Verification

### In Vercel Dashboard:

1. **Go to:** Settings → Environment Variables
2. **Verify:**
   - ✅ `NEXT_PUBLIC_API_URL` exists
   - ✅ Value = `https://sports-app-ncya.onrender.com`
   - ✅ Production is checked
   - ✅ Preview is checked
   - ✅ Development is checked

### In Vercel Deployments:

1. **Go to:** Deployments tab
2. **Check latest deployment:**
   - ✅ Status = "Ready"
   - ✅ Was deployed AFTER you set the environment variable
   - ❌ If it's an old deployment, redeploy

### In Browser:

1. **Open Console (F12)**
2. **Type:** `console.log(process.env.NEXT_PUBLIC_API_URL)`
3. **Should show:** `https://sports-app-ncya.onrender.com`

---

## Nuclear Option: Delete and Re-add

If nothing works:

1. **In Vercel:** Delete `NEXT_PUBLIC_API_URL` variable
2. **Add it again** with value: `https://sports-app-ncya.onrender.com`
3. **Make sure all environments are checked**
4. **Save**
5. **Redeploy frontend**
6. **Wait for deployment**
7. **Hard refresh browser**

---

## What to Tell Me

Please check the browser console and tell me:

1. **What does `console.log(process.env.NEXT_PUBLIC_API_URL)` show?**
   - Is it `undefined`?
   - Is it `http://localhost:8001`?
   - Is it `https://sports-app-ncya.onrender.com`?

2. **In Network tab, what URL is the failed request trying to connect to?**

3. **When did you last redeploy the frontend?** (Before or after setting the variable?)

This will help me figure out exactly what's wrong!

