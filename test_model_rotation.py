#!/usr/bin/env python3
"""
Demonstration of intelligent model rotation and quota handling
This script shows how CVTailor now automatically handles quota limits
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("="*70)
print(" CVTailor - Intelligent Model Rotation Demo")
print("="*70)
print()

# Check API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    print("\n💡 Solution:")
    print("   1. Copy .env.example to .env")
    print("   2. Add your API key from: https://aistudio.google.com/app/apikey")
    exit(1)

print(f"✓ API Key loaded: {api_key[:10]}...{api_key[-4:]}")
print()

# Import after checking API key
from utils.gemini_service import modify_cv_with_gemini, quota_exceeded_models

# Sample CV and job description for testing
sample_cv = """
JOHN DOE
Software Engineer
john.doe@email.com | (555) 123-4567

EXPERIENCE
Software Engineer at Tech Corp (2020-2023)
- Developed web applications
- Worked with databases
- Collaborated with team members

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2020

SKILLS
Python, JavaScript, SQL, Git
"""

sample_job = """
Senior Software Engineer
We're looking for a skilled engineer with experience in:
- Python and Django
- RESTful APIs
- Cloud platforms (AWS/GCP)
- Team leadership
"""

print("="*70)
print(" Testing Model Rotation with Sample CV")
print("="*70)
print()
print("📄 Sample CV: Software Engineer with 3 years experience")
print("🎯 Target Job: Senior Software Engineer (Python/Django/Cloud)")
print()
print("This will demonstrate:")
print("  • Checking multiple models")
print("  • Detecting quota limits")
print("  • Automatic model rotation")
print("  • Success with fallback models")
print()
input("Press ENTER to start the test...")
print()

try:
    result = modify_cv_with_gemini(sample_cv, sample_job)
    
    print("="*70)
    print("✅ SUCCESS - CV MODIFICATION COMPLETED")
    print("="*70)
    print()
    print(f"📊 Original Match Score: {result['original_match_score']}%")
    print(f"📈 Modified Match Score: {result['modified_match_score']}%")
    print(f"🎯 Improvement: {int(result['modified_match_score']) - int(result['original_match_score'])}%")
    print()
    print("📝 Changes Summary:")
    print("-" * 70)
    print(result['changes_summary'])
    print()
    print("="*70)
    print("🎉 Model rotation working successfully!")
    print("="*70)
    print()
    
    if quota_exceeded_models:
        print("⚠️  Models with quota issues:")
        for model in quota_exceeded_models:
            print(f"   • {model}")
        print()
        print("💡 These models will be retried after 5 minutes")
    else:
        print("✅ No quota issues encountered")
    
except Exception as e:
    print("="*70)
    print("❌ TEST FAILED")
    print("="*70)
    print()
    print(f"Error: {str(e)}")
    print()
    
    if "API key expired" in str(e) or "API_KEY_INVALID" in str(e):
        print("🔑 Your API key has expired or is invalid")
        print()
        print("💡 Solution:")
        print("   1. Visit: https://aistudio.google.com/app/apikey")
        print("   2. Generate a new API key")
        print("   3. Update your .env file:")
        print("      GEMINI_API_KEY=your_new_key_here")
    elif "quota" in str(e).lower():
        print("📊 All models have hit their quota limits")
        print()
        print("💡 Solutions:")
        print("   1. Wait 5-10 minutes for quotas to reset")
        print("   2. Get a new API key (separate quota)")
        print("   3. Upgrade to a paid plan for higher limits")
    
    print()

print()
print("="*70)
print(" Test Complete")
print("="*70)
