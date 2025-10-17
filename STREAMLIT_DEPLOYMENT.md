# 🚀 Streamlit Cloud Deployment Guide

## Overview
This guide walks you through deploying the Shuru Tech RAG Chatbot to Streamlit Cloud for free public hosting.

---

## Prerequisites

✅ GitHub account with repository: https://github.com/samaysalunke/shuru-repo.git  
✅ Anthropic API key (for Claude 3.5 Sonnet)  
✅ Code pushed to GitHub (✅ DONE)

---

## Step 1: Sign Up for Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"Sign up"** or **"Get started"**
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit to access your GitHub account

---

## Step 2: Deploy Your App

### Option A: Deploy from Dashboard

1. Once logged in, click **"New app"** button
2. Fill in the deployment form:
   ```
   Repository: samaysalunke/shuru-repo
   Branch: main
   Main file path: app.py
   ```
3. Click **"Advanced settings"** (optional)
   - Python version: 3.11 or 3.12
   - Keep default settings

4. Click **"Deploy!"**

### Option B: Deploy via URL

Visit this direct link (replace with your info):
```
https://share.streamlit.io/deploy?repository=samaysalunke/shuru-repo&branch=main&mainModule=app.py
```

---

## Step 3: Configure Secrets

⚠️ **IMPORTANT:** You must add your API key as a secret.

1. After deployment starts, click **"⚙️ Settings"** in the app dashboard
2. Go to **"Secrets"** tab
3. Add your secrets in TOML format:

```toml
ANTHROPIC_API_KEY = "sk-ant-xxxxxxxxxxxxxxxxxxxxx"
TEMPERATURE = "0.7"
MAX_TOKENS = "1024"
```

4. Click **"Save"**
5. App will automatically restart with secrets loaded

---

## Step 4: Verify Deployment

Your app will be available at:
```
https://[your-app-name]-[random-string].streamlit.app
```

Example:
```
https://shuru-tech-chatbot-abc123.streamlit.app
```

### Check that:
- ✅ Dashboard loads with 3 panels
- ✅ Stats panel shows case study counts
- ✅ Chat input is visible
- ✅ Case study browser appears on right
- ✅ API status shows "✅ API Connected"

---

## Step 5: Update App (After Changes)

Streamlit Cloud auto-deploys when you push to GitHub:

```bash
# Make your changes locally
git add .
git commit -m "Update: description of changes"
git push origin main
```

Streamlit Cloud will:
1. Detect the push automatically
2. Rebuild the app (~2-3 minutes)
3. Deploy the new version

---

## Troubleshooting

### Issue: App won't start

**Check:**
1. Secrets are configured correctly
2. `requirements.txt` has all dependencies
3. Python version compatibility (3.11 recommended)

**Solution:** Check logs in Streamlit Cloud dashboard

### Issue: API key not working

**Error:** `❌ API Missing` in System Status

**Solution:**
1. Verify secret name is exactly `ANTHROPIC_API_KEY` (case-sensitive)
2. Check for extra spaces or quotes in secret value
3. Restart app from settings

### Issue: Knowledge base not loading

**Error:** "Knowledge base not found"

**Solution:**
1. Verify `knowledge_base.json` is in repository root
2. Check file is not in `.gitignore`
3. Confirm file was pushed: `git ls-files | grep knowledge_base.json`

### Issue: Dependencies failing

**Error:** Build fails with module errors

**Solution:**
1. Update `requirements.txt` with exact versions:
   ```
   streamlit==1.31.0
   anthropic==0.25.0
   langchain==0.2.0
   ```
2. Push changes to trigger rebuild

### Issue: Slow loading

**Cause:** First load initializes embeddings model (~10 seconds)

**Solution:** This is normal. Subsequent loads are faster.

---

## Resource Limits (Free Tier)

Streamlit Cloud free tier includes:
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ CPU-only compute
- ✅ Auto-sleep after inactivity
- ⚠️ Wakes up on first visit (cold start)

**Optimization Tips:**
1. App sleeps after 7 days of inactivity
2. First visitor wakes it up (takes ~30 seconds)
3. Stays awake while actively used
4. Consider upgrading for private apps or more resources

---

## Custom Domain (Optional)

### Free Option: Streamlit Subdomain
Your app gets a free `.streamlit.app` subdomain automatically.

### Custom Domain (Paid Plans)
Requires Streamlit Teams or Enterprise:
1. Go to app settings
2. Navigate to "General" tab
3. Add custom domain (e.g., `chat.shurutech.com`)
4. Follow DNS configuration instructions

---

## Security Best Practices

### ✅ DO:
- Store API keys in Streamlit Secrets
- Use `.gitignore` to exclude `.env` files
- Keep `secrets.toml` out of git
- Rotate API keys periodically

