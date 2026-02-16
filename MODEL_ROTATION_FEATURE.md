# Intelligent Model Rotation Feature

## ✅ Implementation Complete

CVTailor now includes **intelligent model rotation** to maximize your free tier usage and automatically handle quota limits!

## 🎯 What It Does

The system automatically:

1. **Queries available models** from the Gemini API
2. **Tracks quota status** for each model (5-minute memory)
3. **Detects quota errors** automatically (429, "exceeded", etc.)
4. **Rotates to next model** when one hits its limit
5. **Provides clear logging** so you know which model succeeded

## 🔄 How It Works

```
User uploads CV + Job Description
         ↓
[Check Available Models]
         ↓
Try gemini-2.5-flash
  ├─ Success? ✅ Return result
  └─ Quota exceeded? ⚠️
         ↓
Try gemini-2.5-flash-lite
  ├─ Success? ✅ Return result
  └─ Quota exceeded? ⚠️
         ↓
Try gemini-2.5-pro
  ├─ Success? ✅ Return result
  └─ Quota exceeded? ⚠️
         ↓
Try gemini-3-flash-preview
  └─ Continue until success or all models exhausted
```

## 📊 Model Priority Order

1. **gemini-2.5-flash** - Best price-performance (20 requests/day)
2. **gemini-2.5-flash-lite** - Fastest, most cost-efficient (20 requests/day)
3. **gemini-2.5-pro** - Advanced thinking (10 requests/day)
4. **gemini-3-flash-preview** - Latest preview
5. **gemini-3-pro-preview** - Most powerful
6. **gemini-2.0-flash** - Fallback (deprecated March 2026)

**Total potential free tier usage:** 50+ requests/day across all models!

## 💡 Key Features

### Quota Tracking
- Remembers which models hit quota for 5 minutes
- Skips known-quota-exceeded models automatically
- Retries models after cooldown period

### Smart Error Detection
```python
def is_quota_error(error_message):
    quota_keywords = [
        'quota', 'rate limit', 'exceeded',
        'too many requests', '429', 'resource exhausted'
    ]
    return any(keyword in error_str for keyword in quota_keywords)
```

### Detailed Logging
```
============================================================
🔍 Checking available Gemini models...
============================================================
✓ Available model: models/gemini-2.5-flash
✓ Available model: models/gemini-2.5-flash-lite
✓ Available model: models/gemini-2.5-pro

📋 Will try 6 model(s) in order:
  1. gemini-2.5-flash
  2. gemini-2.5-flash-lite
  3. gemini-2.5-pro
  4. gemini-3-flash-preview
  5. gemini-3-pro-preview
  6. gemini-2.0-flash

🔄 Attempt 1/6: Trying model 'gemini-2.5-flash'...
⚠️  QUOTA EXCEEDED for gemini-2.5-flash
   ⏭  Rotating to next available model...

🔄 Attempt 2/6: Trying model 'gemini-2.5-flash-lite'...
✅ SUCCESS! Used model: gemini-2.5-flash-lite
============================================================
```

## 🧪 Testing

### Basic Test
```bash
python3 test_gemini.py
```

### Model Rotation Demo
```bash
python3 test_model_rotation.py
```

### Full Application Test
```bash
python3 app.py
# Visit http://localhost:5000
```

## 📈 Benefits

| Before | After |
|--------|-------|
| ❌ Single model (20 req/day) | ✅ Multiple models (50+ req/day) |
| ❌ Manual model switching | ✅ Automatic rotation |
| ❌ Cryptic error messages | ✅ Clear, actionable errors |
| ❌ No quota tracking | ✅ Smart quota memory |

## 🚀 Usage

No code changes needed! Just use CVTailor normally:

1. Upload your CV
2. Paste job description
3. Click "Tailor My CV"
4. System handles everything automatically

## 📝 Code Changes

All changes are in `utils/gemini_service.py`:

- Added `quota_exceeded_models` dictionary for tracking
- Added `is_quota_error()` function
- Added `is_model_available()` function
- Enhanced `get_available_models()` (formerly `get_available_model()`)
- Improved `modify_cv_with_gemini()` with rotation logic
- Enhanced `test_gemini_connection()` with multi-model testing

## 🔧 Configuration

No configuration needed! The system:
- Auto-detects available models
- Uses optimal fallback order
- Tracks quota automatically
- Provides helpful error messages

## 📚 Documentation

- **Setup Guide**: See `GEMINI_API_SETUP.md`
- **Main README**: See `README.md`
- **This Feature**: You're reading it!

## 🎉 Result

Your CVTailor application is now much more robust and can handle quota limits gracefully by automatically rotating between multiple Gemini models. This maximizes your free tier usage and provides a better user experience!
