"""
Flask application for CVTailor
"""
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
import platform

# Import utility modules
from utils.scraper import extract_job_description, validate_url
from utils.doc_handler import read_docx, write_docx, validate_docx
from utils.gemini_service import modify_cv_with_gemini

# PDF conversion - platform dependent
try:
    if platform.system() == 'Darwin':  # macOS
        from docx2pdf import convert as docx2pdf_convert
    elif platform.system() == 'Windows':
        from docx2pdf import convert as docx2pdf_convert
    else:  # Linux - use LibreOffice
        docx2pdf_convert = None
except ImportError:
    docx2pdf_convert = None

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = 'uploads'
MODIFIED_FOLDER = 'modified'
ALLOWED_EXTENSIONS = {'docx', 'doc'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODIFIED_FOLDER'] = MODIFIED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODIFIED_FOLDER, exist_ok=True)

# Server-side session storage (in-memory for MVP)
# For production, use Redis or database
sessions_data = {}

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """Process CV and job description"""
    try:
        # Validate inputs
        if 'cv_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['cv_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .docx and .doc files are allowed'}), 400
        
        # Get job description either from URL or direct text
        job_url = request.form.get('job_url', '').strip()
        job_text = request.form.get('job_text', '').strip()
        
        # Validate that at least one is provided
        if not job_url and not job_text:
            return jsonify({'error': 'Please provide either a job URL or paste the job description'}), 400
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
        file.save(original_path)
        
        # Get job description
        job_description = None
        
        # Priority: Use pasted text if provided, otherwise scrape URL
        if job_text:
            job_description = job_text
        elif job_url:
            if not validate_url(job_url):
                return jsonify({'error': 'Invalid URL format'}), 400
            
            job_description = extract_job_description(job_url)
            if job_description.startswith('Error') or job_description.startswith('Unable'):
                return jsonify({'error': job_description}), 400
        
        # Ensure we have a job description
        if not job_description or len(job_description.strip()) < 50:
            return jsonify({'error': 'Job description is too short or empty. Please provide more details.'}), 400
        
        # Read CV content
        cv_text = read_docx(original_path)
        
        # Modify CV using Gemini
        result = modify_cv_with_gemini(cv_text, job_description)
        
        # Save modified CV with preserved formatting
        modified_filename = f"{session_id}_modified.docx"
        modified_path = os.path.join(app.config['MODIFIED_FOLDER'], modified_filename)
        write_docx(result['modified_cv'], modified_path, original_path)
        
        # Store data in server-side storage
        sessions_data[session_id] = {
            'original_cv': cv_text,
            'modified_cv': result['modified_cv'],
            'match_score': result['match_score'],
            'changes_summary': result['changes_summary'],
            'modified_filename': modified_filename,
            'original_filename': filename,
            'timestamp': datetime.now().isoformat()
        }
        
        # Return preview data
        return jsonify({
            'success': True,
            'session_id': session_id,
            'original_cv': cv_text,
            'modified_cv': result['modified_cv'],
            'match_score': result['match_score'],
            'changes_summary': result['changes_summary'],
            'job_description': job_description[:500] + '...' if len(job_description) > 500 else job_description
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/download/<session_id>')
def download(session_id):
    """Download modified CV as PDF"""
    try:
        if session_id not in sessions_data:
            return jsonify({'error': 'Session not found or expired'}), 404
        
        data = sessions_data[session_id]
        modified_filename = data['modified_filename']
        modified_path = os.path.join(app.config['MODIFIED_FOLDER'], modified_filename)
        
        if not os.path.exists(modified_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Convert DOCX to PDF
        pdf_filename = modified_filename.replace('.docx', '.pdf')
        pdf_path = os.path.join(app.config['MODIFIED_FOLDER'], pdf_filename)
        
        # Try to convert to PDF
        conversion_success = False
        error_messages = []
        
        # Method 1: Try docx2pdf (for macOS with Word)
        if docx2pdf_convert is not None:
            try:
                print(f"Trying docx2pdf conversion...")
                docx2pdf_convert(modified_path, pdf_path)
                if os.path.exists(pdf_path):
                    conversion_success = True
                    print("docx2pdf conversion successful!")
                else:
                    error_messages.append("docx2pdf did not create PDF file")
            except Exception as e:
                error_messages.append(f"docx2pdf failed: {str(e)}")
                print(f"docx2pdf conversion failed: {e}")
        
        # Method 2: Try LibreOffice command line (works on macOS now)
        if not conversion_success:
            try:
                import subprocess
                print(f"Trying LibreOffice conversion...")
                
                # Use absolute paths
                abs_modified_path = os.path.abspath(modified_path)
                abs_output_dir = os.path.abspath(app.config['MODIFIED_FOLDER'])
                print(f"Converting: {abs_modified_path}")
                print(f"Output dir: {abs_output_dir}")
                
                # Kill any existing soffice processes first
                subprocess.run(['pkill', '-9', 'soffice'], capture_output=True)
                
                # Run conversion with longer timeout and absolute paths
                result = subprocess.run(
                    ['/usr/local/bin/soffice', '--headless', '--convert-to', 'pdf', 
                     '--outdir', abs_output_dir, abs_modified_path],
                    capture_output=True,
                    text=True,
                    timeout=60,  # Increased timeout
                    cwd=abs_output_dir  # Set working directory
                )
                
                print(f"LibreOffice return code: {result.returncode}")
                print(f"LibreOffice stdout: {result.stdout}")
                print(f"LibreOffice stderr: {result.stderr}")
                
                # Check if PDF was created
                if result.returncode == 0:
                    # Wait a moment for file to be written
                    import time
                    time.sleep(1)
                    
                    if os.path.exists(pdf_path):
                        conversion_success = True
                        print("LibreOffice conversion successful!")
                    else:
                        error_messages.append(f"LibreOffice completed but PDF not found at {pdf_path}")
                else:
                    error_messages.append(f"LibreOffice failed with code {result.returncode}: {result.stderr}")
            except FileNotFoundError:
                error_messages.append("LibreOffice not found at /usr/local/bin/soffice")
                print("LibreOffice not found")
            except subprocess.TimeoutExpired:
                error_messages.append("LibreOffice conversion timed out (60s)")
                print("LibreOffice conversion timed out")
                # Kill the process
                subprocess.run(['pkill', '-9', 'soffice'], capture_output=True)
            except Exception as e:
                error_messages.append(f"LibreOffice error: {str(e)}")
                print(f"LibreOffice conversion failed: {e}")
        
        # Print all errors for debugging
        if not conversion_success:
            print(f"PDF conversion failed. Errors: {'; '.join(error_messages)}")
        
        # If PDF conversion failed, return DOCX instead
        if not conversion_success or not os.path.exists(pdf_path):
            original_name = data['original_filename']
            if original_name.lower().endswith('.docx'):
                download_name = original_name[:-5] + '_modified.docx'
            elif original_name.lower().endswith('.doc'):
                download_name = original_name[:-4] + '_modified.docx'
            else:
                download_name = original_name + '_modified.docx'
            
            response = send_file(
                modified_path,
                as_attachment=True,
                download_name=download_name,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            
            # Clean up files after successful download
            try:
                # Delete the session data
                if session_id in sessions_data:
                    del sessions_data[session_id]
                
                # Delete the files (in background to not delay response)
                import threading
                def cleanup_files():
                    try:
                        if os.path.exists(modified_path):
                            os.remove(modified_path)
                        # Also remove original uploaded file
                        original_filename = data.get('original_filename', '')
                        for file in os.listdir(app.config['UPLOAD_FOLDER']):
                            if file.endswith(original_filename):
                                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
                    except Exception as e:
                        print(f"Cleanup error: {e}")
                
                # Start cleanup in background thread
                threading.Thread(target=cleanup_files, daemon=True).start()
            except Exception as e:
                print(f"Error setting up cleanup: {e}")
            
            return response
        
        # Return PDF
        original_name = data['original_filename']
        if original_name.lower().endswith('.docx'):
            download_name = original_name[:-5] + '_modified.pdf'
        elif original_name.lower().endswith('.doc'):
            download_name = original_name[:-4] + '_modified.pdf'
        else:
            download_name = original_name + '_modified.pdf'
        
        response = send_file(
            pdf_path,
            as_attachment=True,
            download_name=download_name,
            mimetype='application/pdf'
        )
        
        # Clean up files after successful download
        try:
            # Delete the session data
            if session_id in sessions_data:
                del sessions_data[session_id]
            
            # Delete the files (in background to not delay response)
            import threading
            def cleanup_files():
                try:
                    if os.path.exists(modified_path):
                        os.remove(modified_path)
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                    # Also remove original uploaded file
                    original_filename = data.get('original_filename', '')
                    for file in os.listdir(app.config['UPLOAD_FOLDER']):
                        if file.endswith(original_filename):
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
                except Exception as e:
                    print(f"Cleanup error: {e}")
            
            # Start cleanup in background thread
            threading.Thread(target=cleanup_files, daemon=True).start()
        except Exception as e:
            print(f"Error setting up cleanup: {e}")
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'CVTailor is running'})

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

if __name__ == '__main__':
    app.run(debug=True, port=5001)
