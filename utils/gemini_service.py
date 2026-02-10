"""
Google Gemini AI service for CV modification
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def get_available_model():
    """
    Get the first available model that supports content generation
    """
    try:
        models = genai.list_models()
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                return model.name
        return None
    except Exception as e:
        print(f"Error listing models: {e}")
        return None

def modify_cv_with_gemini(cv_text, job_description):
    """
    Use Gemini AI to modify CV based on job description
    Returns: dict with modified_cv, match_score, and changes_summary
    """
    # Try different model names in order of preference
    model_names_to_try = [
        'gemini-1.5-flash-latest',
        'gemini-1.5-flash',
        'gemini-1.5-pro-latest',
        'gemini-1.5-pro',
        'gemini-pro',
        'models/gemini-1.5-flash-latest',
        'models/gemini-1.5-flash',
        'models/gemini-pro'
    ]
    
    # Also try to get available models from API
    available_model = get_available_model()
    if available_model:
        model_names_to_try.insert(0, available_model)
    
    prompt = f"""You are an expert CV/resume optimizer. Your task is to MODIFY the existing CV (not create a new one) to better match the job description while maintaining the original structure and truthfulness.

JOB DESCRIPTION:
{job_description}

ORIGINAL CV:
{cv_text}

CRITICAL INSTRUCTIONS:
1. KEEP the EXACT same CV structure, format, and all sections as the original
2. KEEP all dates, company names, job titles, education details, contact information EXACTLY as they appear
3. PRESERVE the exact formatting - if something is in ALL CAPS, keep it in ALL CAPS
4. PRESERVE all section headers, bullet points, and line breaks exactly as they are
5. ONLY modify the content of experience descriptions/bullet points to:
   - Add relevant keywords from the job description
   - Emphasize skills and achievements that match the job requirements
   - Reword descriptions to highlight relevant experience
   - Use action verbs and quantifiable achievements where applicable
6. DO NOT add any false information, fake companies, or experiences that don't exist
7. DO NOT change the overall structure - every section, every job, every line should stay in the same order
8. Copy the CV structure EXACTLY, changing ONLY the wording of experience descriptions

EXAMPLE of what to do:
Original: "Developed web applications using Python"
Modified: "Developed scalable web applications using Python, Django, and RESTful APIs, serving 10K+ users"

EXAMPLE of what NOT to do:
❌ Don't add: "Led a team of 10 developers" if they were solo
❌ Don't change: "Software Engineer at XYZ Corp" to "Senior Software Engineer"
❌ Don't remove existing sections and create new ones

Please provide your response in the following format:

MODIFIED_CV:
[The MODIFIED version of the original CV with enhanced descriptions]

MATCH_SCORE:
[A percentage from 0-100 indicating how well the modified CV matches the job description]

CHANGES_SUMMARY:
[A bullet-point list of the specific changes you made to experience descriptions and why they improve the match]
"""
    
    last_error = None
    
    # Try each model until one works
    for model_name in model_names_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            
            # If we get here, the model worked!
            response_text = response.text
            
            # Extract sections
            modified_cv = ""
            match_score = "N/A"
            changes_summary = ""
            
            if "MODIFIED_CV:" in response_text:
                parts = response_text.split("MODIFIED_CV:")[1]
                if "MATCH_SCORE:" in parts:
                    modified_cv = parts.split("MATCH_SCORE:")[0].strip()
                    remaining = parts.split("MATCH_SCORE:")[1]
                    if "CHANGES_SUMMARY:" in remaining:
                        match_score = remaining.split("CHANGES_SUMMARY:")[0].strip()
                        changes_summary = remaining.split("CHANGES_SUMMARY:")[1].strip()
                    else:
                        match_score = remaining.strip()
                else:
                    modified_cv = parts.strip()
            else:
                # If format not followed, use the entire response as modified CV
                modified_cv = response_text
            
            # Clean up match score to extract just the number
            if match_score and match_score != "N/A":
                import re
                numbers = re.findall(r'\d+', match_score)
                if numbers:
                    match_score = numbers[0] + "%"
            
            return {
                'modified_cv': modified_cv,
                'match_score': match_score,
                'changes_summary': changes_summary if changes_summary else "CV optimized for job requirements with enhanced keywords and relevant experience highlighting."
            }
            
        except Exception as e:
            last_error = str(e)
            continue  # Try next model
    
    # If we got here, no model worked
    raise Exception(f"Unable to find working Gemini model. Last error: {last_error}. Please check your API key at https://makersuite.google.com/app/apikey")

def test_gemini_connection():
    """
    Test if Gemini API is properly configured
    """
    model_name = get_available_model()
    if not model_name:
        return False, "Could not find any available models"
    
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Connection successful' if you can read this.")
        return True, f"Connection successful using {model_name}"
    except Exception as e:
        return False, str(e)
