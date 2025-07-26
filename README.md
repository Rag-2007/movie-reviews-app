# 🎬 IMDb Movie Review Sentiment Analyzer

A Streamlit app that scrapes IMDb user reviews for any movie, analyzes sentiment using VADER, and gives a final verdict like **Blockbuster**, **Hit**, or **Flop** — based on both IMDb rating and public opinion.

---

## 🚀 Features

- 🔍 Search any IMDb-recognized movie
- 📄 Extract up to 450 user reviews
- 💬 Analyze sentiment (Positive / Negative / Neutral) using lexicons
- ⭐ Combine IMDb rating with sentiment score
- 🎨 Verdict displayed as Blockbuster, Hit, Flop, etc.

---

## 🛠️ Tech Stack

- `streamlit` – UI framework
- `helium` – IMDb automation (built on Selenium)
- `vaderSentiment` – Sentiment analysis
- Python 3.10+ (tested on macOS with M3 chip)

---

## 📦 Installation

```bash

git clone https://github.com/yourusername/imdb-sentiment-analyzer.git
cd imdb-sentiment-analyzer

pip install -r requirements.txt

streamlit run app.py

---

imdb-sentiment-analyzer/
│
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

---

Built with ❤️ by Raghuveer Karanam
