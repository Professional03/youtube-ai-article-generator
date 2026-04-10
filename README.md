# YouTube → Article Generator

🚀 **Live Demo:** [http://51.21.243.192:8501](http://51.21.243.192:8501)

A Generative AI-powered web application that converts any YouTube video into a structured, publication-ready article. Paste a YouTube URL, and the app automatically extracts the transcript, generates a concise summary, and produces a full HTML article — ready to download and publish.

---

## What It Does

- **Extracts** the transcript from any YouTube video with captions
- **Summarizes** the transcript into a concise, informative paragraph using Google Gemini
- **Generates** a structured, publication-ready HTML article from the summary
- **Previews** the article inline and allows one-click HTML download

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | Google Gemini 2.5 Flash (via `google-genai`) |
| Transcript | `youtube-transcript-api` |
| Deployment | AWS EC2 (Ubuntu, t3.micro) |
| Language | Python 3 |

---

## Project Structure

```
youtube-ai-article-generator/
│
├── app.py                  # Streamlit UI + Gemini API calls
├── utils.py                # Transcript extraction + text cleaning
├── requirements.txt        # Python dependencies
├── .env                    # API key (gitignored)
└── .gitignore
```

---

## How to Run Locally

**1. Clone the repo:**
```bash
git clone https://github.com/Professional03/youtube-ai-article-generator.git
cd youtube-ai-article-generator
```

**2. Create a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Add your Gemini API key:**

Create a `.env` file in the root folder:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get a free API key at [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

**5. Run the app:**
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How to Use

1. Paste any YouTube video URL into the input field
2. Click **Generate**
3. View the **Summary** and **Article** in the UI
4. Preview the **HTML output** inline
5. Click **Download HTML** to save the article

---

## Deployment

The app is deployed on **AWS EC2** (Ubuntu t3.micro, Europe/Stockholm region).

- Instance is kept live using `nohup`
- Port 8501 is open via EC2 Security Group inbound rules
- API key is stored securely in a `.env` file on the server (never committed to GitHub)

---

## Use Case

Built for **marketing agencies** that need to rapidly extract insights from YouTube videos (tutorials, product demos, promotional content) and repurpose them as blog posts, documentation, or campaign assets — without manual effort.

---

## Author

**Tejas Chikane**  
Internship Project — Innomatics Research Labs  
Generative AI Track
