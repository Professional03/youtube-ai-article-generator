import os
import time
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from utils import get_transcript, clean_transcript


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")


primary_model = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=api_key,
    temperature=0.3
)

backup_model = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    google_api_key=api_key,
    temperature=0.3
)



def safe_invoke(prompt, retries=3):
    for i in range(retries):
        try:
            return primary_model.invoke(prompt).content

        except Exception as e:
            if "429" in str(e):  # quota exceeded
                time.sleep(10)
            elif "503" in str(e) or "UNAVAILABLE" in str(e):
                time.sleep(2 * (i + 1))
            else:
                raise e

    # fallback
    try:
        return backup_model.invoke(prompt).content
    except Exception:
        return "System busy. Please try again later."




def generate_all(text):
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
    return safe_invoke(prompt)



def parse_output(result):
    try:
        # Handle structured responses
        if isinstance(result, list):
            result = result[0].get("text", str(result))

        if isinstance(result, dict):
            result = result.get("text", str(result))

        result = str(result)

        summary = result.split('---SUMMARY---')[1].split('---ARTICLE---')[0].strip()
        article = result.split('---ARTICLE---')[1].split('---HTML---')[0].strip()
        html = result.split('---HTML---')[1].strip()

        # Fix HTML if model messes up
        if "<html" not in html.lower():
            html = f"<html><body><p>{article}</p></body></html>"

        return summary, article, html

    except Exception:
        return "Parsing failed", result, "<html><body><p>Error generating HTML</p></body></html>"



st.set_page_config(page_title="YouTube Summarizer", layout="wide")

st.title("YouTube → Article Generator")

url = st.text_input("Enter YouTube URL")

if st.button("Generate"):

    if not url:
        st.warning("Please enter a URL")
        st.stop()

    try:
        # Step 1: Transcript
        with st.spinner("Fetching transcript..."):
            transcript = get_transcript(url)

        # Step 2: Clean
        clean_text = clean_transcript(transcript)

        # Limit size (important for quota)
        clean_text = clean_text[:6000]

        # Step 3: Generate everything
        with st.spinner("Generating content..."):
            result = generate_all(clean_text)

        # Step 4: Parse
        summary, article, html = parse_output(result)

        st.success("Done!")

        # ---------------- OUTPUT ---------------- #

        st.subheader("Summary")
        st.write(summary)

        st.subheader("Article")
        st.write(article)

        st.subheader("HTML Preview")
        st.components.v1.html(html, height=600, scrolling=True)

        # Debug view (IMPORTANT)
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