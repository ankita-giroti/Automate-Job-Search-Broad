import streamlit as st
import pandas as pd

st.title("Data Science jobs on :blue[LinkedIn]")

jobs = pd.read_csv('linkedin_jobs.csv')

st.write(jobs)