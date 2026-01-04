# AI Stock Analysis Agent V2

A multi-agent stock analysis system with voice interface, achieving 90% accuracy through systematic evaluation and specialised agent handoffs.

🚀 **[Live Demo](https://us-stock-agent.streamlit.app/)**

---

## What Makes This Different

Most stock analysis tools just display raw data. This system:
- **Understands natural language** queries about stocks
- **Orchestrates multiple specialists** via agent handoffs
- **Analyzes comprehensively** across income, balance, cash flow, and earnings
- **Works via voice** - ask questions by speaking
- **Validates quality** through systematic evaluation (90% accuracy)

Built as a demonstration of:
- Multi-agent AI architecture with specialized handoffs
- Voice-enabled financial analysis
- Data-driven optimization (improved from 58% → 90% accuracy)
- Production deployment with comprehensive testing

---

### Voice Interface
- **Speech-to-text**: Ask questions by speaking
- **Text-to-speech**: Get analysis read aloud
- **Use cases**: Hands-free analysis while driving, multitasking

### Multi-Agent Architecture
- **Triage Agent**: Routes queries to appropriate specialist
- **Financial Data Agent**: Income statements, balance sheets, cash flow
- **Qualitative Agent**: Earnings calls, management commentary
- **Full Analysis Agent**: Comprehensive multi-statement analysis

### Comprehensive Analysis
- **Financial statements**: All three statements (income, balance, cash flow)
- **Earnings insights**: Management commentary from quarterly calls
- **Multi-company comparison**: Side-by-side analysis with tables
- **Current pricing**: Real-time stock data

### Quality Assurance
- **Evaluation framework**: 20+ test cases across 5 categories
- **Measured accuracy**: 90% tool usage accuracy
- **Systematic testing**: Validates every major query type
- **Data-driven optimization**: Improved through eval-driven redesign


## Architecture

### Multi-Agent System with Handoffs
```
User Query (Text or Voice)
    ↓
Triage Agent (Router)
    ├─→ Financial Data Agent
    │   Tools: income_statement, balance_sheet, cash_flow, price_data
    │   
    ├─→ Qualitative Agent
    │   Tools: earnings_analysis
    │   
    └─→ Full Analysis Agent
        Tools: All of the above
        Use: Comprehensive multi-statement analysis
```

**Why multi-agent?**
- Single agent with 6 tools: 58% accuracy 
- Multi-agent with specialized roles: 90% accuracy 

### Voice Pipeline
```
User speaks
    ↓
OpenAI Whisper (speech-to-text)
    ↓
Agent processes query
    ↓
OpenAI TTS (text-to-speech)
    ↓
Audio response plays
```

---

## Evaluation Results

### Before (V1 - Single Agent)
- Income Statement queries: 40% accuracy
- Cash Flow queries: 33% accuracy
- Earnings queries: 66% accuracy
- **Overall: 58% accuracy**

### After (V2 - Multi-Agent)
- Income Statement queries: 80% accuracy (+40pp)
- Cash Flow queries: 100% accuracy (+67pp)
- Earnings queries: 100% accuracy (+34pp)
- **Overall: 90% accuracy (+32pp)**

**Key improvement:** Cash flow coverage went from 33% to 100% through specialized agent architecture.

## How Quality is Validated

### Evaluation Framework

**Test Categories (20 tests total):**
1. **Income Statement** (5 tests): Revenue, profit, expense queries
2. **Balance Sheet** (4 tests): Cash, debt, asset queries  
3. **Cash Flow** (3 tests): Operating CF, CapEx, FCF queries
4. **Earnings Analysis** (3 tests): Management commentary, guidance
5. **Complex Queries** (5 tests): Multi-statement comprehensive analysis

**Methodology:**
- OpenAI's trace evaluation framework
- Validates correct tool usage for each query type
- Measures before/after accuracy
- Documents improvement systematically

**Results:**
- V1 (single agent): 58% overall accuracy
- V2 (multi-agent): 90% overall accuracy
- **+32 percentage point improvement**

---

## Example Queries

### Financial Analysis
```
"What is Apple's revenue?"
"Compare Tesla and Ford's profitability"
"Show me Microsoft's cash flow over the last 5 years"
```

### Earnings Insights
```
"What happened in Google's latest earnings call?"
"What did Amazon's management say about AWS?"
"Latest guidance from Microsoft"
```

### Comprehensive Analysis
```
"Give me a full analysis of Amazon"
"Should I invest in Tesla based on fundamentals?"
"Is Nvidia overvalued?"
```

### Voice Queries
*Click microphone and speak:*
```
"Tell me about Apple's financial health"
"What's the latest on Google's earnings?"
"Compare Microsoft and Oracle"
```

---

## Sample Output

**Query:** "Give me a full analysis of Amazon"

**Agent workflow:**
1. Triage Agent routes to Full Analysis Agent
2. Full Analysis Agent calls:
   - `find_ticker("Amazon")` → AMZN
   - `get_income_statement("AMZN")`
   - `get_balance_sheet("AMZN")`
   - `cash_flow_statement("AMZN")`
   - `earnings_analysis("AMZN")`
3. Synthesizes comprehensive analysis

**Output includes:**
- Income statement table (5 years)
- Balance sheet table (5 years)
- Cash flow analysis
- Latest earnings call insights (10 key points)
- Overall investment perspective
- Risk/opportunity assessment

---

## Local Development

### Prerequisites
- Python 3.11+
- OpenAI API key
- Alpha Vantage API key (free tier)

### Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/stock-analysis-agent.git
cd stock-analysis-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "OPENAI_API_KEY=your_key_here" > .env
echo "ALPHA_VANTAGE_API_KEY=your_key_here" >> .env

# Run locally
streamlit run app.py
```

---

## Deployment

Deployed on Streamlit Cloud with environment variables configured in secrets management.

**Live URL**: https://us-stock-agent.streamlit.app/

---

## Limitations & Disclaimer

### Current Limitations
- **Data scope**: US stocks only (Alpha Vantage constraint)
- **Rate limits**: 25 API calls/day on free tier (5-7 unique stocks)

### Important Disclaimer
⚠️ **This is an AI-powered analysis tool for educational purposes only, not financial advice.**

- Always conduct your own due diligence
- Consult with licensed financial advisors
- Past performance doesn't guarantee future results
- AI analysis may contain errors or biases

---