"""
Google Gemini AI service for CV modification
"""
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Track which models have hit quota limits (simple in-memory cache)
# Format: {model_name: timestamp_when_quota_hit}
quota_exceeded_models = {}

def is_quota_error(error_message):
    """
    Check if an error is related to quota/rate limits
    """
    error_str = str(error_message).lower()
    quota_keywords = [
        'quota',
        'rate limit',
        'exceeded',
        'too many requests',
        '429',
        'resource exhausted'
    ]
    return any(keyword in error_str for keyword in quota_keywords)

def is_model_available(model_name):
    """
    Check if a model is available (not in quota exceeded state)
    Returns True if model can be tried
    """
    if model_name not in quota_exceeded_models:
        return True
    
    # Check if enough time has passed since quota was hit (5 minutes)
    time_since_quota = time.time() - quota_exceeded_models[model_name]
    if time_since_quota > 300:  # 5 minutes
        # Remove from quota list and try again
        del quota_exceeded_models[model_name]
        return True
    
    return False

def get_available_models():
    """
    Get all available models that support content generation
    Returns list of model names, excluding those with quota issues
    """
    try:
        models = genai.list_models()
        available = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                if is_model_available(model.name):
                    available.append(model.name)
                    print(f"✓ Available model: {model.name}")
                else:
                    print(f"⏭ Skipping {model.name} (quota exceeded recently)")
        
        if not available:
            print("⚠ No models available - all may have quota issues")
        
        return available
    except Exception as e:
        print(f"Error listing models: {e}")
        return []

def modify_cv_with_gemini(cv_text, job_description):
    """
    Use Gemini AI to modify CV based on job description
    Returns: dict with modified_cv, match_score, and changes_summary
    
    Implements intelligent model fallback:
    - Tries multiple models in order of preference
    - Skips models that recently hit quota limits
    - Detects quota errors and rotates to next model
    """
    # Try different model names in order of preference (updated for 2025/2026)
    # Using current stable models as of January 2026
    model_names_to_try = [
        'gemini-2.5-flash',              # Stable - best price-performance
        'gemini-2.5-flash-lite',         # Fastest and most cost-efficient
        'gemini-2.5-pro',                # Advanced thinking model
        'gemini-3-flash-preview',        # Latest preview flash model
        'gemini-3-pro-preview',          # Most powerful (may have rate limits)
        'gemini-2.0-flash',              # Deprecated but still available until March 2026
    ]
    
    # Filter out models that have recently hit quota
    model_names_to_try = [m for m in model_names_to_try if is_model_available(m)]
    
    # Also try to get available models from API
    print("\n" + "="*60)
    print("🔍 Checking available Gemini models...")
    print("="*60)
    api_models = get_available_models()
    
    # Add API models to the front if not already in list
    for model in api_models:
        model_short = model.replace('models/', '')
        if model_short not in model_names_to_try:
            model_names_to_try.insert(0, model_short)
    
    if not model_names_to_try:
        raise Exception("❌ All models have hit quota limits. Please wait a few minutes and try again, or upgrade your API plan.")
    
    print(f"\n📋 Will try {len(model_names_to_try)} model(s) in order:")
    for i, model in enumerate(model_names_to_try, 1):
        print(f"  {i}. {model}")
    print()
    
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

ORIGINAL_MATCH_SCORE:
[A percentage from 0-100 indicating how well the ORIGINAL CV matches the job description]

MODIFIED_CV:
[The MODIFIED version of the original CV with enhanced descriptions]

MODIFIED_MATCH_SCORE:
[A percentage from 0-100 indicating how well the MODIFIED CV matches the job description]

