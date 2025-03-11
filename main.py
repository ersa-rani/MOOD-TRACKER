import streamlit as st
import pandas as pd
import datetime
import csv
import os

MOOD_FILE = "mood_log.csv"

# Function to load mood data
def load_mood_data():
    if not os.path.exists(MOOD_FILE):
        return pd.DataFrame(columns=["Date", "Mood"])
    return pd.read_csv(MOOD_FILE)

# Function to save mood data
def save_mood_data(date, mood):
    with open(MOOD_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([str(date), mood])  # Convert date to string and save

# UI Enhancements
st.set_page_config(page_title="Mood Tracker", page_icon="😊", layout="centered")

st.title("😊 Mood Tracker")

today = datetime.date.today()

st.subheader("🌟 How are you feeling today?")

# Improved Mood Selection with Emojis
mood_options = {
    "😊 Happy": "Happy",
    "😢 Sad": "Sad",
    "😡 Angry": "Angry",
    "😐 Neutral": "Neutral",
}
mood = st.selectbox("Select your mood", list(mood_options.keys()))

if st.button("Log Mood", use_container_width=True):
    save_mood_data(today, mood_options[mood])
    st.success("✅ Mood Logged Successfully!")

# Load Data
data = load_mood_data()

if not data.empty:
    st.subheader("📊 Mood Trends Over Time")

    # Convert Date column to datetime
    data["Date"] = pd.to_datetime(data["Date"])

    # Count occurrences of each mood
    mood_counts = data["Mood"].value_counts()

    # Bar Chart for Mood Distribution
    st.bar_chart(mood_counts)

    # Line Chart for Mood Trends
    mood_trends = data.groupby("Date")["Mood"].count()
    st.line_chart(mood_trends)

    # Display Data Summary
    with st.expander("📜 Mood Log Data"):
        st.dataframe(data)

    # Show Most Frequent Mood
    most_common_mood = mood_counts.idxmax()
    st.info(f"💡 Most Frequent Mood: **{most_common_mood}**")

