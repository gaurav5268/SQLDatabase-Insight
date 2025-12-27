import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
import re

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

import plotly.express as px
import streamlit as st
import speech_recognition as sr

from prompts import prompt


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment (.env)")

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
if not GROQ_API_KEY:
    raise RuntimeError("GROOQ_APIKEY not set in environment (.env)")

groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0.2
)

llm = groq_llm

def get_connection():
    db_path = os.path.join(os.getcwd(), "database.db")
    return sqlite3.connect(db_path)


# this used to be for mysql database
'''import mysql.connector
def get_connection():

    "Establishes and returns a connection to the MySQL database."

    return mysql.connector.connect(
        host="YOUR_HOST ",
        user="YOUR_USERNAME ",
        password="YOUR_PASSWORD",
        database="YOUR_DATABASE"
    )'''


def llm_chain(prompt,llm):
    chain = prompt | llm
    return chain

chain = llm_chain(prompt , llm)


def parse_llm_response(raw_text: str):
    parts = raw_text.split("2.", 1)
    nlp_part = parts[0].replace("1.", "").strip()
    sql_part = parts[1].strip() if len(parts) > 1 else ""
    return nlp_part, sql_part


def run_sql(query: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cols = [col[0] for col in cursor.description]
    conn.close()
    return pd.DataFrame(rows, columns=cols)


def format_final_response(nlp_part: str, df: pd.DataFrame) -> str:
    if df.shape == (1, 1):
        value = df.iloc[0, 0]
        return f"{nlp_part} {value}"
    else:
        return f"{nlp_part}\n{df.to_string(index=False)}"


def detect_chart_request(user_input: str) -> str:
    user_input_lower = user_input.lower()

    if any(keyword in user_input_lower for keyword in ["bar chart", "bar graph"]):
        return "bar"
    elif any(keyword in user_input_lower for keyword in ["pie chart", "pie graph"]):
        return "pie"
    elif any(keyword in user_input_lower for keyword in ["line chart", "line graph", "trend"]):
        return "line"
    elif any(keyword in user_input_lower for keyword in ["scatter plot", "scatter chart"]):
        return "scatter"
    elif any(keyword in user_input_lower for keyword in ["chart", "graph", "plot", "visualization", "distribution", "comparison"]):
        return "auto"
    return None


def auto_detect_chart_type(df: pd.DataFrame) -> str:
    if df.empty:
        return None

    num_cols = len(df.columns)

    if df.shape == (1, 1):
        return None

    if num_cols == 2:
        col1_type = df.dtypes.iloc[0]
        col2_type = df.dtypes.iloc[1]

        if (col1_type == 'object' or col1_type.name == 'category') and pd.api.types.is_numeric_dtype(col2_type):
            if len(df) <= 10 and df.iloc[:, 1].sum() <= 100 and all(df.iloc[:, 1] >= 0):
                return "pie"
            return "bar"

        elif pd.api.types.is_datetime64_any_dtype(col1_type) and pd.api.types.is_numeric_dtype(col2_type):
            return "line"

        elif pd.api.types.is_numeric_dtype(col1_type) and pd.api.types.is_numeric_dtype(col2_type):
            return "scatter"

    if num_cols > 2:
        return "bar"

    return "bar"


def create_chart(df: pd.DataFrame, chart_type: str, nlp_part: str):
    if df.empty or df.shape == (1, 1):
        return None

    try:
        cols = df.columns.tolist()

        if chart_type == "bar" and len(cols) >= 2:
            fig = px.bar(df, x=cols[0], y=cols[1], title=nlp_part.strip())
            fig.update_layout(xaxis_title=cols[0], yaxis_title=cols[1])
            return fig

        elif chart_type == "pie" and len(cols) >= 2:
            fig = px.pie(df, names=cols[0], values=cols[1], title=nlp_part.strip())
            return fig

        elif chart_type == "line" and len(cols) >= 2:
            fig = px.line(df, x=cols[0], y=cols[1], title=nlp_part.strip())
            fig.update_layout(xaxis_title=cols[0], yaxis_title=cols[1])
            return fig

        elif chart_type == "scatter" and len(cols) >= 2:
            fig = px.scatter(df, x=cols[0], y=cols[1], title=nlp_part.strip())
            fig.update_layout(xaxis_title=cols[0], yaxis_title=cols[1])
            return fig

        fig = px.bar(df, x=cols[0], y=cols[1], title=nlp_part.strip())
        fig.update_layout(xaxis_title=cols[0], yaxis_title=cols[1])
        return fig

    except Exception as e:
        st.error(f"Chart creation error: {e}")
        return None


def mic_input_sr(language_code="en-IN", timeout=None, phrase_time_limit=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    text = r.recognize_google(audio, language=language_code)
    return text
