import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Movie Ratings Analysis", layout="wide")

# -----------------------------
# UI Styling
# -----------------------------
st.markdown("""
<style>
h1 { color: #00FFAA; }
h2, h3 { color: #00CCFF; }
</style>
""", unsafe_allow_html=True)

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
    df["year"] = df["title"].str.extract(r"\((\d{4})\)")
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
# Dashboard Overview
# -----------------------------
st.subheader("📊 Project Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Movies", df["movieId"].nunique())
col2.metric("Total Users", df["userId"].nunique())
col3.metric("Average Rating", round(df["rating"].mean(), 2))

# -----------------------------
# Search Feature
# -----------------------------
st.subheader("🔍 Search Movie")

movie_name = st.text_input("Enter movie name")

if movie_name:
    result = df[df["title"].str.contains(movie_name, case=False)]
    st.write(result[["title", "rating"]].head(10))

# -----------------------------
# Genre Filter
# -----------------------------
st.subheader("🎭 Filter by Genre")

genre_list = sorted(set("|".join(df["genres"]).split("|")))
selected_genre = st.selectbox("Select Genre", genre_list)

genre_filtered = filtered_df[filtered_df["genres"].str.contains(selected_genre)]
st.write(genre_filtered[["title", "genres", "rating"]].head(10))

# -----------------------------
# 🎥 Movie Recommendation System (NEW 🔥)
# -----------------------------
st.markdown("---")
st.subheader("🎥 Movie Recommendation System")

# Inputs
rec_genre = st.selectbox("Choose Genre", genre_list, key="rec_genre")
rec_rating = st.slider("Minimum Rating", 1.0, 5.0, 3.5)
rec_year = st.selectbox("Select Year", sorted(df["year"].dropna().unique()))
violence_level = st.selectbox("Content Preference", ["Family Friendly (Low Violence)", "Action / Intense"])

# Filtering
recommendations = df[
    (df["genres"].str.contains(rec_genre)) &
    (df["rating"] >= rec_rating) &
    (df["year"] == rec_year)
]

# Simulated violence filter
if violence_level == "Family Friendly (Low Violence)":
    recommendations = recommendations[
        recommendations["genres"].str.contains("Comedy|Animation|Children")
    ]
else:
    recommendations = recommendations[
        recommendations["genres"].str.contains("Action|Thriller|Crime")
    ]

st.write("### 🎯 Recommended Movies:")
st.write(recommendations[["title", "genres", "rating"]].drop_duplicates().head(10))

st.write("👉 This system suggests movies based on user preferences like genre, rating, year, and content type.")

# -----------------------------
# Rating Distribution
# -----------------------------
st.markdown("---")
st.subheader("📊 Rating Distribution")

fig1, ax1 = plt.subplots()
sns.histplot(filtered_df["rating"], bins=10, kde=True, ax=ax1)
st.pyplot(fig1)

st.write("👉 Most users give ratings between 3 and 4, indicating generally positive feedback.")

# -----------------------------
# Top Rated Movies
# -----------------------------
st.markdown("---")
st.subheader("⭐ Top Rated Movies")

top_rated = (
    filtered_df.groupby("title")["rating"]
    .agg(['mean', 'count'])
    .sort_values(by="mean", ascending=False)
)

top_rated = top_rated[top_rated["count"] > 50].head(10)

st.write(top_rated)

st.write("👉 These movies have the highest average ratings and are considered the best-rated by users.")

# -----------------------------
# Genre Analysis
# -----------------------------
st.markdown("---")
st.subheader("🎭 Average Rating per Genre")

genre_df = filtered_df.copy()
genre_df["genres"] = genre_df["genres"].str.split("|")
genre_df = genre_df.explode("genres")

avg_genre = genre_df.groupby("genres")["rating"].mean().sort_values(ascending=False)

fig3, ax3 = plt.subplots(figsize=(10,5))
avg_genre.plot(kind="bar", ax=ax3)
st.pyplot(fig3)

st.write("👉 Some genres consistently receive higher average ratings.")

# -----------------------------
# Year Trend
# -----------------------------
st.markdown("---")
st.subheader("📅 Year-wise Movie Release Trend")

year_count = df["year"].value_counts().sort_index()

fig4, ax4 = plt.subplots(figsize=(10,5))
year_count.plot(ax=ax4)
st.pyplot(fig4)

st.write("👉 Movie releases vary over time showing industry trends.")

# -----------------------------
# Download
# -----------------------------
st.markdown("---")
st.subheader("📥 Download Data")

st.download_button(
    "Download Dataset",
    df.to_csv(index=False),
    "movie_data.csv"
)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.write("📌 Developed using Python, Pandas, Matplotlib, Seaborn & Streamlit")
