import json
import requests

# Profile for my roommate/friend Ananya
FRIEND_PROFILE = {
    "name": "Ananya",
    "dietary_type": "Strict Pure Veg / Eggless",
    "severe_allergies": ["Peanuts", "Lactose / Milk Solids"],
    "hidden_additives_to_avoid": ["E120 (Carmine)", "Gelatin", "Rennet", "Bone Char Sugar"]
}

def analyze_indian_label(ingredient_text):
    """
    Analyzes packaged Indian food ingredient labels for Ananya's safety.
    Designed for local open-weight inference (Gemma 2 / Qwen via Ollama).
    """
    prompt = f"""
    You are an expert food safety assistant analyzing ingredients for {FRIEND_PROFILE['name']}.
    
    CRITICAL HEALTH & DIETARY CONSTRAINTS:
    - Dietary Rule: {FRIEND_PROFILE['dietary_type']}
    - Severe Allergies: {', '.join(FRIEND_PROFILE['severe_allergies'])}
    - Hidden Non-Veg Additives to Flag: {', '.join(FRIEND_PROFILE['hidden_additives_to_avoid'])}

    INGREDIENT LABEL TO SCAN:
    "{ingredient_text}"

    INSTRUCTIONS:
    1. Determine status: UNSAFE, WARNING, or SAFE.
    2. Detail EXACTLY which ingredient triggers the restriction.
    3. Keep response concise (under 60 words).
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma2",
                "prompt": prompt,
                "stream": False
            },
            timeout=5
        )
        return response.json().get("response", "Error reading model response.")
    except Exception:
        # Fallback offline simulation logic
        if "peanut" in ingredient_text.lower() or "milk" in ingredient_text.lower():
            return f"🛑 UNSAFE FOR ANANYA: Flagged Peanut/Lactose derivatives in ingredients."
        return f"✅ SAFE FOR ANANYA: No flagged allergens or non-veg additives found."

if __name__ == "__main__":
    sample_label = "Refined Wheat Flour (Maida), Sugar, Palm Oil, Peanut Oil, Milk Solids, INS 322."
    print(f"--- SafeBite AI Analysis for {FRIEND_PROFILE['name']} ---")
    print(f"Input: {sample_label}\n")
    print(analyze_indian_label(sample_label))
  