### ❌ DON'T:
- Hardcode API keys in code
- Commit `.env` or `secrets.toml` to git
- Share app URL with API keys visible
- Use production API keys for testing

---

## Monitoring Your App

### View Logs:
1. Go to Streamlit Cloud dashboard
2. Click your app
3. View **"Logs"** tab for real-time output

### Analytics:
- View visitor count in dashboard
- Track app wake/sleep cycles
- Monitor resource usage

### Alerts:
Streamlit will email you if:
- App crashes repeatedly
- Build fails
- Resource limits exceeded

---

## Cost Considerations

### Free Tier:
- ✅ **Cost:** $0/month
- ✅ **Apps:** Unlimited public apps
- ✅ **Usage:** Moderate traffic
- ⚠️ **Limits:** Auto-sleep, 1GB RAM

### Paid Tiers:
If you need more:
- **Starter:** $20/month (private apps, more resources)
- **Teams:** $250/month (team collaboration, custom domains)
- **Enterprise:** Custom pricing (SSO, SLA, dedicated support)

For this chatbot, **free tier is sufficient** for demos and low-traffic use.

---

## Alternative Hosting Options

If Streamlit Cloud doesn't meet your needs:

### 1. **Render.com** (Free tier available)
- Docker-based deployment
- More control over environment
- Free SSL certificates

### 2. **Railway.app** (Free $5 credit/month)
- Simple git-based deployment
- Good for production apps
- Pay-as-you-go pricing

### 3. **Hugging Face Spaces** (Free)
- Specialized for ML/AI apps
- Good community support
- Gradio or Streamlit interface

### 4. **AWS/GCP/Azure** (Paid)
- Full control and scalability
- More expensive
- Requires DevOps knowledge

---

## Updating Your Deployment

### Quick Updates (Code Only):
```bash
git add .
git commit -m "Fix: bug description"
git push origin main
```
Auto-deploys in ~2 minutes.

### Dependency Updates:
```bash
# Update requirements.txt
pip freeze > requirements.txt

git add requirements.txt
git commit -m "Update: dependencies"
git push origin main
```
Rebuilds app (~5 minutes).

### Configuration Updates:
1. Edit secrets in Streamlit Cloud dashboard
2. Or update `.streamlit/config.toml` and push

---

## Performance Optimization

### 1. Caching
Already implemented in code:
```python
@st.cache_resource
def load_bot():
    return ShuruTechRAGBot()
```

### 2. Reduce Cold Starts
- Keep app active by visiting regularly
- Or upgrade to paid plan (no auto-sleep)

### 3. Optimize Knowledge Base
- Keep `knowledge_base.json` under 10MB
- Limit case studies to most relevant ones
- Remove unused fields

### 4. Monitor Performance
- Check logs for slow queries
- Profile with Streamlit's built-in profiler
- Optimize FAISS index if needed

---

## Support & Resources

### Official Documentation:
- **Streamlit Docs:** https://docs.streamlit.io
- **Deployment Guide:** https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app
- **Secrets Management:** https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management

### Community:
- **Forum:** https://discuss.streamlit.io
- **Discord:** https://discord.gg/streamlit
- **GitHub Issues:** https://github.com/streamlit/streamlit/issues

### Anthropic API:
- **API Docs:** https://docs.anthropic.com
- **Rate Limits:** Check your plan limits
- **Pricing:** https://www.anthropic.com/pricing

---

## Checklist Before Going Live

- [ ] Code pushed to GitHub
- [ ] `requirements.txt` is complete
- [ ] `.gitignore` excludes sensitive files
- [ ] Streamlit Cloud account created
- [ ] App deployed successfully
- [ ] Secrets configured (API key)
- [ ] Dashboard loads with 3 panels
- [ ] Chat functionality works
- [ ] Case studies display correctly
- [ ] API status shows connected
- [ ] Test on mobile device
- [ ] Share URL with stakeholders

---

## Your Deployment URLs

| Resource | URL |
|----------|-----|
| **GitHub Repo** | https://github.com/samaysalunke/shuru-repo.git |
| **Streamlit Cloud** | https://share.streamlit.io |
| **App URL** | (Will be generated after deployment) |

---

## Next Steps

1. ✅ **Code is pushed to GitHub**
2. 🔄 **Deploy on Streamlit Cloud** (follow Step 2 above)
3. 🔑 **Add API key to secrets** (follow Step 3 above)
4. ✅ **Test the live app**
5. 📱 **Share with your team!**

---

**Need help?** Check the troubleshooting section or reach out on [Streamlit Community Forum](https://discuss.streamlit.io).

**Ready to deploy?** Visit [share.streamlit.io](https://share.streamlit.io) now! 🚀

