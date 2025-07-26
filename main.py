from helium import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import streamlit as st

st.title('MOVIE REVIEW ANALYSIS 🍿')

with st.form(key='movie-form'):
    movie_name = st.text_input('🎬 Enter the IMDb-recognized movie name')
    is_done = st.form_submit_button("SEARCH")

if is_done:
    with st.status("Launching IMDb Search...", expanded=True) as status:
        try:
            start_chrome("https://www.imdb.com/find?q=" + movie_name)
            time.sleep(3)
            status.update(label="Navigating to search results...")

            click(S("//a[contains(@class, 'ipc-metadata-list-summary-item__t') and contains(@href, '/title/')]"))
            status.update(label="Opening movie page...")

            time.sleep(2)
            rating_element = find_all(S("//span[@class='sc-4dc495c1-1 lbQcRY']"))
            rating = rating_element[0].web_element.text

            click(S("//a[contains(@href, '/reviews') and contains(@class, 'ipc-title-link-wrapper')]"))
            time.sleep(3)
            status.update(label="Opening reviews section...")

            checkbox = S("//input[contains(@class , 'ipc-boolean-input__input')]")
            if checkbox.exists():
                click(checkbox)
                time.sleep(1)
                status.update(label="Filtered user reviews.")
            else:
                status.update(label="⚠️ Checkbox for filtering not found.")

            all_button = S("//button[.//span[contains(@class, 'ipc-btn__text') and contains(., 'All')]]")
            if all_button.exists():
                click(all_button)
                time.sleep(8)
                status.update(label="Loaded all reviews.")
            else:
                status.update(label="⚠️ All button not found, fetching visible reviews only.")

            review_elements = find_all(S("//div[contains(@class, 'ipc-html-content')]"))
            reviews = []
            for r in review_elements:
                text = r.web_element.get_attribute("innerText").strip()
                if text and text not in reviews:
                    reviews.append(text)
                if len(reviews) >= 450:
                    break

            status.update(label=f"Fetched {len(reviews)} reviews.")
        except Exception as e:
            status.update(label=f"❌ Error: {e}")
            kill_browser()
            st.stop()

    status.update(label="Analyzing sentiments...", state="running")

    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    for review in reviews:
        score = analyzer.polarity_scores(review)
        if score['compound'] >= 0.05:
            sentiments.append("Positive")
        elif score['compound'] <= -0.05:
            sentiments.append("Negative")
        else:
            sentiments.append("Neutral")

    score = 0
    for sentiment in sentiments:
        if sentiment == "Positive":
            score += 1
        elif sentiment == "Negative":
            score -= 1
        elif sentiment == "Neutral":
            score += 0.2

    total_reviews = len(sentiments)
    normalized_score = round(((score / total_reviews) + 1) * 5, 2)
    normalized_score = (normalized_score + float(rating)) / 2

    if normalized_score >= 9:
        overall = "Blockbuster"
        color = "#009e60"  
    elif normalized_score >= 8.5:
        overall = "Super Hit"
        color = "#33b249"  
    elif normalized_score >= 7:
        overall = "Hit"
        color = "#85e085" 
    elif normalized_score >= 5:
        overall = "Average"
        color = "#f4d03f"  
    elif normalized_score >= 3:
        overall = "Flop"
        color = "#ff6666"  
    else:
        overall = "Utter Flop"
        color = "#ff0000"  

    status.update(label="Analysis complete ✅", state="complete")

    st.markdown(f"""
    <div style='background-color:{color}; padding: 1.2rem; border-radius: 10px; text-align: center; color: white; font-weight: bold; font-size: 1.5rem;'>
        🎬 {overall} — {normalized_score}/10
    </div>
    """, unsafe_allow_html=True)

    kill_browser()
