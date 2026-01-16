import streamlit as st
import asyncio
from agent import agent_triage
from agent import voice_agent_builder
import os
from openai import OpenAI
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
import ssl
import time
SERVICE_ACCOUNT_FILE = "/Users/Rakshit.Lodha/Downloads/useful-approach-484123-n8-fcf7d7c5d2b8.json" #check-this
SHEET_ID = "16gxyyB3En4XdaTGvJTTXR6NVxa3m2dNjs-TOLcfaOpM"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
import pandas as pd

# Page config
st.set_page_config(
    page_title="AI Stock Analysis",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 AI Stock Analysis Agent")
st.markdown("""
Ask me anything about stocks! I'll analyze financial data including income statements,
balance sheets, cash flow, and current prices to provide insights.
""")

tab1, tab2, tab3 = st.tabs(["Text Analysis", "Voice Analysis", "Analytics"])

with tab1:

    # Example queries
    st.markdown("**Try asking:**")
    st.markdown("- *What happened in the latest earnings call of Tesla?*")
    st.markdown("- *Compare Apple and Microsoft*")
    st.markdown("- *What's the financial health of Alphabet Inc?*")
    st.markdown("- *Map the latest quarter performance with what was said in the latest earnings call for Microsoft?*")

    st.divider()

    # User input
    query = st.text_input(
        "Your question:",
        placeholder="e.g., Should I invest in Tesla?",
        help="Ask about any publicly traded US stock"
    )

    # Analyze button
    if st.button("Analyze", type="primary", use_container_width=True):
        if query:
            with st.spinner("Analyzing... "):
                try:
                    # Run async function in sync context
                    result = asyncio.run(agent_triage(query))

                    # Display result
                    st.markdown("### Analysis")
                    st.markdown(result)

                    st.success("Analysis complete!")

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Please try rephrasing your question or try a different stock.")
        else:
            st.warning("Please enter a question")

with tab2:

    st.markdown("**Voice Analysis**")
    st.markdown("*Click the microphone to record your question*")

    audio_value = st.audio_input("Record your question")

    if audio_value:
        st.audio(audio_value)

        with open("temp_recording.wav","wb") as f:
            f.write(audio_value.getbuffer())
        
        with st.spinner("Transcribing your question..."):
            with open("temp_recording.wav", "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model = "whisper-1",
                    file = audio_file
                )

                query_text = transcript.text
            st.success("Transcription Complete!")

            with st.spinner("Analysing stock data..."):
                result_speech = asyncio.run(voice_agent_builder(query_text))

                st.markdown(result_speech)

                st.success("Stock analysis complete")
            
                with st.spinner("Generating a voice response..."):
                    speech_response = client.audio.speech.create(
                        model = "gpt-4o-mini-tts",
                        voice = "nova",
                        input = result_speech,
                        instructions = """You are a helpful stock market assistant that is supposed to be VERY EXCITED
                        when explaining the answer to the user"""
                    )

                    speech_response.stream_to_file("response_audio.mp3")

                    # st.audio(audio_bytes, format = "audio/mp3")

                    st.success("Voice response complete!")

                    with open("response_audio.mp3","rb") as audio_file_1:
                        audio_data = audio_file_1.read()
                        st.audio(audio_data, format = "audio/mpeg")

with tab3:

    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes = SCOPES
        )
    
    except Exception as e:
        creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes = SCOPES)
        
    sheets = build("sheets", "v4", credentials = creds)

    latency = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range = "events!D2:D",
        ).execute()

    values = latency.get('values',)

    latency_report = []

    cleaned_latency = []

    for latency_row in values:
        latency_report.append(latency_row)

    for row in latency_report:
        if row:
            num_str = row[0].replace(',', '')
            cleaned_latency.append(float(num_str))

    df = pd.Series(cleaned_latency)

    average_latency = df.mean()
    p95_latency = df.quantile(0.95)

    st.markdown(f"Average Latency: {average_latency:.2f}")
    st.markdown(f"P95 Latency: {p95_latency: .2f}")

    st.markdown(f"------------")

    cost = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range = "events!E2:E",
        ).execute()
    
    values_1 = cost.get('values',)
    
    cost_report = []
    
    cleaned_cost = []

    for cost_row in values_1:
        cost_report.append(cost_row)

    for row in cost_report:
        if row:
            num_str = row[0].replace(',', '')
            cleaned_cost.append(float(num_str))

    df = pd.Series(cleaned_cost)

    average_cost = df.mean()
    p95_cost = df.quantile(0.95)

    st.markdown(f"Average Cost per query: ${average_cost: 4f}")
    st.markdown(f"P95 Cost per query: ${p95_cost: 4f}")


        

# Footer
st.divider()
st.caption("⚠️ **Disclaimer:** This is AI-generated analysis for educational purposes only, not financial advice.")
st.caption("💡 **Tip:** Be specific with your questions for better results")
st.caption("🔧 **Built with:** OpenAI GPT-4o-Mini, Alpha Vantage API, Streamlit")
