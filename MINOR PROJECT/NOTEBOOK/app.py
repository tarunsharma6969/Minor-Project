import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="Movie Ratings Analysis", layout="wide")

st.title("🎬 Movie Ratings & Genre Trends Dashboard")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    movies = pd.read_csv(
        "DATA/movies.dat",
        sep="::",
        engine="python",
        encoding="latin-1",
        names=["movieId", "title", "genres"]
    )

    ratings = pd.read_csv(
        "DATA/ratings.dat",
        sep="::",
        engine="python",
        names=["userId", "movieId", "rating", "timestamp"]
    )

    df = pd.merge(ratings, movies, on="movieId")
    return df

df = load_data()

st.success("✅ Dataset Loaded Successfully!")

# -----------------------------
# Sidebar Filter
# -----------------------------
st.sidebar.header("Filter Options")

min_rating = st.sidebar.slider("Select Minimum Rating", 1.0, 5.0, 3.0)

filtered_df = df[df["rating"] >= min_rating]

# -----------------------------
# 1️⃣ Rating Distribution
# -----------------------------
st.subheader("📊 Rating Distribution")

fig1, ax1 = plt.subplots()
sns.histplot(filtered_df["rating"], bins=10, kde=True, ax=ax1)
ax1.set_xlabel("Rating")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# -----------------------------
# 2️⃣ Top 10 Most Rated Movies
# -----------------------------
st.subheader("🏆 Top 10 Most Rated Movies")

top_movies = (
    filtered_df.groupby("title")["rating"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

fig2, ax2 = plt.subplots(figsize=(10,5))
top_movies.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Number of Ratings")
st.pyplot(fig2)

# -----------------------------
# 3️⃣ Average Rating per Genre
# -----------------------------
st.subheader("🎭 Average Rating per Genre")

genre_df = filtered_df.copy()
genre_df["genres"] = genre_df["genres"].str.split("|")
genre_df = genre_df.explode("genres")

avg_genre = genre_df.groupby("genres")["rating"].mean().sort_values(ascending=False)

fig3, ax3 = plt.subplots(figsize=(10,5))
avg_genre.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Average Rating")
st.pyplot(fig3)

# -----------------------------
# 4️⃣ Year-wise Movie Trend
# -----------------------------
st.subheader("📅 Year-wise Movie Release Trend")

df["year"] = df["title"].str.extract(r"\((\d{4})\)")
year_count = df["year"].value_counts().sort_index()

fig4, ax4 = plt.subplots(figsize=(10,5))
year_count.plot(ax=ax4)
ax4.set_xlabel("Year")
ax4.set_ylabel("Number of Movies")
st.pyplot(fig4)

st.markdown("---")
st.write("📌 Project Developed using Python, Pandas, Matplotlib, Seaborn & Streamlit")