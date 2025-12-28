import streamlit as st
import asyncio
from agent import _agent_builder  # Import your agent function

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

# Footer
st.divider()
st.caption("⚠️ **Disclaimer:** This is AI-generated analysis for educational purposes only, not financial advice.")
st.caption("💡 **Tip:** Be specific with your questions for better results")
st.caption("🔧 **Built with:** OpenAI GPT-4.1, Alpha Vantage API, Streamlit")