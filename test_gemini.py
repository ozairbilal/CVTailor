#!/usr/bin/env python3
"""
Test script to verify Gemini API connection
"""
from utils.gemini_service import test_gemini_connection, get_available_model
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Testing Gemini API Connection")
print("=" * 60)

# Check if API key is set
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

print(f"✓ API Key found: {api_key[:10]}...{api_key[-4:]}")
print()

# Configure API
genai.configure(api_key=api_key)

# List all available models
print("Listing all available models...")
print("-" * 60)
try:
    models = genai.list_models()
    model_count = 0
    generate_content_models = []
    
    for model in models:
        model_count += 1
        if 'generateContent' in model.supported_generation_methods:
            generate_content_models.append(model.name)
            print(f"✓ {model.name}")
            print(f"  Supported methods: {', '.join(model.supported_generation_methods)}")
    
    print()
    print(f"Total models found: {model_count}")
    print(f"Models supporting generateContent: {len(generate_content_models)}")
    print()
    
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print()

# Test connection using the helper function
print("-" * 60)
print("Testing connection with test_gemini_connection()...")
print("-" * 60)
success, message = test_gemini_connection()

if success:
    print(f"✓ {message}")
else:
    print(f"❌ {message}")

print()
print("=" * 60)
print("Test complete!")
print("=" * 60)
