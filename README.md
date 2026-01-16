# FixTheVuln - Automated Security News Blog

🔒 Your automated vulnerability remediation blog that updates daily with the latest security news!

## What This Does

- **Automatically fetches** security news from CISA, NVD, Bleeping Computer, and The Hacker News
- **Generates blog posts** every day at 6 AM UTC
- **Zero maintenance** - runs completely automated via GitHub Actions
- **100% FREE** - no hosting costs, no API fees

## Quick Start Guide

### 1. Set Up GitHub Repository

1. **Create a new GitHub repository** (public or private)
   - Go to github.com → New Repository
   - Name it `fixthevuln` (or whatever you want)
   - Make it PUBLIC (required for free GitHub Actions)

2. **Upload these files** to your repository:
   - Drag and drop all files from this folder
   - OR use Git commands:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/fixthevuln.git
   git push -u origin main
   ```

### 2. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. You should see "Daily Security News Update" workflow
4. Click **"Enable Actions"** if prompted

**That's it!** The script will run automatically every day at 6 AM UTC.

### 3. Deploy to Netlify

1. **Sign up at Netlify** (free): https://netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect your GitHub account
4. Select your `fixthevuln` repository
5. Deploy settings:
   - Build command: (leave empty)
   - Publish directory: `/`
6. Click **"Deploy site"**

**Boom!** Your site is live at `random-name.netlify.app`

### 4. Connect Your Custom Domain

1. In Netlify, go to **"Domain settings"**
2. Click **"Add custom domain"**
3. Enter `fixthevuln.com`
4. Netlify will give you DNS settings
5. Go to your domain registrar (where you bought the domain)
6. Add these DNS records:
   - Type: `A` → Value: `75.2.60.5`
   - Type: `CNAME` → Name: `www` → Value: `your-site.netlify.app`
7. Wait 5-60 minutes for DNS to propagate

**Done!** Your site is live at fixthevuln.com 🎉

## How It Works

```
Every day at 6 AM UTC:
┌─────────────────────────────────────┐
│ GitHub Actions triggers Python script│
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Fetches latest security news from:  │
│ - CISA Known Exploited Vulnerabilities│
│ - Bleeping Computer RSS             │
│ - The Hacker News RSS               │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Generates HTML blog posts           │
│ Saves to /posts/ directory          │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Commits changes to GitHub           │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Netlify auto-deploys updated site   │
└─────────────────────────────────────┘
```

## File Structure

```
fixthevuln-site/
├── index.html              # Homepage (blog listing)
├── about.html              # About page
├── services.html           # Services page
├── contact.html            # Contact page
├── fetch_news.py           # Python script that fetches news
├── requirements.txt        # Python dependencies
├── posts/                  # Auto-generated blog posts (created by script)
│   ├── 2026-01-09-cisa-alert-cve-xxxx.html
│   ├── 2026-01-09-critical-jenkins-vuln.html
│   └── index.json          # Index of all posts
└── .github/
    └── workflows/
        └── daily-update.yml # GitHub Actions workflow
```

## Manual Testing

Want to test the news fetcher locally before going live?

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the script
python fetch_news.py

# Check the generated posts
ls posts/
```

## Customization

### Change Update Time

Edit `.github/workflows/daily-update.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'  # Change '6' to your preferred hour (UTC)
```

### Add More News Sources

Edit `fetch_news.py` and add to `NEWS_SOURCES` dictionary:
```python
NEWS_SOURCES = {
    'your_source': 'https://example.com/feed.xml',
}
```

### Customize Blog Post Template

The script generates posts automatically, but you can customize the HTML template 
by editing the `generate_blog_post()` function in `fetch_news.py`.

## Troubleshooting

**GitHub Actions not running?**
- Make sure your repository is PUBLIC (private repos have limited free Actions)
- Check the Actions tab for error logs

**Posts not showing up?**
- Check `posts/` directory exists in your repo
- Look at GitHub Actions logs for errors

**Netlify not updating?**
- Netlify auto-deploys when GitHub changes
- Check Netlify deploy logs

**Need help?**
- Check GitHub Actions logs: Repository → Actions tab
- Check Netlify deploy logs: Netlify dashboard → Deploys

## Cost Breakdown

| Service | Cost |
|---------|------|
| GitHub (repository + Actions) | $0/month |
| Netlify (hosting) | $0/month |
| Domain (fixthevuln.com) | ~$12/year |
| **Total** | **~$1/month** |

## What's Next?

1. **Customize your pages** - Add your name, photo, real credentials
2. **Write your first manual post** - Add your expert commentary to auto-generated posts
3. **Set up analytics** - Add Google Analytics to track visitors
4. **Set up contact form** - Use Netlify Forms (built-in and free)
5. **Add newsletter** - Use ConvertKit or Mailchimp free tier

## Pro Tips

- **Manual posts:** Create HTML files in `/posts/` to write custom content
- **SEO:** Add meta descriptions and keywords to your pages
- **Social sharing:** Add Open Graph tags for better social media previews
- **Newsletter:** Repurpose daily posts into a weekly newsletter
- **Monetization:** Once you have traffic, add affiliate links or consulting CTAs

---

## Support

Questions? Issues? Want to add features?

- Email: hello@fixthevuln.com
- Open an issue on GitHub
- Check the blog for tutorials

**Now go make this thing LIVE!** 🚀
