# Installation Steps - Follow These Exactly

Complete step-by-step installation guide for the CV Modifier application.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key
- (Optional) Microsoft Word or LibreOffice for PDF conversion

## Step 1: Activate the Virtual Environment

The virtual environment has been created. Now activate it:

```bash
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt.

## Step 2: Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- **Flask** (web framework)
- **python-docx** (document handling with formatting preservation)
- **beautifulsoup4** (web scraping)
- **requests** (HTTP library)
- **google-generativeai** (Gemini API)
- **python-dotenv** (environment variables)
- **Werkzeug** (WSGI utilities)
- **docx2pdf** (PDF conversion)

## Step 3: Configure API Key

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Get your Gemini API key from: https://makersuite.google.com/app/apikey

3. Edit the `.env` file:
```bash
nano .env
```
Or open it in any text editor and add:
```
GEMINI_API_KEY=your_actual_api_key_here
FLASK_SECRET_KEY=any_random_string_12345
FLASK_ENV=development
```

**Important**: Replace `your_actual_api_key_here` with your real Gemini API key!

## Step 4: Setup PDF Conversion (Optional)

For PDF output, you need document conversion software:

### macOS (you):
**Option 1** - Use Microsoft Word (if installed):
- Nothing to do! The app will auto-detect Word

**Option 2** - Install LibreOffice (free):
```bash
brew install --cask libreoffice
```

### Windows:
- Install Microsoft Word (if not already installed)

### Linux:
```bash
sudo apt-get install libreoffice
```

**Note**: If neither is available, the app will output DOCX files which you can manually convert to PDF.

## Step 5: Verify Installation

Test that everything is installed correctly:

```bash
# Check Python version
python3 --version

# Check if all packages installed
pip list | grep -E "Flask|docx|beautifulsoup4|gemini"

# Check if virtual environment is active
which python  # Should show path with 'venv' in it
```

## Step 6: Run the Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## Step 7: Open in Browser

Go to: **http://localhost:5000**

You should see the CV Modifier web interface!

---

## Quick Commands Summary

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install packages (already done if successful)
pip install -r requirements.txt

# 3. Configure .env (edit with your API key)
cp .env.example .env
nano .env

# 4. Run the app
python app.py

# 5. Open browser
# Navigate to http://localhost:5000
```

## Troubleshooting

### Virtual environment not activating?
Make sure you're in the correct directory:
```bash
cd "/Users/sheikhozairbilal/Desktop/Personal/Personal Projects/CV modifier"
```

### Still getting "externally-managed-environment" error?
Make sure the virtual environment is activated (you should see `(venv)` in your prompt).

### Import errors when running app.py?
The virtual environment must be activated before running the app:
```bash
source venv/bin/activate
python app.py
```

### PDF conversion not working?
Install LibreOffice:
```bash
brew install --cask libreoffice
```

Or just use DOCX output - it preserves formatting perfectly and can be converted manually.

### Gemini API errors?
- Verify API key in `.env` is correct
- No extra spaces or quotes around the key
- Check quota at https://makersuite.google.com/app/apikey

## Testing the Application

1. **Upload a test CV**:
   - Create a simple .docx file with your CV
   - Or use an existing one

2. **Find a job posting URL**:
   - Any public job posting works
   - LinkedIn, Indeed, company career pages

3. **Test the workflow**:
   - Upload CV
   - Paste job URL
   - Click "Analyze & Modify"
   - Review preview
   - Download PDF

## Production Deployment

For production use:

1. Change `FLASK_ENV=production` in `.env`
2. Generate a strong `FLASK_SECRET_KEY`
3. Use Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
4. Set up Nginx reverse proxy
5. Enable HTTPS
6. Implement file cleanup
7. Add rate limiting

## Uninstallation

To remove everything:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove uploaded files
rm -rf uploads/* modified/*

# Keep the source code if you want to reinstall later
```

---

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [QUICKSTART.md](QUICKSTART.md) for usage tips
- Start optimizing your CVs!

**Support**: Check documentation or Google Gemini API docs for help.
