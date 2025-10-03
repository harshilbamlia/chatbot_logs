# Quick Deploy to Streamlit Cloud 🚀

## 5-Minute Deployment Checklist

### ✅ Step 1: Initialize Git & Push to GitHub (2 min)

```bash
# Initialize git
git init

# Add all files (sensitive files are already in .gitignore)
git add .

# Commit
git commit -m "Initial commit - AI Database Chatbot"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### ✅ Step 2: Deploy on Streamlit Cloud (2 min)

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"New app"**
3. Select your GitHub repo
4. Main file: `app.py`
5. Click **"Advanced settings"**

### ✅ Step 3: Add Secrets (1 min)

Paste this in the secrets section (with your actual values):

```toml
AZURE_OPENAI_API_KEY = "your-actual-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com"
AZURE_OPENAI_DEPLOYMENT = "your-deployment"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"
DATABASE_URL = "postgresql://user:pass@host:5432/db"
```

### ✅ Step 4: Deploy!

Click **"Deploy"** and wait 2-3 minutes.

---

## Files Created for Deployment

✅ `.gitignore` - Protects sensitive files
✅ `.streamlit/config.toml` - UI configuration
✅ `.streamlit/secrets.toml.example` - Secrets template
✅ `DEPLOYMENT.md` - Full deployment guide
✅ Updated `chatbot/rag.py` - Supports Streamlit secrets

---

## Your app will be live at:
`https://your-app-name.streamlit.app`

🎉 **That's it!** Your AI Database Chatbot is now live on the internet!
