import streamlit as st
import pandas as pd

st.title("Salary Prediction Monitoring Dashboard")

logs = pd.read_csv("salary_api.log", sep="\|\|", header=None,
                   names=["Timestamp", "Level", "Message"],
                   engine="python")

logs["Timestamp"] = logs["Timestamp"].str.strip()
logs["Level"] = logs["Level"].str.strip()
logs["Message"] = logs["Message"].str.strip()

st.metric("Total Logs", len(logs))
st.metric("Errors", (logs["Level"]=="ERROR").sum())

st.dataframe(logs)
