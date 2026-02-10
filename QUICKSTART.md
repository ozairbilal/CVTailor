# Quick Start Guide

## Get Your Gemini API Key First! 🔑

Before running the application, you need a Google Gemini API key:

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy the API key

## Setup (5 minutes)

### Option 1: Automated Setup (Recommended)
```bash
./setup.sh
```

Then edit `.env` file and paste your API key.

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# 3. Install packages
pip install -r requirements.txt

# 4. Create config file
cp .env.example .env

# 5. Edit .env and add your keys
nano .env  # or use any text editor
```

Your `.env` should look like:
```
GEMINI_API_KEY=AIzaSyC...your_actual_key_here
FLASK_SECRET_KEY=any_random_string_here_12345
```

## PDF Conversion Setup (Optional but Recommended)

For PDF output, you need one of these:

### macOS:
```bash
# Option 1: Use Microsoft Word (if installed) - Nothing to do!
# Option 2: Install LibreOffice (free)
brew install --cask libreoffice
```

### Windows:
- Install Microsoft Word (if not already installed)

### Linux:
```bash
sudo apt-get install libreoffice
```

**Note**: If PDF conversion is not available, the app will give you DOCX files instead.

## Run the App

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run
python app.py
```

Open browser: **http://localhost:5000**

## Usage

1. **Paste job URL** (e.g., LinkedIn job posting, company career page)
2. **Upload your CV** (.docx file)
3. **Click "Analyze & Modify"**
4. **Wait ~15-30 seconds** ⏳
5. **Review the preview**:
   - Match score percentage
   - Changes summary
   - Side-by-side comparison
6. **Download** your optimized CV as PDF! 📥

## Tips

- ✅ Works best with public job postings
- ✅ Your CV should be in .docx format
- ✅ Gemini free tier has generous limits
- ✅ Original formatting is preserved (fonts, colors, bold, links)
- ⚠️ LinkedIn may require login for some job posts
- ⚠️ First API call may take a bit longer
- ⚠️ PDF output requires MS Word or LibreOffice

## What Gets Modified?

**✅ Modified:**
- Experience descriptions (enhanced with keywords)
- Bullet points (made more impactful)
- Skills emphasis (relevant to job)

**❌ NOT Modified:**
- Your name and contact info
- Job titles and company names
- Dates and education
- Overall structure
- Formatting (fonts, colors, bold)

## Troubleshooting

**Can't extract job description?**
- Make sure the URL is publicly accessible
- Try a different job posting site
- Some sites block scraping

**Gemini API error?**
- Double-check your API key in `.env`
- Ensure you have quota (check Google AI Studio)
- Make sure there are no extra spaces in the key

**File upload fails?**
- Only .doc and .docx supported
- Max size: 16MB
- File shouldn't be password-protected

**Getting DOCX instead of PDF?**
- Install Microsoft Word or LibreOffice
- DOCX output still works great - just convert manually if needed

## Need Help?

See the full [README.md](README.md) for detailed documentation.

---

Happy job hunting! 🎯
