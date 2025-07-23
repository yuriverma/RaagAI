from pydub import AudioSegment
import random
import os

SAMPLES_DIR = "samples"

def generate_music(genre, output_path="outputs/tracks/generated_track.mp3", target_duration_ms=30000):
    """
    Generate structured music with proper overlay for build-up and main section.
    """
    genre_path = os.path.join(SAMPLES_DIR, genre)
    loops = [os.path.join(genre_path, f) for f in os.listdir(genre_path) if f.endswith(".mp3")]

    if not loops:
        raise ValueError(f"No loops found for genre: {genre}")

    # Normalize loops to ~4 sec
    normalized_loops = []
    for loop_path in loops:
        loop = AudioSegment.from_file(loop_path)

        # Handle length issues
        if len(loop) > 8000:  # >8 sec → cut to 8 sec
            loop = loop[:8000]
        elif len(loop) < 2000:  # <2 sec → repeat until 4 sec
            while len(loop) < 4000:
                loop += loop
            loop = loop[:4000]
        else:
            loop = loop[:4000]

        normalized_loops.append(loop)

    if len(normalized_loops) < 2:
        raise ValueError("Need at least 2 loops for layering!")

    random.shuffle(normalized_loops)

    # Sections
    intro = normalized_loops[0] - 6  # Soft volume

    # Build: overlay first 2 loops
    build = normalized_loops[0].overlay(normalized_loops[1])

    # Main: overlay all loops
    main = normalized_loops[0]
    for loop in normalized_loops[1:]:
        main = main.overlay(loop)

    # Repeat and structure
    track = intro + build + (main * 6)  # Repeat main to reach length
    track = track[:target_duration_ms]

    # Fade out at end
    track = track.fade_out(3000)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    track.export(output_path, format="mp3")
    return output_path

