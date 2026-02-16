# Gemini API Setup Guide

## Current Status ✅

The code has been updated successfully! The model names are now correct:
- ✅ Found working model: `models/gemini-2.5-flash`
- ✅ Code updated to use latest Gemini 2.5/3.0 models

## Issues Found 🔴

### 1. API Key Expired
**Error:** `400 API key expired. Please renew the API key.`

**Solution:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Generate a new API key
4. Update your `.env` file with the new key:
   ```
   GEMINI_API_KEY=your_new_api_key_here
   ```

### 2. Free Tier Quota Exceeded
**Error:** `429 You exceeded your current quota (20 requests per day)`

**Solution Options:**

#### Option A: Wait for Quota Reset
- Free tier: 20 requests per day per model
- Your quota will reset in ~13 seconds (or at daily reset time)
- Wait and try again later

#### Option B: Upgrade Your Plan
- Visit [Google AI Studio](https://aistudio.google.com/)
- Consider upgrading to a paid plan for higher quotas
- Paid tiers offer significantly higher limits

#### Option C: Use Multiple Models (Load Balancing) ✅ IMPLEMENTED
**This is now automatically enabled!** The system intelligently rotates between models:

**How it works:**
1. 🔍 Checks all available models from the API
2. 🚫 Skips models that recently hit quota limits
3. 🔄 Tries models in order of preference
4. ⚠️  Detects quota errors automatically
5. ⏭  Rotates to the next available model
6. 💾 Remembers which models have quota issues for 5 minutes

**Models tried in order:**
  - `gemini-2.5-flash` (best price-performance)
  - `gemini-2.5-flash-lite` (most cost-efficient)
  - `gemini-2.5-pro` (advanced thinking)
  - `gemini-3-flash-preview` (latest preview)
  - `gemini-3-pro-preview` (most powerful)
  - `gemini-2.0-flash` (fallback, deprecated)

**Benefits:**
- ✅ Maximizes your free tier usage across all models
- ✅ Automatically handles quota limits
- ✅ Provides clear logging of which model succeeded
- ✅ No manual intervention required

## Testing Your Setup

After updating your API key, run:
```bash
python3 test_gemini.py
```

Or test the full application:
```bash
python3 app.py
```

Then visit: http://localhost:5000

## Rate Limits (Free Tier)

| Model | Requests/Day | Requests/Minute |
|-------|--------------|-----------------|
| gemini-2.5-flash | 20 | 2 |
| gemini-2.5-pro | 10 | 2 |
| gemini-3-flash-preview | Variable | Variable |

## What Was Fixed

### ✅ Updated Model Names
- ❌ OLD: `gemini-pro`, `gemini-1.5-flash`, `gemini-1.5-pro`
- ✅ NEW: `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-3-flash-preview`

### ✅ Intelligent Model Rotation (Load Balancing)
- 🔄 Automatically tries multiple models in sequence
- 🎯 Detects quota errors and rotates to next model
- 💾 Tracks which models hit quota (5-minute memory)
- 📊 Provides detailed logging of model attempts
- ⚡ Maximizes usage across all available models

### ✅ Enhanced Error Handling
- Clear error messages with actionable solutions
- Quota detection and automatic model switching
- Better logging for debugging

### ✅ Updated Documentation
- API key URL: https://aistudio.google.com/app/apikey
- Clear setup instructions
- Quota limit information

## Need Help?

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Rate Limits Info](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Get API Key](https://aistudio.google.com/app/apikey)
