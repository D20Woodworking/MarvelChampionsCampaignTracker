import streamlit as st
import pandas as pd

st.title("Marvel Champions Campaign Tracker")

# UI for logging sessions
with st.form("log_game"):
    date = st.date_input("Date")
    heroes = st.multiselect("Heroes played", ["Iron Man", "Captain America", "Black Panther"])
    villain = st.selectbox("Villain", ["Ultron", "Green Goblin", "Loki"])
    result = st.radio("Result", ["Win", "Loss"])
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Log game")
    if submitted:
        row = {"Date": date, "Heroes": heroes, "Villain": villain, "Result": result, "Notes": notes}
        st.session_state.logs = st.session_state.get("logs", []) + [row]

# Display logs
logs = st.session_state.get("logs", [])
if logs:
    df = pd.DataFrame(logs)
    st.subheader("Logged Games")
    st.dataframe(df)
    st.subheader("Win/Loss Stats")
    st.bar_chart(df["Result"].value_counts())
