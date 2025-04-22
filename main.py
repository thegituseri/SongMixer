import subprocess
from pydub import AudioSegment
import sys
import os

def download_song_from_url(url, output_file):
    """Download a song from a YouTube URL using yt-dlp."""
    try:
        subprocess.run([
            'yt-dlp',
            url,  # Use URL directly
            '--extract-audio',
            '--audio-format', 'mp3',
            '-o', output_file
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Downloaded: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}:")
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: yt-dlp or ffmpeg not found. Ensure they are installed and in your PATH.")
        sys.exit(1)


def download_song(song_name, output_file):
    """Download a song from YouTube using yt-dlp."""
    subprocess.run([
        'yt-dlp',
        f'ytsearch1:{song_name}',
        '--extract-audio',
        '--audio-format', 'mp3',
        '-o', output_file
    ], check=True)

def main():
    # 1) Get song names from user
    method = input("Enter '1' to download from URL or '2' to search by name: ")
    song1 = 0
    song2 = 0
    if method == '1':
        song1_URL= input("Enter song URL for left ear: ")
        song2_URL = input("Enter song URL for the right ear: ")
        song1 = download_song_from_url(song1_URL, "song1.mp3")
        song2 = download_song_from_url(song2_URL, "song2.mp3")
    else:
        song1_name = input("Enter song name for left ear: ")
        song2_name = input("Enter song name for right ear: ")
        song1 = download_song(song1_name, "song1.mp3")
        song2 = download_song(song2_name, "song2.mp3")

    # 3) Load the audio files
    song1 = AudioSegment.from_mp3("song1.mp3")
    song2 = AudioSegment.from_mp3("song2.mp3")

    # 4) Match lengths by padding the shorter song with silence
    len1, len2 = len(song1), len(song2)
    if len1 < len2:
        song1 += AudioSegment.silent(duration=len2 - len1)
    elif len2 < len1:
        song2 += AudioSegment.silent(duration=len1 - len2)

    # 5) Convert to mono
    song1_mono = song1.set_channels(1)
    song2_mono = song2.set_channels(1)

    # 6) Pan: song1 → left, song2 → right
    song1_left  = song1_mono.set_channels(2).pan(-1)  # full left
    song2_right = song2_mono.set_channels(2).pan(1)   # full right

    # 7) Overlay to mix them so they play simultaneously
    combined = song1_left.overlay(song2_right)

    # 8) Export the result
    combined.export("combined.mp3", format="mp3")
    print("Songs combined successfully! Check 'combined.mp3'.")

if __name__ == "__main__":
    main()
