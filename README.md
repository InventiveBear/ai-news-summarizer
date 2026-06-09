# 📰 AI News Summarizer

> **Stanford Code in Place 2024 — Final Project**
> A desktop application that fetches, summarizes, and categorizes news topics using a large language model, built with Python and Tkinter.

---

## Overview

AI News Summarizer is a Python desktop application that lets users type any news topic and instantly receive an AI-generated summary with automatic topic categorization. The project was built as the final submission for **Stanford University's Code in Place** — a six-week introductory Python programming course.

The application demonstrates practical use of Python fundamentals including functions, modules, classes, threading, and GUI development, combined with real-world API integration through the Groq LLM API.

---

## Features

- **AI-Powered Summaries** — Generates concise, factual news overviews for any topic using Llama 3.3 70B via Groq
- **Auto Categorization** — Classifies topics into categories such as Technology, Science, Politics, Health, and more
- **Search History** — Keeps a sidebar log of recent searches; click any entry to re-run it
- **Quick Topic Chips** — One-click buttons for popular topics (AI, Climate, Space, Economy, Healthcare)
- **Non-blocking UI** — API calls run on a background thread so the interface stays responsive
- **Demo Mode** — Works offline with placeholder output when no API key is configured

---

## Screenshots
<img width="1366" height="721" alt="Screenshot 2026-06-10 010810" src="https://github.com/user-attachments/assets/fb40d2ef-2edc-4123-bbf6-ed6993cca787" />

<img width="1366" height="721" alt="Screenshot 2026-06-10 014452" src="https://github.com/user-attachments/assets/aa7cf478-f6ee-4732-b398-c9ffc5193741" />

<img width="1366" height="721" alt="Screenshot 2026-06-10 011014" src="https://github.com/user-attachments/assets/4936fb76-0293-41d9-8fc0-91762a081070" />

<img width="1366" height="721" alt="Screenshot 2026-06-10 014452" src="https://github.com/user-attachments/assets/7eaa1d00-9022-4cde-b347-870343177f85" />




## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| GUI | Tkinter (stdlib) |
| AI Backend | [Groq API](https://console.groq.com) — Llama 3.3 70B |
| Threading | Python `threading` module |
| Code Style | Stanford Code in Place conventions |

---

## Project Structure

```
ai-news-summarizer/
│
├── news_summarizer.py   # Main application — GUI and app logic
├── ai.py                # AI interface — wraps the Groq API call
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A free [Groq API key](https://console.groq.com) (no credit card required)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/InventiveBear/ai-news-summarizer.git
cd ai-news-summarizer
```

**2. Install dependencies**

```bash
pip install groq
```
or 
pip install -r requirements.txt

**3. Configure your API key**

Open `ai.py` and replace the placeholder with your Groq API key:

```python
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")
```

You can get a free key at [console.groq.com](https://console.groq.com) → API Keys → Create Key.

**4. Run the application**

```bash
python news_summarizer.py
```

---

## How It Works

1. The user types a topic (e.g. "Mars exploration") and clicks **Summarise**
2. The app spawns a background thread to avoid freezing the UI
3. Two separate API calls are made to the LLM:
   - One to generate a detailed news summary
   - One to classify the topic and extract tags
4. Results are rendered back on the main thread with category badges and formatted text
5. The search is saved to the history sidebar

---

## requirements.txt

```
groq
```

---

## Concepts Demonstrated

This project was built applying concepts taught across the six weeks of Code in Place:

- **Week 1–2** — Variables, functions, conditionals, loops
- **Week 3** — Decomposition and helper functions 
- **Week 4** — Data structures — lists and dictionaries 
- **Week 5** — File structure and modules 
- **Week 6** — Classes and final project 

---

## Limitations

- The free Groq tier has rate limits (14,400 requests/day, 30 requests/minute)
- Summaries are AI-generated and should not be used as a primary news source
- The application requires an internet connection to generate summaries

---

## Future Improvements

- [ ] Export summaries to PDF or text file
- [ ] Add a favorites/bookmarks feature
- [ ] Support multiple AI providers (OpenAI, Gemini)
- [ ] Display live news headlines alongside AI summaries
- [ ] Add dark/light theme toggle

---

## Acknowledgements

- **Stanford Code in Place** — for the curriculum and opportunity
- **Groq** — for providing a generous free API tier
- **Meta AI** — for the open-source Llama 3.3 model powering the summaries

---

## License

This project is open source and available under the [MIT License](LICENSE).
