import tweepy
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Download VADER lexicon
nltk.download('vader_lexicon')

# Initialize VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to fetch tweets using Tweepy
def fetch_tweets_tweepy(bearer_token, keyword, max_tweets=100):
    client = tweepy.Client(bearer_token=bearer_token)
    query = f"{keyword} lang:en -is:retweet"
    tweets = client.search_recent_tweets(query=query, max_results=max_tweets, tweet_fields=["created_at", "text", "author_id"])
    if tweets.data:
        return pd.DataFrame([(tweet.created_at, tweet.text, tweet.author_id) for tweet in tweets.data],
                            columns=['Date', 'Content', 'Username'])
    else:
        return pd.DataFrame(columns=['Date', 'Content', 'Username'])

# Function to analyze sentiment
def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)
    if score['compound'] >= 0.05:
        return 'Positive'
    elif score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Streamlit App
def main():
    st.title("Social Media Sentiment Analysis Dashboard")

    # Sidebar Inputs
    st.sidebar.header("Filters")
    keyword = st.sidebar.text_input("Enter a keyword to search for tweets", "Python")
    max_tweets = st.sidebar.slider("Number of tweets to fetch", 50, 100, 50)
    selected_sentiment = st.sidebar.selectbox("Filter by Sentiment", ["All", "Positive", "Neutral", "Negative"])

    # API Key Input
    st.sidebar.subheader("Twitter API Credentials")
    bearer_token = st.sidebar.text_input("Enter your Twitter API Bearer Token", type="password")

    if st.sidebar.button("Fetch Tweets"):
        if not bearer_token:
            st.error("Please provide a valid Twitter API Bearer Token!")
            return

        # Fetch and process data
        with st.spinner("Fetching and analyzing tweets..."):
            data = fetch_tweets_tweepy(bearer_token, keyword, max_tweets)
            if data.empty:
                st.error("No tweets found. Try a different keyword or increase the max tweets.")
                return
            data['Sentiment'] = data['Content'].apply(analyze_sentiment)

        if selected_sentiment != "All":
            data = data[data["Sentiment"] == selected_sentiment]

        # Sentiment Distribution
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        data['Sentiment'].value_counts().plot(kind='bar', ax=ax, color=['green', 'blue', 'red'])
        plt.title("Sentiment Distribution")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        st.pyplot(fig)

        # Word Cloud
        st.subheader("Word Cloud")
        all_text = " ".join(data['Content'])
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        # Data Table
        st.subheader("Tweet Data")
        st.dataframe(data)

if __name__ == "__main__":
    main()
