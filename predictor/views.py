
# views.py - ML Model Integration

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import joblib
import numpy as np
from django.conf import settings
from typing import Tuple
import os
from dotenv import load_dotenv
import google.generativeai as genai

# load .env first
load_dotenv()   # loads .env in project root

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    # fail fast with a clear message (useful in dev)
    print("ERROR: GEMINI_API_KEY is not set in environment (.env missing or key not present).")
else:
    # configure once
    genai.configure(api_key=GEMINI_API_KEY)


try:
    #Using a model that is present in the list of available models
    gemini_model = genai.GenerativeModel("gemini-flash-latest")
    response = gemini_model.generate_content("Write a motivational quote and tips for students.")
    # response object may differ by SDK versions; try these:
    print(getattr(response, "text", None) or response or "No text returned")
except Exception as e:
    print(f"Error loading Gemini: {e}")
    gemini_model = None


def landing_page(request):
    return render(request, 'predictor/landing.html')

def survey_page(request):
    return render(request, 'predictor/survey.html')

def chat_page(request):
    return render(request, 'predictor/chat.html')


        
# Load your ML model (do this once when Django starts)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'predictor', 'ml_model', 'trained_model.joblib')

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None


# inside views.py (replace your existing stress_predictor_view with the following)

def stress_predictor_view(request):
    """Main view for the stress predictor page"""
    context = {}

    # If GET, just render the form page
    if request.method == 'GET':
        return render(request, 'predictor/survey.html', context)

    # Handle POST (form submit)
    if request.method == 'POST':
        try:
            # --- Input parsing (keep same order as training features) ---
            gender = 1 if request.POST.get('gender') == 'Male' else 0
            age = int(request.POST.get('age') or 0)

            features = [
                gender,
                age,
                int(request.POST.get('stress_life') or 1),
                int(request.POST.get('heartbeat') or 1),
                int(request.POST.get('anxiety') or 1),
                int(request.POST.get('sleep') or 1),
                int(request.POST.get('concentration_general') or 1),
                int(request.POST.get('headaches') or 1),
                int(request.POST.get('irritation') or 1),
                int(request.POST.get('concentration_academic') or 1),
                int(request.POST.get('sadness') or 1),
                int(request.POST.get('illness') or 1),
                int(request.POST.get('lonely') or 1),
                int(request.POST.get('workload') or 1),
                int(request.POST.get('competition') or 1),
                int(request.POST.get('relationship') or 1),
                int(request.POST.get('professor_difficulty') or 1),
                int(request.POST.get('work_environment') or 1),
                int(request.POST.get('relaxation_time') or 1),
                int(request.POST.get('home_environment') or 1),
                int(request.POST.get('confidence_performance') or 1),
                int(request.POST.get('confidence_subjects') or 1),
                int(request.POST.get('activities_conflict') or 1),
                int(request.POST.get('class_attendance') or 5),
                int(request.POST.get('weight_change') or 1)
            ]

            # Convert to numpy array for model
            features_array = np.array(features).reshape(1, -1)

            if model is None:
                # Model not loaded
                context.update({
                    'error': True,
                    'message': 'ML model not loaded. Check server logs for details.'
                })
                return render(request, 'predictor/survey.html', context)

            # --- Prediction ---
            prediction_raw = model.predict(features_array)
            # sometimes predict returns array, sometimes single value
            prediction = int(prediction_raw[0]) if hasattr(prediction_raw, '__iter__') else int(prediction_raw)

            # Try to get probability / confidence
            confidence = None
            try:
                probs = model.predict_proba(features_array)[0]
                confidence = float(max(probs) * 100)
            except Exception:
                # model may not support predict_proba
                confidence = None

            # --- Map numeric labels to human-friendly results ---
            # IMPORTANT: Ensure these numeric keys (0,1,2) match how you trained your model.
            stress_types = {
                0: {
                    'name': 'Distress (Negative Stress)',
                    'description': 'You are experiencing negative stress that may impair your well-being.',
                    'class': 'distress',
                    'icon': '⚠️'
                },
                1: {
                    'name': 'Eustress (Positive Stress)',
                    'description': 'You are experiencing positive stress that can motivate and enhance your performance.',
                    'class': 'eustress',
                    'icon': '✨'
                },
                2: {
                    'name': 'No Stress',
                    'description': 'You are currently experiencing minimal to no stress. Keep it up!',
                    'class': 'no-stress',
                    'icon': '😊'
                }
            }

            # Fallback: if prediction label not in dict, treat as distress
            stress_result = stress_types.get(prediction, stress_types[0])

            # Simple tailored recommendations (customize as needed)
            recommendations_map = {
                'distress': [
                    "Talk to a counsellor or trusted friend.",
                    "Prioritise sleep and short breaks during study sessions.",
                    "Try breathing exercises or brief walks to reduce anxiety."
                ],
                'eustress': [
                    "Channel your energy into structured goals.",
                    "Keep a balanced schedule to avoid burnout.",
                    "Use short relaxation routines to recover."
                ],
                'no-stress': [
                    "Maintain healthy routines that work for you.",
                    "Keep stress-management habits to stay balanced.",
                    "Support peers who may be stressed."
                ]
            }

            recs = recommendations_map.get(stress_result['class'], [])

            # Build context to send to template
            context.update({
                'result': True,
                'prediction': prediction,
                'stress_type': stress_result['name'],
                'description': stress_result['description'],
                'stress_class': stress_result['class'],
                'icon': stress_result['icon'],
                'confidence': confidence,
                'recommendations': recs
            })

            # Optional: print debug info to server console (check runserver logs)
            print("DEBUG: features =", features)
            print("DEBUG: prediction =", prediction, "confidence =", confidence)

            return render(request, 'predictor/survey.html', context)

        except Exception as e:
            # Catch-all error -> show on template
            err_msg = f"An error occurred while predicting: {e}"
            print("ERROR in stress_predictor_view:", err_msg)
            context.update({
                'error': True,
                'message': err_msg
            })
            return render(request, 'predictor/survey.html', context)

    # Default fallback
    return render(request, 'predictor/survey.html', context)
 


