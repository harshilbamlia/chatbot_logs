# Deployment Guide for Streamlit Cloud

This guide will help you deploy the AI Database Chatbot to Streamlit Cloud.

## Prerequisites

1. A GitHub account
2. Azure OpenAI API access
3. PostgreSQL database (accessible from the internet)
4. Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

## Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit - AI Database Chatbot"
```

### 1.2 Create GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository
2. Name it `chatbot_logs` or any name you prefer
3. **DO NOT** initialize with README (you already have one)

### 1.3 Push Code to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

**IMPORTANT:** The `.gitignore` file ensures sensitive files (`.env`, `.streamlit/secrets.toml`) are NOT pushed to GitHub.

## Step 2: Deploy to Streamlit Cloud

### 2.1 Sign Up / Login

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Grant Streamlit access to your repositories

### 2.2 Create New App

1. Click **"New app"**
2. Select your repository: `YOUR_USERNAME/YOUR_REPO_NAME`
3. Set **Branch**: `main`
4. Set **Main file path**: `app.py`
5. Click **"Advanced settings"** before deploying

### 2.3 Configure Secrets

In the Advanced settings, paste your secrets in TOML format:

```toml
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = "BmqSfnv7SLa92veHN0uXgworg0T7kbpe2BOi8tvlcPOPwUnYhrl5JQQJ99BDACYeBjFXJ3w3AAABACOGZlOo"
AZURE_OPENAI_ENDPOINT = "https://aonami.openai.azure.com"
AZURE_OPENAI_DEPLOYMENT = "o4-mini"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"

# Database Configuration
DATABASE_URL = "postgresql://postgres.qhhpwyyqoljvievtebyz:password@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"
```

**Security Note:** Replace with your actual credentials. These secrets are encrypted and only accessible to your app.

### 2.4 Deploy

1. Click **"Deploy!"**
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

## Step 3: Verify Deployment

1. Visit your app URL
2. Test with queries like:
   - "What tables are available?"
   - "Show me the first 5 rows from execution_logs"
   - "How many executions are there?"

## Managing Your Deployment

### Update Your App

Push changes to GitHub and Streamlit will auto-deploy:

```bash
git add .
git commit -m "Update chatbot"
git push
```

### Update Secrets

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click your app → "Settings" → "Secrets"
3. Update values and save
4. Reboot app if needed

### View Logs

1. Click your app in Streamlit Cloud dashboard
2. Click "Manage app" → "Logs"
3. View real-time logs and debug output

### Reboot App

If something goes wrong:
1. Go to app settings
2. Click **"Reboot app"**

## Troubleshooting

### Connection Issues

If database connections fail:
- Verify DATABASE_URL is correct
- Ensure database allows connections from Streamlit Cloud IPs
- Check if database requires SSL (Supabase does by default)

### Import Errors

If you see import errors:
- Check `requirements.txt` has all dependencies
- Verify Python version compatibility
- Look at deployment logs for details

### API Errors

If Azure OpenAI fails:
- Verify API key is correct
- Check deployment name matches
- Ensure API version is supported

## File Structure

```
chatbot_logs/
├── .gitignore              # Excludes sensitive files
├── .streamlit/
│   ├── config.toml        # UI configuration
│   └── secrets.toml.example  # Template for secrets
├── app.py                 # Main Streamlit app
├── chatbot/
│   ├── __init__.py
│   ├── database.py        # Database manager
│   ├── rag.py            # RAG chatbot logic
│   └── bot.py            # Simple chatbot (unused)
├── requirements.txt       # Python dependencies
├── README.md             # Project overview
└── DEPLOYMENT.md         # This file
```

## Security Best Practices

✅ **DO:**
- Use Streamlit secrets for production
- Keep `.env` in `.gitignore`
- Rotate API keys regularly
- Use read-only database credentials if possible

❌ **DON'T:**
- Commit `.env` or `secrets.toml` to git
- Share secrets in public channels
- Use production credentials in development
- Hardcode secrets in code

## Cost Considerations

- **Streamlit Cloud**: Free for public apps (limited resources)
- **Azure OpenAI**: Pay per token usage
- **Database**: Depends on your hosting provider

## Support

For issues:
- Streamlit Cloud: [docs.streamlit.io](https://docs.streamlit.io)
- Azure OpenAI: [Azure Portal](https://portal.azure.com)
- This app: Open an issue on GitHub

---

**Deployed successfully?** 🎉 Share your app URL and start querying your database with AI!
