from backend.music_pipeline import generate_music

API_KEY = "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"
genre = "classical"  # or "qawwali" or "dhh"

result = generate_music(genre, API_KEY)
print("🔥 Full generation complete:", result)

