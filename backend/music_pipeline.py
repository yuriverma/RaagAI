from backend.arrangement_planner import generate_arrangement
from backend.audio_mixer import mix_audio
from backend.lyrics_generator import generate_lyrics
import os

def generate_music(genre, api_key, track_length=30):
    """
    Full pipeline: arrangement → lyrics → audio mix → save outputs.
    """
    print(f"🎵 Generating {genre.upper()} music...")

    # Step 1: Get Arrangement from Perplexity
    print("➡ Fetching arrangement...")
    arrangement = generate_arrangement(genre, track_length, api_key)
    print(f"✅ Arrangement received: {arrangement}")

    # Step 2: Mix audio
    print("➡ Mixing audio...")
    track_path = f"outputs/tracks/{genre}_track.mp3"
    mix_audio(arrangement, samples_path="samples", output_path=track_path)
    print(f"✅ Audio track ready at: {track_path}")

    # Step 3: Generate lyrics
    print("➡ Generating lyrics...")
    lyrics = generate_lyrics(genre, api_key)
    lyrics_dir = "outputs/lyrics"
    os.makedirs(lyrics_dir, exist_ok=True)
    lyrics_path = os.path.join(lyrics_dir, f"{genre}_lyrics.txt")

    with open(lyrics_path, "w") as f:
        f.write(lyrics)
    print(f"✅ Lyrics saved at: {lyrics_path}")

    return {"track": track_path, "lyrics": lyrics_path, "arrangement": arrangement}

