import json
import os

import ffmpeg


def process_video(input_file, output_file):
    # Extract metadata information from the video
    metadata = {
        "clip_name": os.path.basename(input_file),
        "description": "",
        "clip_start_point": 0.0,
        "clip_end_point": 0.0,
        "is_autoclipped": False,
        "is_manually_trimmed": True,
        "framerate": 60,  # Assuming 60 FPS by default, can be extracted dynamically if needed
        "audio_bitrate": 192,  # Default audio bitrate
        "audio_samplerate": 48000,  # Default audio samplerate
        "video_bitrate": 0,  # Default video bitrate
        "resolution_width": 2560,  # Assuming 2560 width by default
        "resolution_height": 1440,  # Assuming 1440 height by default
        "recording_timestamp": "unknown",  # You can extract the actual timestamp dynamically
        "last_edit_timestamp": "unknown",  # Can be set dynamically
        "game_name": "Unknown Game",  # Default value, can be updated based on the game
        "full_length": 0.0,  # Will be set dynamically
        "tags": [],
        "audio_tracks_props": [
            {"name": "Game", "volume": 1, "muted": False},
            {"name": "Chat", "volume": 1, "muted": False},
            {"name": "Mic", "volume": 1, "muted": False},
        ],
        "audio_drop": 0,
        "video_drop": 0,
        "hdr_enabled": False,
        "duplicated_frames_count": 0,
        "game_session_id": "unknown-session-id",  # Default
        "capture_mode": "game",  # Assuming game capture by default
        "shared_clips_array": [],
    }

    # Use ffprobe to extract actual metadata details (e.g., duration, resolution)
    probe = ffmpeg.probe(
        input_file,
        v="error",
        select_streams="v:0",
        show_entries="stream=duration,width,height",
    )

    # Update video metadata from ffprobe output
    metadata["full_length"] = float(probe["streams"][0]["duration"])
    metadata["resolution_width"] = int(probe["streams"][0]["width"])
    metadata["resolution_height"] = int(probe["streams"][0]["height"])

    # If you have a method to detect the game name or other details, you can add that here
    metadata["game_name"] = "Tom Clancy's Rainbow Six Siege"  # This can be dynamic

    # Convert metadata to JSON format
    metadata_json = json.dumps(metadata)

    # Process video using ffmpeg and add metadata
    ffmpeg.input(input_file).output(
        output_file,
        vcodec="libx264",
        acodec="aac",
        metadata="STEELSERIES_META=" + metadata_json,
    ).run()


def process_folder(input_folder, output_folder):
    # Make sure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all video files in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Only process .mp4 files (or other formats you need)
        if input_path.endswith(".mp4"):
            output_path = os.path.join(output_folder, f"Processed_{filename}")

            print(f"Processing {filename}...")
            process_video(input_path, output_path)
            print(f"Processed video saved to {output_path}")


# Example usage
input_folder = "./Records"  # Folder with the original clips
output_folder = "./Processed"  # Folder to save the processed clips

process_folder(input_folder, output_folder)
