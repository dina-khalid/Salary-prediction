import streamlit as st
from predict import showPredictPage
from ExplorePage import showExplorePage

page = st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore"))


if page == "Predict":
    showPredictPage()
else:
    showExplorePage()