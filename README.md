# CV Modifier - AI-Powered Resume Optimizer

A minimal viable web application that optimizes your CV/resume to match job descriptions using Google Gemini AI. Upload your CV and provide a job posting URL - the app will analyze, modify, and enhance your resume to maximize your match score while preserving your original formatting.

## 🌟 Features

- **Job Description Extraction**: Automatically extracts job requirements from LinkedIn, company websites, and other job boards
- **AI-Powered CV Optimization**: Uses Google Gemini to intelligently modify your CV experience descriptions
- **Formatting Preservation**: Maintains your original DOCX formatting (fonts, colors, bold, links)
- **Side-by-Side Comparison**: Preview original vs. modified CV before downloading
- **Match Score**: Get a percentage score showing how well your CV matches the job
- **Changes Summary**: See exactly what was changed and why
- **PDF Output**: Download your optimized CV as a PDF file (requires MS Word or LibreOffice)
- **ATS Optimization**: Automatically adds relevant keywords for Applicant Tracking Systems

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available at [Google AI Studio](https://makersuite.google.com/app/apikey))
- Microsoft Word (for PDF conversion) OR LibreOffice (free alternative)

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd "CV modifier"
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   FLASK_SECRET_KEY=your_random_secret_key_here
   ```

   To get a Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy and paste into `.env`

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📖 How to Use

1. **Enter Job URL**: Paste the URL of the job posting (LinkedIn, company career page, etc.)
2. **Upload Your CV**: Select your CV/resume file (`.docx` or `.doc` format)
3. **Click "Analyze & Modify"**: Wait while AI processes your CV (usually 10-30 seconds)
4. **Review Changes**: 
   - See your match score
   - Read the summary of changes made
   - Compare original vs. modified CV side-by-side
5. **Download**: Click "Download Modified CV" to get your optimized resume as PDF

## 🏗️ Project Structure

```
cv-modifier/
├── app.py                  # Flask application (main entry point)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── QUICKSTART.md          # Quick setup guide
├── INSTALL_STEPS.md       # Detailed installation instructions
├── uploads/               # Temporary storage for uploaded CVs
├── modified/              # Temporary storage for modified CVs
├── templates/
│   └── index.html         # Main web interface
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── main.js        # Frontend JavaScript
└── utils/
    ├── scraper.py         # Web scraping for job descriptions
    ├── doc_handler.py     # DOCX file reading/writing with formatting preservation
    └── gemini_service.py  # Google Gemini AI integration
```

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `FLASK_SECRET_KEY`: Secret key for Flask sessions (required for production)
- `FLASK_ENV`: Set to `production` for production deployment (optional)

### File Size Limits

- Maximum upload size: 16MB
- Supported formats: `.doc`, `.docx`

### PDF Conversion

The app converts DOCX to PDF for download. Requirements:
- **macOS**: Requires Microsoft Word or LibreOffice
- **Windows**: Requires Microsoft Word
- **Linux**: Requires LibreOffice

If PDF conversion fails, the app automatically falls back to DOCX format.

## 🎯 How It Works

1. **Scraping**: The app fetches and extracts job description text from the provided URL
2. **CV Parsing**: Your uploaded CV is read while preserving formatting
3. **AI Analysis**: Google Gemini analyzes both documents and identifies:
   - Key skills and requirements from the job description
   - Relevant experience in your CV
   - Keywords for ATS optimization
   - Areas for improvement
4. **CV Modification**: Gemini modifies your CV to:
   - Emphasize relevant skills and experience
   - Add industry-specific keywords
   - Enhance bullet points with action verbs
   - Maintain truthfulness (no false information added)
   - **Preserve original formatting** (fonts, colors, bold, links)
5. **Conversion**: Modified DOCX is converted to PDF
6. **Preview & Download**: Review changes and download the optimized PDF

## 🛡️ Important Notes

- **Truthfulness**: The AI is instructed to NEVER add false information. It only emphasizes and rephrases existing experience.
- **Formatting**: Your original CV formatting (fonts, colors, bold, hyperlinks) is preserved in the modified version.
- **Privacy**: Uploaded files are stored temporarily on the server. For production use, implement automatic cleanup.
- **API Costs**: Gemini has a free tier with generous limits. Check pricing at [Google AI Pricing](https://ai.google.dev/pricing).
- **Web Scraping**: May not work for all websites (especially those requiring authentication like LinkedIn login).

## 🐛 Troubleshooting

### "Error fetching URL"
- Ensure the URL is accessible and not behind a login wall
- Some sites block scraping - try a different job board
- Copy/paste the job description manually if needed

### "Error with Gemini API"
- Verify your API key is correct in `.env`
- Check if you have API quota remaining
- The app automatically detects available models

### "File upload errors"
- Ensure file is `.docx` or `.doc` format
- Check file size is under 16MB
- Make sure the file isn't password-protected

### "PDF conversion failed"
- **macOS**: Install Microsoft Word or LibreOffice (`brew install --cask libreoffice`)
- **Windows**: Install Microsoft Word
- **Linux**: Install LibreOffice (`sudo apt-get install libreoffice`)
- If conversion fails, you'll get a DOCX file (can manually convert to PDF)

## 🚀 Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
3. Set up reverse proxy (Nginx/Apache)
4. Use HTTPS
5. Implement file cleanup cron job for uploads/modified folders
6. Consider adding rate limiting and user authentication
7. Use Redis or database for session storage instead of in-memory

## 📝 License

This is a personal project. Feel free to modify and use as needed.

## 🤝 Contributing

This is an MVP (Minimal Viable Product). Potential improvements:
- Better diff visualization with highlighted changes
- Support for PDF input files
- Multiple CV templates
- Job description manual input option
- History of previous modifications
- Batch processing for multiple jobs
- Better formatting preservation for complex documents

## 📧 Support

For issues or questions, refer to:
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [INSTALL_STEPS.md](INSTALL_STEPS.md) - Detailed installation steps
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [python-docx Documentation](https://python-docx.readthedocs.io/)

---

**Built with**: Python, Flask, Google Gemini AI, Bootstrap 5

**Last Updated**: October 2026
