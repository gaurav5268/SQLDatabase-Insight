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


# -------------------- LLM SETUP --------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set in environment (.env)")

groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0.0
)

llm = groq_llm


def llm_chain(prompt, llm):
    chain = prompt | llm
    return chain


chain = llm_chain(prompt, llm)


# -------------------- DB CONNECTION --------------------

def get_connection():
    db_path = os.path.join(os.getcwd(), "database.db")
    return sqlite3.connect(db_path)


# -------------------- LLM RESPONSE NORMALIZER --------------------

def normalize_llm_output(resp):
    """
    Groq may return content as list[('text','chunk')]
    Convert to plain string.
    """
    if not hasattr(resp, "content"):
        return str(resp)

    content = resp.content

    # Case — Groq structured output
    if isinstance(content, list):
        return "".join(
            chunk[1]
            for chunk in content
            if isinstance(chunk, tuple) and len(chunk) == 2
        )

    # Case — plain text
    return content


# -------------------- PARSER --------------------

def parse_llm_response(raw_text: str):
    raw_text = raw_text.strip()

    # Split safely on "2."
    parts = re.split(r"\b2\.\s*", raw_text, 1)

    nlp_part = parts[0].replace("1.", "").strip()
    sql_part = parts[1].strip() if len(parts) > 1 else ""

    return nlp_part, sql_part


# -------------------- SQL RUNNER --------------------

def run_sql(query: str):
    if not query:
        return pd.DataFrame()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        return pd.DataFrame(rows, columns=cols)

    finally:
        conn.close()


# -------------------- TEXT RESPONSE FORMATTER --------------------

def format_final_response(nlp_part: str, df: pd.DataFrame) -> str:
    if df.shape == (1, 1):
        value = df.iloc[0, 0]
        return f"{nlp_part} {value}"
    else:
        return f"{nlp_part}\n{df.to_string(index=False)}"


# -------------------- CHART DETECTION --------------------

def detect_chart_request(user_input: str) -> str:
    user_input_lower = user_input.lower()

    if any(k in user_input_lower for k in ["bar chart", "bar graph"]):
        return "bar"
    elif any(k in user_input_lower for k in ["pie chart", "pie graph"]):
        return "pie"
    elif any(k in user_input_lower for k in ["line chart", "line graph", "trend"]):
        return "line"
    elif any(k in user_input_lower for k in ["scatter plot", "scatter chart"]):
        return "scatter"
    elif any(k in user_input_lower for k in ["chart", "graph", "plot", "visualization", "distribution", "comparison"]):
        return "auto"

    return None


def auto_detect_chart_type(df: pd.DataFrame) -> str:
    if df.empty:
        return None

    if df.shape == (1, 1):
        return None

    num_cols = len(df.columns)

    if num_cols == 2:
        c1, c2 = df.dtypes.iloc[0], df.dtypes.iloc[1]

        if (c1 == 'object' or c1.name == 'category') and pd.api.types.is_numeric_dtype(c2):
            if len(df) <= 10 and df.iloc[:, 1].sum() <= 100 and all(df.iloc[:, 1] >= 0):
                return "pie"
            return "bar"

        if pd.api.types.is_datetime64_any_dtype(c1) and pd.api.types.is_numeric_dtype(c2):
            return "line"

        if pd.api.types.is_numeric_dtype(c1) and pd.api.types.is_numeric_dtype(c2):
            return "scatter"

    if num_cols > 2:
        return "bar"

    return "bar"


# -------------------- CHART CREATOR --------------------

def create_chart(df: pd.DataFrame, chart_type: str, nlp_part: str):
    if df.empty or df.shape == (1, 1):
        return None

    try:
        cols = df.columns.tolist()

        if chart_type == "bar" and len(cols) >= 2:
            fig = px.bar(df, x=cols[0], y=cols[1], title=nlp_part.strip())
            fig.update_layout(xaxis_title=cols[0], yaxis_title=cols[1])
            return fig

        if chart_type == "pie" and len(cols) >= 2:
            return px.pie(df, names=cols[0], values=cols[1], title=nlp_part.strip())

        if chart_type == "line" and len(cols) >= 2:
            fig = px.line(df, x=cols[0], y=cols[1], title=nlp_part.strip())
            fig.update_layout(xaxis_title=cols[0], yaxis_title=cols[1])
            return fig

        if chart_type == "scatter" and len(cols) >= 2:
            fig = px.scatter(df, x=cols[0], y=cols[1], title=nlp_part.strip())
            fig.update_layout(xaxis_title=cols[0], yaxis_title=cols[1])
            return fig

        # fallback
        fig = px.bar(df, x=cols[0], y=cols[1], title=nlp_part.strip())
        fig.update_layout(xaxis_title=cols[0], yaxis_title=cols[1])
        return fig

    except Exception as e:
        st.error(f"Chart creation error: {e}")
        return None


# -------------------- SPEECH INPUT --------------------

def mic_input_sr(language_code="en-IN", timeout=None, phrase_time_limit=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return r.recognize_google(audio, language=language_code)


# -------------------- MAIN PIPELINE (CALL THIS IN UI) --------------------

def process_user_query(user_input: str):

    # Run LLM
    resp = chain.invoke(user_input)

    # Normalize Groq output
    raw_text = normalize_llm_output(resp)

    # Extract NLP response + SQL query
    nlp_part, sql_part = parse_llm_response(raw_text)

    # Run SQL
    df = run_sql(sql_part)

    # Text response
    final_text = format_final_response(nlp_part, df)

    st.write(final_text)

    # Chart detection
    chart_req = detect_chart_request(user_input)

    if chart_req:
        chart_type = chart_req if chart_req != "auto" else auto_detect_chart_type(df)
        fig = create_chart(df, chart_type, nlp_part)
        if fig:
            st.plotly_chart(fig)
