import streamlit as st
import pandas as pd

DATA_PATH = "./data/olist_order_reviews_dataset.csv"

df = pd.read_csv(DATA_PATH)
# Lesson assumption:
# this dataset has already gone through EDA and basic cleaning.
# Here we focus on dashboard building, not data cleaning.
# We still set the datetime dtype explicitly for reliable filtering and charting.
df["review_creation_date"] = pd.to_datetime(df["review_creation_date"])

st.title("🛒 Olist Order Reviews Dashboard")
st.write(f"Rows loaded: {len(df):,} | Columns: {len(df.columns)}")
st.dataframe(df.head(20), width="stretch")

unique_reviews = sorted(df["review_id"].dropna().unique())
unique_orders = sorted(df["order_id"].dropna().unique())

min_review_score = int(df["review_score"].min())
max_review_score = int(df["review_score"].max())
review_range = st.sidebar.slider(
    "Review Score Range",
    min_value=min_review_score,
    max_value=max_review_score,
    value=(min_review_score, max_review_score),
    step=1,
)

date_min = df["review_creation_date"].min().date()
date_max = df["review_creation_date"].max().date()
date_range = st.sidebar.date_input("Review Creation Date Range", value=(date_min, date_max))

filtered_df = df.copy()
filtered_df = filtered_df[filtered_df["review_score"].between(review_range[0], review_range[1])]

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        filtered_df["review_creation_date"].between(pd.to_datetime(start_date), pd.to_datetime(end_date))   
    ]

st.header("Filtered Results")
st.write(f"Matching rows: {len(filtered_df):,} | Columns: {len(filtered_df.columns)}")
st.dataframe(filtered_df.head(20), width="stretch")