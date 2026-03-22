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
# Rating Distribution
# -----------------------------
st.markdown("---")
st.subheader("📊 Rating Distribution")

fig1, ax1 = plt.subplots()
sns.histplot(filtered_df["rating"], bins=10, kde=True, ax=ax1)
ax1.set_xlabel("Rating")
ax1.set_ylabel("Count")
st.pyplot(fig1)

st.write("👉 Most users give ratings between 3 and 4, indicating generally positive feedback.")

# -----------------------------
# Top Rated Movies (FIXED)
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
# Average Rating per Genre
# -----------------------------
st.markdown("---")
st.subheader("🎭 Average Rating per Genre")

genre_df = filtered_df.copy()
genre_df["genres"] = genre_df["genres"].str.split("|")
genre_df = genre_df.explode("genres")

avg_genre = genre_df.groupby("genres")["rating"].mean().sort_values(ascending=False)

fig3, ax3 = plt.subplots(figsize=(10,5))
avg_genre.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Average Rating")
st.pyplot(fig3)

st.write("👉 Some genres consistently receive higher average ratings, showing audience preference for certain types of movies.")

# -----------------------------
# Year-wise Trend
# -----------------------------
st.markdown("---")
st.subheader("📅 Year-wise Movie Release Trend")

df["year"] = df["title"].str.extract(r"\((\d{4})\)")
year_count = df["year"].value_counts().sort_index()

fig4, ax4 = plt.subplots(figsize=(10,5))
year_count.plot(ax=ax4)
ax4.set_xlabel("Year")
ax4.set_ylabel("Number of Movies")
st.pyplot(fig4)

st.write("👉 The number of movies released has changed over the years, reflecting trends in the film industry.")

# -----------------------------
# Download Button
# -----------------------------
st.markdown("---")
st.subheader("📥 Download Data")

st.download_button(
    label="Download Full Dataset as CSV",
    data=df.to_csv(index=False),
    file_name="movie_data.csv",
    mime="text/csv"
)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.write("📌 Project Developed using Python, Pandas, Matplotlib, Seaborn & Streamlit")
