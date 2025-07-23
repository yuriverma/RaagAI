from pydub import AudioSegment
import os

def find_sample_path(samples_root, layer_name):
    """Search for the correct sample in any subfolder by prefix match."""
    base_name = layer_name.replace(".mp3", "").replace(".wav", "")
    for root, _, files in os.walk(samples_root):
        for file in files:
            if file.lower().startswith(base_name.lower()):
                return os.path.join(root, file)
    return None

def mix_audio(arrangement, samples_path="samples", output_path="outputs/tracks/final_track.mp3"):
    """Mix track based on arrangement with volume balance and fades."""
    final_track = AudioSegment.silent(duration=0)

    for section in arrangement:
        start_time = section.get("start", 0)
        end_time = section.get("end", 0)
        layers = section.get("layers", [])
        section_duration = (end_time - start_time) * 1000

        if section_duration <= 0:
            continue

        mixed_section = AudioSegment.silent(duration=section_duration)

        for layer in layers:
            layer_path = find_sample_path(samples_path, layer)
            if not layer_path:
                print(f"❌ Missing: {layer}")
                continue

            print(f"✅ Adding layer: {layer_path}")
            loop = AudioSegment.from_file(layer_path)

            # Normalize (-3dB)
            loop = loop.apply_gain(-3)

            # Repeat if shorter
            if len(loop) < section_duration:
                repeat_times = (section_duration // len(loop)) + 1
                loop = loop * repeat_times

            loop = loop[:section_duration]

            # Smooth transitions
            loop = loop.fade_in(300).fade_out(300)

            mixed_section = mixed_section.overlay(loop)

        final_track += mixed_section

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_track.export(output_path, format="mp3")
    return output_path

