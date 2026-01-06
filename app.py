import streamlit as st
from main import (
    chain, parse_llm_response, run_sql,
    detect_chart_request, auto_detect_chart_type,
    create_chart, mic_input_sr, get_connection
)

st.set_page_config(
    page_title="MySQL Database Bot", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; font-size: 3rem; margin: 0;"> MySQL Database Bot</h1>
    <p style="color: #f0f0f0; font-size: 1.2rem; margin: 10px 0;">Hello! What are you looking for?</p>
    <p style="color: #e0e0e0; font-size: 1rem; margin: 0;">Ask questions about your database or request charts and visualizations!</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([7,1])

user_input = None

with col1:
    chat_input_val = st.chat_input("Type your message here...")
    if chat_input_val:
        user_input = chat_input_val

with col2:
    if st.button("🎤 Speak", use_container_width=True, help="Click to use voice input"):
        st.info("🎤 Listening...")
        try:
            spoken = mic_input_sr()
            if spoken:
                user_input = spoken
            else:
                st.warning("⚠️ Could not recognize speech, try again.")
        except Exception as e:
            st.error(f"❌ Speech error: {e}")

if user_input:
    st.markdown("---")

    st.markdown(f"""
    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #2196f3;">
        <strong>👤 You:</strong> {user_input}
    </div>
    """, unsafe_allow_html=True)

    st.header(f"Bot")

    with st.container():
        with st.spinner("🔍 Processing your query..."):
            try:
                requested_chart_type = detect_chart_request(user_input)

                raw_output = chain.invoke({"question": user_input}).content.strip()
                res, sql_query = parse_llm_response(raw_output)

                if not sql_query:
                    st.error(" Could not parse SQL query from response.")
                else:
                    df = run_sql(sql_query)

                    if not df.empty and df.shape == (1, 1):
                        value = df.iloc[0, 0]
                        final_answer = f"{res} {value}"

                        st.markdown(f"""
                        <div style="background-color: #e8f5e8; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #4caf50;">
                            <h4 style="color: #2e7d32; margin: 0;">✅ Result</h4>
                            <p style="font-size: 1.1rem; margin: 5px 0 0 0;">{final_answer}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    else:
                        if requested_chart_type:
                            if requested_chart_type == "auto":
                                chart_type = auto_detect_chart_type(df)
                            else:
                                chart_type = requested_chart_type

                            if chart_type:
                                chart = create_chart(df, chart_type, res)
                                if chart:
                                    st.markdown("#### Visualization")
                                    st.plotly_chart(chart, use_container_width=True)
                                else:
                                    st.info("Could not create chart. Showing data table instead.")

                            if not df.empty:
                                st.markdown("#### Data Table")
                                df_display = df.copy()
                                df_display.index = df_display.index + 1
                                st.dataframe(df_display, use_container_width=True)

                        else:
                            st.write(res)
                            if not df.empty:
                                st.markdown("#### Data Results")
                                df_display = df.copy()
                                df_display.index = df_display.index + 1
                                st.dataframe(df_display, use_container_width=True)

            except Exception as e:
                st.markdown(f"""
                <div style="background-color: #ffebee; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #f44336;">
                    <h4 style="color: #c62828; margin: 0;">❌ Error</h4>
                    <p style="margin: 5px 0 0 0;">Error: {e}</p>
                </div>
                """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h4 style="color: #1976d2; margin-top: 0;"> Note : </h4>
        <p style="margin-bottom: 0; font-size: 0.9rem;">You can ask for charts or it will show automatically if helpfull</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    try:
        test_conn = get_connection()
        test_conn.close()
        st.markdown("""
        <div style="display: flex; align-items: center; padding: 10px; background-color: #e8f5e8; border-radius: 5px;">
            <span style="color: #4caf50; margin-right: 8px;">🟢</span>
            <span style="color: #2e7d32; font-weight: bold;">Database Connected</span>
        </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div style="display: flex; align-items: center; padding: 10px; background-color: #ffebee; border-radius: 5px;">
            <span style="color: #f44336; margin-right: 8px;">🔴</span>
            <span style="color: #c62828; font-weight: bold;">Database Disconnected</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
<div style="background-color:#f5f5f5; padding:12px; border-radius:10px;">
    <h4 style="margin-top:0;">💡 Example Queries</h4>
    <ul style="line-height:1.6;">
        <li>show the departments distribution</li>
        <li>give names of male employees</li>
        <li>list employees working in Finance department</li>
        <li>show salary distribution in a bar chart</li>
        <li>how many employees are there</li>
        <li>show number of male and female employees</li>
    </ul>
</div>
""", unsafe_allow_html=True)


    st.link_button(
        "View Code on GitHub",
        "https://github.com/gaurav5268/SQLDatabase-Insight",
        use_container_width=True
    )

