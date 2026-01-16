# Unsplash Integration Update 📸

## What's New

Your blog posts now automatically include professional, high-quality images from Unsplash!

### Features Added:
✅ Auto-fetches relevant security-themed images for each post
✅ Downloads and saves images to `/images/` folder
✅ Adds photo credit to comply with Unsplash guidelines
✅ Smart keyword matching (Docker posts get container images, SQL posts get database images, etc.)
✅ Respects API rate limits with built-in delays

---

## Files to Update in Your GitHub Repo

You need to replace 2 files:

### 1. **fetch_news.py** (The main script)
- New version includes Unsplash API integration
- Downloads images automatically
- Adds image credits to posts

### 2. **.github/workflows/daily-update.yml** (The automation workflow)
- Updated to pass your Unsplash API key securely
- Now commits both posts AND images folders

---

## How to Update

### Step 1: Update fetch_news.py

1. Go to your GitHub repo: https://github.com/YOUR_USERNAME/fixthevuln
2. Click on **fetch_news.py**
3. Click the **pencil icon** to edit
4. **Delete all the old code**
5. **Copy the new code** from `fetch_news.py` (in this folder)
6. **Paste** it in
7. Click **"Commit changes"**

### Step 2: Update the GitHub Actions workflow

1. In your repo, navigate to: `.github/workflows/daily-update.yml`
2. Click the **pencil icon** to edit
3. **Delete all the old code**
4. **Copy the new code** from `.github/workflows/daily-update.yml` (in this folder)
5. **Paste** it in
6. Click **"Commit changes"**

### Step 3: Test It!

1. Go to **Actions** tab in your repo
2. Click on "Daily Security News Update"
3. Click **"Run workflow"**
4. Watch it run (should take 1-2 minutes)
5. Check the `images/` folder in your repo - you should see new .jpg files!
6. Check the `posts/` folder - posts should now have images!

---

## What Happens Now

Every day at 6 AM UTC, your automation will:
1. Fetch latest security news ✅
2. For each article, fetch a relevant Unsplash image 📸
3. Download the image to `/images/` folder
4. Generate blog post HTML with the image embedded
5. Add photo credit (required by Unsplash)
6. Commit everything to GitHub
7. Netlify auto-deploys your updated site 🚀

---

## Image Selection Logic

The script intelligently matches images to content:

- **"docker" or "container"** in title → Gets container/DevOps images
- **"sql" or "database"** in title → Gets database security images
- **"jenkins" or "ci/cd"** in title → Gets DevOps/automation images
- **"cloud"** in title → Gets cloud computing images
- **Everything else** → Gets general cybersecurity images

---

## Unsplash API Limits

**Free tier:** 50 requests/hour

Since you're generating ~10 posts/day = 10 images/day, you're well within limits!

---

## Troubleshooting

**Images not showing up?**
- Check GitHub Actions logs for errors
- Make sure `UNSPLASH_ACCESS_KEY` secret is set correctly
- Verify the secret name matches exactly: `UNSPLASH_ACCESS_KEY`

**"No Unsplash API key found" error?**
- The workflow isn't passing the secret correctly
- Double-check the `.github/workflows/daily-update.yml` file has the `env:` section

**Rate limit errors?**
- You're making too many requests
- The script has built-in 0.5 second delays to prevent this
- Free tier = 50/hour, you'll never hit this with 10 posts/day

---

## Photo Credits

Images automatically include credits like:
> Photo by [Photographer Name] on Unsplash

This is **required** by Unsplash's terms of service and is automatically added to every post!

---

## Cost

**Still $0/month!** 🎉

Unsplash API is completely free for your usage level.

---

## Ready to Update?

Follow the steps above to update your two files, then run the workflow manually to test. Your blog will look way more professional with these images! 📸✨
