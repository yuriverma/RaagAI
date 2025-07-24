import requests
import json
import re

# ✅ Genre-specific samples
GENRE_SAMPLES = {
    "qawwali": ["harmonium_qawwali.mp3", "dholak_loop.mp3", "claps.mp3"],
    "classical": ["harmonium_loop.mp3", "tabla_loop1.mp3", "clapscla.mp3"],
    "dhh": ["kick.mp3", "snare.mp3", "bass.mp3"]
}

def generate_arrangement(genre, track_length=30, API_KEY=None, model="sonar-pro", debug=False):
    loops = GENRE_SAMPLES.get(genre.lower(), GENRE_SAMPLES["classical"])

    prompt = f"""
    Generate an arrangement for {genre.upper()} music, track length {track_length} seconds.
    Use ONLY these loops: {loops}.
    Output strictly in this JSON format (no text outside JSON):
    [
      {{"start": 0, "end": 5, "layers": ["{loops[0]}"]}},
      {{"start": 5, "end": 15, "layers": ["{loops[0]}", "{loops[1]}"]}},
      {{"start": 15, "end": 30, "layers": ["{loops[0]}", "{loops[1]}", "{loops[2]}"]}}
    ]
    """

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "temperature": 0.7,
        "max_tokens": 500,
        "messages": [
            {"role": "system", "content": "You are a JSON generator for music arrangement. Respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        json_match = re.search(r"\[.*?\]", content, re.DOTALL)
        if not json_match:
            return get_mock_arrangement(genre)

        json_text = json_match.group(0)
        clean_text = (
            json_text.replace("\n", "")
            .replace("\r", "")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("'", '"')
            .strip()
        )
        if not clean_text.endswith("]"):
            clean_text += "]"

        return json.loads(clean_text)
    except Exception:
        return get_mock_arrangement(genre)


def get_mock_arrangement(genre):
    loops = GENRE_SAMPLES.get(genre.lower(), GENRE_SAMPLES["classical"])
    return [
        {"start": 0, "end": 4, "layers": [loops[0]]},
        {"start": 4, "end": 8, "layers": [loops[0], loops[1]]},
        {"start": 8, "end": 16, "layers": [loops[0], loops[1], loops[2]]},
        {"start": 16, "end": 24, "layers": [loops[0], loops[1]]},
        {"start": 24, "end": 30, "layers": [loops[0], loops[1], loops[2]]}
    ]