MODEL_NAME = "gemini-pro-latest"   # change to gemini-2.5-pro etc if you prefer

def _extract_text_from_response(resp) -> str:
    """
    Robust extractor because SDK responses can differ between versions.
    """
    if resp is None:
        return ""
    # try common attributes in order
    for attr in ("text", "output", "outputs", "candidates", "content"):
        val = getattr(resp, attr, None)
        if val:
            # outputs/ output might be a list of objects/dicts
            try:
                if isinstance(val, str):
                    return val
                # if it's a list, try to find first string content field
                if isinstance(val, (list, tuple)) and len(val) > 0:
                    first = val[0]
                    # if object with .text or .content
                    if hasattr(first, "text"):
                        return first.text
                    if hasattr(first, "content"):
                        return first.content
                    if isinstance(first, dict):
                        # common nested structures
                        for key in ("text","content","message","output"):
                            if key in first and isinstance(first[key], str):
                                return first[key]
                        # if candidates list inside
                        if "candidates" in first and isinstance(first["candidates"], list) and first["candidates"]:
                            cand = first["candidates"][0]
                            if isinstance(cand, str):
                                return cand
                            if isinstance(cand, dict) and "content" in cand:
                                return cand["content"]
                # if it's an object with a .text attr and that attr is string
                if hasattr(val, "text") and isinstance(val.text, str):
                    return val.text
                if isinstance(val, dict) and "text" in val and isinstance(val["text"], str):
                    return val["text"]
            except Exception:
                continue
    # fallback to stringifying response
    try:
        return str(resp)
    except Exception:
        return ""

def get_gemini_response(user_message: str, stress_type: str | None = None) -> Tuple[bool, str]:
    """
    Calls Gemini to get a reply for the chatbot.
    Returns tuple (ok: bool, text_or_error: str).
    """
    if not user_message:
        return False, "No prompt provided."

    # Compose a system-style prompt that gives the assistant context
    context = ("You are StressLess, a friendly and empathetic AI stress management assistant. "
               "You speak warmly and briefly, offering emotional support and general stress-coping suggestions. "
               "Avoid giving medical diagnoses. Encourage positivity and self-care.")
    prompt = f"{context}\n\nUser says: {user_message}"
    if stress_type:
        prompt += f"\n\nDetected stress type: {stress_type}"

    try:
        # Create model instance and call generate_content
        model = genai.GenerativeModel(MODEL_NAME)
        resp = model.generate_content(prompt)
        text = _extract_text_from_response(resp)
        if not text:
            return False, "No text returned from Gemini."
        return True, text.strip()
    except Exception as e:
        # include the exception string for debugging — you may want to log it instead
        return False, f"Gemini error: {e}"


