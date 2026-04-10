# app.py

import streamlit as st
from dotenv import load_dotenv
from google import genai
from utils import get_transcript, clean_transcript
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash"


def generate_all(text: str) -> str:
    prompt = f"""
You are an AI content generator.

STRICT RULES:
- Return ONLY plain text
- DO NOT return JSON, lists, or objects
- HTML must be COMPLETE and VALID
- HTML must include: <!DOCTYPE html>, <html>, <head>, <body>
- Use proper tags: <h1>, <h2>, <p>, <ul>, <li>

Generate content in EXACT format:

---SUMMARY---
<summary>

---ARTICLE---
<article>

---HTML---
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Generated Article</title>
</head>
<body>
<h1>Main Title</h1>
<p>Content...</p>
</body>
</html>

Transcript:
{text}
"""
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {str(e)}")


def parse_output(result: str):
    try:
        if isinstance(result, (list, dict)):
            result = str(result)

        summary = result.split('---SUMMARY---')[1].split('---ARTICLE---')[0].strip()
        article = result.split('---ARTICLE---')[1].split('---HTML---')[0].strip()
        html = result.split('---HTML---')[1].strip()

        if "<html" not in html.lower():
            html = f"<html><body><p>{article}</p></body></html>"

        return summary, article, html

    except Exception:
        return "Parsing failed.", result, "<html><body><p>Error generating HTML.</p></body></html>"


# ── UI ──────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="YouTube Summarizer", layout="wide")
st.title("YouTube → Article Generator")

url = st.text_input("Enter YouTube URL")

if st.button("Generate"):

    if not url:
        st.warning("Please enter a YouTube URL.")
        st.stop()

    try:
        with st.spinner("Fetching transcript..."):
            transcript = get_transcript(url)

        clean_text = clean_transcript(transcript)
        clean_text = clean_text[:6000]  # stay within free tier token limits

        with st.spinner("Generating content with Gemini..."):
            result = generate_all(clean_text)

        summary, article, html = parse_output(result)

        st.success("Done!")

        st.subheader("Summary")
        st.write(summary)

        st.subheader("Article")
        st.write(article)

        st.subheader("HTML Preview")
        st.components.v1.html(html, height=600, scrolling=True)

        with st.expander("Show Raw HTML"):
            st.code(html, language="html")

        st.download_button(
            label="Download HTML",
            data=html,
            file_name="article.html",
            mime="text/html"
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")