CHANGES_SUMMARY:
[A bullet-point list of the specific changes you made to experience descriptions and why they improve the match]
"""
    
    last_error = None
    models_tried = 0
    
    # Try each model until one works
    for model_name in model_names_to_try:
        models_tried += 1
        try:
            print(f"🔄 Attempt {models_tried}/{len(model_names_to_try)}: Trying model '{model_name}'...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            
            # If we get here, the model worked!
            print(f"✅ SUCCESS! Used model: {model_name}")
            print("="*60 + "\n")
            response_text = response.text
            
            # Extract sections
            modified_cv = ""
            original_match_score = "N/A"
            modified_match_score = "N/A"
            changes_summary = ""
            
            # Parse ORIGINAL_MATCH_SCORE
            if "ORIGINAL_MATCH_SCORE:" in response_text:
                parts = response_text.split("ORIGINAL_MATCH_SCORE:")[1]
                if "MODIFIED_CV:" in parts:
                    original_match_score = parts.split("MODIFIED_CV:")[0].strip()
                    remaining = parts.split("MODIFIED_CV:")[1]
                    
                    # Parse MODIFIED_CV
                    if "MODIFIED_MATCH_SCORE:" in remaining:
                        modified_cv = remaining.split("MODIFIED_MATCH_SCORE:")[0].strip()
                        remaining2 = remaining.split("MODIFIED_MATCH_SCORE:")[1]
                        
                        # Parse MODIFIED_MATCH_SCORE
                        if "CHANGES_SUMMARY:" in remaining2:
                            modified_match_score = remaining2.split("CHANGES_SUMMARY:")[0].strip()
                            changes_summary = remaining2.split("CHANGES_SUMMARY:")[1].strip()
                        else:
                            modified_match_score = remaining2.strip()
                    else:
                        modified_cv = remaining.strip()
            else:
                # Fallback to old format for compatibility
                if "MODIFIED_CV:" in response_text:
                    parts = response_text.split("MODIFIED_CV:")[1]
                    if "MATCH_SCORE:" in parts:
                        modified_cv = parts.split("MATCH_SCORE:")[0].strip()
                        remaining = parts.split("MATCH_SCORE:")[1]
                        if "CHANGES_SUMMARY:" in remaining:
                            modified_match_score = remaining.split("CHANGES_SUMMARY:")[0].strip()
                            changes_summary = remaining.split("CHANGES_SUMMARY:")[1].strip()
                        else:
                            modified_match_score = remaining.strip()
                    else:
                        modified_cv = parts.strip()
                else:
                    # If format not followed, use the entire response as modified CV
                    modified_cv = response_text
            
            # Clean up match scores to extract just the numbers
            import re
            if original_match_score and original_match_score != "N/A":
                numbers = re.findall(r'\d+', original_match_score)
                if numbers:
                    original_match_score = numbers[0]
            
            if modified_match_score and modified_match_score != "N/A":
                numbers = re.findall(r'\d+', modified_match_score)
                if numbers:
                    modified_match_score = numbers[0]
            
            return {
                'modified_cv': modified_cv,
                'original_match_score': original_match_score,
                'modified_match_score': modified_match_score,
                'changes_summary': changes_summary if changes_summary else "CV optimized for job requirements with enhanced keywords and relevant experience highlighting."
            }
            
        except Exception as e:
            last_error = str(e)
            error_preview = str(e)[:150]
            
            # Check if this is a quota error
            if is_quota_error(str(e)):
                print(f"⚠️  QUOTA EXCEEDED for {model_name}")
                print(f"   Error: {error_preview}...")
                # Mark this model as having quota issues
                quota_exceeded_models[model_name] = time.time()
                print(f"   ⏭  Rotating to next available model...")
            else:
                print(f"❌ Model {model_name} failed: {error_preview}...")
            
            # Try next model
            if models_tried < len(model_names_to_try):
                print()  # Add spacing between attempts
            continue
    
    # If we got here, no model worked
    print("\n" + "="*60)
    print("❌ ALL MODELS FAILED")
    print("="*60)
    
    if quota_exceeded_models:
        print(f"\n⚠️  {len(quota_exceeded_models)} model(s) hit quota limits:")
        for model in quota_exceeded_models:
            print(f"   • {model}")
        print("\n💡 Solutions:")
        print("   1. Wait 5-10 minutes for quotas to reset")
        print("   2. Get a new API key at: https://aistudio.google.com/app/apikey")
        print("   3. Upgrade to a paid plan for higher limits")
    
    error_msg = f"Unable to find working Gemini model after trying {models_tried} models. Last error: {last_error}"
    print(f"\n{error_msg}\n")
    raise Exception(error_msg)

def test_gemini_connection():
    """
    Test if Gemini API is properly configured
    Tests all available models and returns the first working one
    """
    available_models = get_available_models()
    
    if not available_models:
        return False, "Could not find any available models"
    
    for model_name in available_models:
        try:
            print(f"Testing {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Connection successful' if you can read this.")
            return True, f"✅ Connection successful using {model_name}"
        except Exception as e:
            if is_quota_error(str(e)):
                quota_exceeded_models[model_name] = time.time()
                print(f"⚠️  {model_name} has quota issues, trying next...")
            else:
                print(f"❌ {model_name} failed: {str(e)[:100]}")
            continue
    
    return False, "All models failed. Check API key and quota limits."