@csrf_exempt
def chat_api(request):
    """API endpoint for Gemini AI chatbot"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            stress_type = data.get('stress_type', None)
            
            print(f"=== CHATBOT DEBUG ===")
            print(f"User message: {user_message}")
            print(f"Stress type: {stress_type}")
            print(f"Gemini model loaded: {gemini_model is not None}")
            
            # Get AI response from Gemini
            response = get_gemini_response(user_message, stress_type)
            
            print(f"Response: {response[:100]}...")
            print(f"=== END DEBUG ===")
            
            return JsonResponse({
                'success': True,
                'response': response
            })
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

#def get_chatbot_response(user_message, stress_type=None):
    """
    Personalized chatbot responses based on stress type
    stress_type: 0 = Distress, 1 = Eustress, 2 = No Stress
    """
    message_lower = user_message.lower()
    
    # Greeting
    if any(word in message_lower for word in ['hi', 'hello', 'hey']):
        if stress_type == 0:
            return ("Hello! I understand you're experiencing distress. I'm here to help you with "
                    "coping strategies, relaxation techniques, and support. What would you like to talk about?")
        elif stress_type == 1:
            return ("Hi! It's great that you're experiencing positive stress! I can help you maintain "
                    "this momentum and prevent burnout. What can I help you with?")
        else:
            return ("Hello! I'm your stress management assistant. I can provide tips on maintaining "
                    "balance, study strategies, and wellness advice. How can I help?")
    
    # Distress-specific responses
    if stress_type == 0 or any(word in message_lower for word in ['anxious', 'overwhelmed', 'depressed', 'sad']):
        if 'breathing' in message_lower or 'breath' in message_lower:
            return ("Let's try the 4-7-8 breathing technique: 1) Breathe in through nose for 4 counts, "
                    "2) Hold for 7 counts, 3) Exhale through mouth for 8 counts. Repeat 4 times. "
                    "This activates your relaxation response. How do you feel?")
        
        if 'sleep' in message_lower or 'insomnia' in message_lower:
            return ("Sleep is crucial for managing distress. Try: 1) Go to bed same time daily, "
                    "2) No screens 1 hour before bed, 3) Keep room cool & dark, 4) Try progressive "
                    "muscle relaxation. Avoid caffeine after 2 PM. Need more specific tips?")
        
        if 'study' in message_lower or 'focus' in message_lower:
            return ("When stressed, concentration suffers. Try: 1) Study in 25-min blocks (Pomodoro), "
                    "2) Remove distractions, 3) Start with easiest task, 4) Use active recall. "
                    "Break large tasks into tiny steps. Which subject is challenging you?")
        
        if 'help' in message_lower or 'counselor' in message_lower:
            return ("Seeking help is a sign of strength! Contact: 1) Your university counseling center, "
                    "2) Student support services, 3) National helpline: 1-800-273-8255 (US), "
                    "4) Online therapy platforms. Would you like more resources?")
        
        return ("I hear that you're struggling. Remember: 1) You're not alone, 2) This feeling is temporary, "
                "3) Small steps matter. Try: deep breathing, talking to someone, or a short walk. "
                "What specific challenge can I help with?")
    
    # Eustress-specific responses
    if stress_type == 1 or any(word in message_lower for word in ['motivated', 'productive', 'busy']):
        if 'burnout' in message_lower or 'tired' in message_lower:
            return ("Even positive stress can lead to burnout! Warning signs: fatigue, irritability, "
                    "decreased performance. Prevent it: 1) Schedule rest days, 2) Say no to extra commitments, "
                    "3) Sleep 7-8 hours, 4) Take real breaks. What's your current schedule like?")
        
        if 'balance' in message_lower:
            return ("Great question! Balance tips: 1) Use time-blocking, 2) Set boundaries (study/social time), "
                    "3) Plan 1 fun activity weekly, 4) Practice saying 'no'. Remember: rest is productive! "
                    "What area needs more balance?")
        
        return ("You're doing well! To maintain positive stress: 1) Keep realistic goals, 2) Celebrate wins, "
                "3) Rest is part of productivity, 4) Connect with others. What's working well for you?")
    
    # No stress responses
    if stress_type == 2:
        return ("That's wonderful! To maintain this: 1) Keep your healthy routines, 2) Build stress "
                "resilience through exercise & mindfulness, 3) Support stressed friends. "
                "Want to learn preventive techniques?")
    
    # Topic-specific responses
    if 'exercise' in message_lower or 'workout' in message_lower:
        return ("Exercise is powerful for stress! Benefits: reduces cortisol, boosts endorphins, improves sleep. "
                "Try: 1) 30-min daily walk, 2) Yoga (YouTube has free videos), 3) Dancing, 4) Any activity you enjoy. "
                "Even 10 minutes helps! What activities interest you?")
    
    if 'exam' in message_lower or 'test' in message_lower:
        return ("Exam stress is common! Tips: 1) Start studying early (no cramming), 2) Practice past papers, "
                "3) Study groups can help, 4) Sleep well before exam, 5) Arrive early to feel settled. "
                "Before exam: deep breaths, positive self-talk. Which exam is coming up?")
    
    if 'relationship' in message_lower or 'friends' in message_lower:
        return ("Relationships affect stress! Healthy habits: 1) Communicate openly, 2) Set boundaries, "
                "3) Spend time with supportive people, 4) It's okay to distance from toxic relationships. "
                "Good friends reduce stress! What's on your mind?")
    
    if 'time management' in message_lower or 'procrastination' in message_lower:
        return ("Time management reduces stress! Try: 1) Priority matrix (urgent/important), "
                "2) Time-blocking your day, 3) Two-minute rule: if <2 min, do it now, "
                "4) Break tasks into 15-min chunks. Use apps like Forest or Notion. What's your biggest time challenge?")
    
    # Default response
    return ("I'm here to help with stress management! I can provide tips on: relaxation techniques, "
            "study strategies, sleep improvement, exercise, time management, exam preparation, and more. "
            "What would you like to explore?")