# FixTheVuln Setup Checklist

## Phase 1: GitHub Setup (5 minutes)

- [ ] Create GitHub account (if you don't have one)
- [ ] Create new PUBLIC repository called `fixthevuln`
- [ ] Upload all files from `fixthevuln-site/` folder
- [ ] Go to "Actions" tab and enable workflows
- [ ] Test: Click "Run workflow" manually to test

**How to upload files to GitHub:**
```
Option A - Via GitHub Website:
1. Go to your repository
2. Click "Add file" → "Upload files"
3. Drag ALL files from fixthevuln-site folder
4. Click "Commit changes"

Option B - Via Git Command Line:
1. Open terminal in fixthevuln-site folder
2. Run these commands:
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/fixthevuln.git
   git push -u origin main
```

## Phase 2: Netlify Setup (10 minutes)

- [ ] Sign up at netlify.com (free)
- [ ] Click "Add new site" → "Import an existing project"
- [ ] Connect GitHub account
- [ ] Select your `fixthevuln` repository
- [ ] Deploy settings:
  - Build command: (leave empty)
  - Publish directory: `/`
- [ ] Click "Deploy site"
- [ ] Wait 2-3 minutes for deploy to complete
- [ ] Click the site URL to see your live site!

## Phase 3: Custom Domain (15 minutes)

- [ ] In Netlify, go to "Domain settings"
- [ ] Click "Add custom domain"
- [ ] Enter: `fixthevuln.com`
- [ ] Netlify will show you DNS settings
- [ ] Go to your domain registrar (where you bought the domain)
- [ ] Update DNS records:
  ```
  Type: A
  Name: @
  Value: 75.2.60.5
  
  Type: CNAME
  Name: www
  Value: your-random-name.netlify.app
  ```
- [ ] Wait 5-60 minutes for DNS to update
- [ ] Test: Visit fixthevuln.com

## Phase 4: Test & Verify (5 minutes)

- [ ] Visit fixthevuln.com - does it load?
- [ ] Check all pages work (About, Services, Contact)
- [ ] Go to GitHub → Actions tab → Check if workflow ran
- [ ] Check if `posts/` folder has files
- [ ] Test contact form (Netlify handles this automatically)

## Phase 5: Customize Content (30 minutes)

- [ ] Edit `about.html` - add your name, photo, credentials
- [ ] Edit `services.html` - update pricing, add your details
- [ ] Edit `contact.html` - add your email, phone, calendar link
- [ ] Update all `[Your Name]` placeholders
- [ ] Add real images to `images/` folder
- [ ] Commit and push changes to GitHub
- [ ] Netlify auto-deploys (takes 1-2 minutes)

## Phase 6: Optional Enhancements

- [ ] Set up Google Analytics
- [ ] Add newsletter signup (ConvertKit, Mailchimp)
- [ ] Create social media accounts
- [ ] Write your first manual blog post
- [ ] Set up email forwarding (hello@fixthevuln.com)
- [ ] Add favicon
- [ ] Create logo/branding

## Troubleshooting

**GitHub Actions not running?**
- Repository must be PUBLIC for free Actions
- Check Actions tab for error messages
- Make sure Python files have correct permissions

**Netlify not deploying?**
- Check deploy logs in Netlify dashboard
- Make sure all files are in root directory
- Check netlify.toml is present

**Domain not working?**
- DNS can take up to 24 hours (usually 5-60 min)
- Check DNS propagation: whatsmydns.net
- Make sure you added both A and CNAME records

**Posts not generating?**
- Check GitHub Actions logs
- Make sure API sources are accessible
- Run `python fetch_news.py` locally to test

## Success Metrics

After setup, you should have:
- ✅ Live website at fixthevuln.com
- ✅ Daily auto-generated security news posts
- ✅ Professional About/Services/Contact pages
- ✅ Working contact form
- ✅ Zero monthly costs (except $12/year domain)

## Next Steps

1. Share your site on LinkedIn/Twitter
2. Start engaging with the security community
3. Add your commentary to auto-generated posts
4. Build your email list
5. Land your first client!

---

Questions? Check README.md or email hello@fixthevuln.com
