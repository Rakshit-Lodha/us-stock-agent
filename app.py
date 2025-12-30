import streamlit as st
import asyncio
from agent import _agent_builder
from agent import voice_agent_builder
import os
from openai import OpenAI
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

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

tab1, tab2 = st.tabs(["Text Analysis", "Voice Analysis"])

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
                    result = asyncio.run(_agent_builder(query))

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

                st.success("Stock analysis complete")
            
                with st.spinner("Generating a voice response..."):
                    speech_response = client.audio.speech.create(
                        model = "gpt-4o-mini-tts",
                        voice = "nova",
                        input = result_speech,
                        instructions = """You are a helpful stock market assistant that is supposed to be VERY EXCITED
                        when explaining the {input} to the user"""
                    )

                    audio_bytes = speech_response.content

                    st.audio(audio_bytes, format = "audio/mp3")

                    st.success("Voice response complete!")



        

# Footer
st.divider()
st.caption("⚠️ **Disclaimer:** This is AI-generated analysis for educational purposes only, not financial advice.")
st.caption("💡 **Tip:** Be specific with your questions for better results")
st.caption("🔧 **Built with:** OpenAI GPT-4.1, Alpha Vantage API, Streamlit")
