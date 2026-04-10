# utils.py

import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    if "v=" in url:
        video_id = url.split("v=")[-1].split("&")[0].split("?")[0]
        return video_id
    elif "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")


def get_transcript(url):
    try:
        video_id = extract_video_id(url)
        transcript = YouTubeTranscriptApi().fetch(video_id)
        text = " ".join([t.text for t in transcript])
        return text
    except Exception as e:
        raise Exception(f"Transcript error: {str(e)}")


def clean_transcript(text):
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_text(text, chunk_size=3000, overlap=200):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks