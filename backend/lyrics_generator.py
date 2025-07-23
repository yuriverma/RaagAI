import requests

def generate_lyrics(genre, api_key, model="sonar-pro"):
    """
    Generate lyrics for the given genre using Perplexity API.
    Returns text string.
    """
    prompt = f"""
    Write original song lyrics for an Indian music track in {genre.upper()} style.
    Rules:
    - Keep it in Hindi/Urdu for Qawwali, Hinglish for DHH, pure Hindi for Classical.
    - Max 8-10 lines.
    - Maintain traditional structure for Qawwali and Classical, and rap flow for DHH.
    Output only lyrics, no extra commentary.
    """

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "temperature": 0.8,
        "max_tokens": 300,
        "messages": [
            {"role": "system", "content": "You are a professional Indian lyricist AI."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        lyrics = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        if not lyrics:
            return "[No lyrics generated]"

        return lyrics

    except Exception as e:
        print(f"Error generating lyrics: {e}")
        return "[Lyrics generation failed]"

