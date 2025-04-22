from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import subprocess
from pydub import AudioSegment
import os


app = Flask(__name__)
CORS(app)  # Allow CORS for frontend requests

# Ensure output directory exists
OUTPUT_DIR = "output_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_song_from_url(url, output_file):
    """Download a song from a YouTube URL using yt-dlp."""
    try:
        subprocess.run([
            'yt-dlp',
            url,
            '--extract-audio',
            '--audio-format', 'mp3',
            '-o', output_file
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: yt-dlp or ffmpeg not found.")
        return False

def download_song(song_name, output_file):
    """Download a song from YouTube using yt-dlp search."""
    try:
        subprocess.run([
            'yt-dlp',
            f'ytsearch1:{song_name}',
            '--extract-audio',
            '--audio-format', 'mp3',
            '-o', output_file
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {song_name}: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: yt-dlp or ffmpeg not found.")
        return False

def process_songs(song1_path, song2_path, output_path):
    """Process and combine two songs into a stereo audio file."""
    try:
        # Load audio files
        song1 = AudioSegment.from_mp3(song1_path)
        song2 = AudioSegment.from_mp3(song2_path)

        # Match lengths
        len1, len2 = len(song1), len(song2)
        if len1 < len2:
            song1 += AudioSegment.silent(duration=len2 - len1)
        elif len2 < len1:
            song2 += AudioSegment.silent(duration=len1 - len2)

        # Convert to mono
        song1_mono = song1.set_channels(1)
        song2_mono = song2.set_channels(1)

        # Pan: song1 → left, song2 → right
        song1_left = song1_mono.set_channels(2).pan(-1)
        song2_right = song2_mono.set_channels(2).pan(1)

        # Combine
        combined = song1_left.overlay(song2_right)

        # Export
        combined.export(output_path, format="mp3")
        return True
    except Exception as e:
        print(f"Error processing songs: {str(e)}")
        return False

@app.route('/download_by_url', methods=['POST'])
def download_by_url():
    data = request.json
    song1_url = data.get('song1_url')
    song2_url = data.get('song2_url')

    if not song1_url or not song2_url:
        return jsonify({'error': 'Both URLs are required'}), 400

    song1_path = os.path.join(OUTPUT_DIR, "song1.mp3")
    song2_path = os.path.join(OUTPUT_DIR, "song2.mp3")
    output_path = os.path.join(OUTPUT_DIR, "combined.mp3")

    # Download songs
    if not download_song_from_url(song1_url, song1_path):
        return jsonify({'error': 'Failed to download song 1'}), 500
    if not download_song_from_url(song2_url, song2_path):
        return jsonify({'error': 'Failed to download song 2'}), 500

    # Process and combine
    if not process_songs(song1_path, song2_path, output_path):
        return jsonify({'error': 'Failed to process songs'}), 500

    return send_file(output_path, as_attachment=True, download_name="combined.mp3")

@app.route('/download_by_name', methods=['POST'])
def download_by_name():
    data = request.json
    song1_name = data.get('song1_name')
    song2_name = data.get('song2_name')

    if not song1_name or not song2_name:
        return jsonify({'error': 'Both song names are required'}), 400

    song1_path = os.path.join(OUTPUT_DIR, "song1.mp3")
    song2_path = os.path.join(OUTPUT_DIR, "song2.mp3")
    output_path = os.path.join(OUTPUT_DIR, "combined.mp3")

    # Download songs
    if not download_song(song1_name, song1_path):
        return jsonify({'error': 'Failed to download song 1'}), 500
    if not download_song(song2_name, song2_path):
        return jsonify({'error': 'Failed to download song 2'}), 500

    # Process and combine
    if not process_songs(song1_path, song2_path, output_path):
        return jsonify({'error': 'Failed to process songs'}), 500

    return send_file(output_path, as_attachment=True, download_name="combined.mp3")

@app.route("/")
def index():
    return render_template("main.html")

if __name__ == '__main__':
    app.run(debug=True)
