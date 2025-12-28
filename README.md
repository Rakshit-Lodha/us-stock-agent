# AI Stock Analysis Agent V1.1

An intelligent stock analysis system that provides comprehensive financial insights by analyzing real-time data from Alpha Vantage API.

🚀 **[Live Demo](https://us-stock-agent.streamlit.app/)**

---

## Overview

This AI agent analyzes US stocks by processing income statements, balance sheets, cash flow statements, and current market data to deliver clear, data-driven investment insights. Unlike basic financial tools that simply display raw data, this agent synthesizes multiple data sources to provide contextual analysis and comparative insights.

Built as a demonstration of production-grade AI agent development, combining large language models with structured financial data APIs.

---

## Features

### Comprehensive Financial Analysis
- **Income Statements**: Revenue, profitability, operating expenses, EBITDA
- **Balance Sheets**: Assets, liabilities, equity, cash reserves
- **Cash Flow**: Operating cash flow, investing activities, financing activities
- **Current Pricing**: Real-time stock prices and trading data

### Quarterly Earnings Call Analysis
- Find out the summary from the latest earnings call

### Multi-Stock Comparison
- Side-by-side financial comparisons with formatted tables
- Growth trend analysis across multiple companies
- Risk/reward profiling for investment decisions

### Intelligent Agent Architecture
- Autonomous tool selection based on query type
- Multi-step reasoning for complex questions
- Natural language understanding of investment queries
- Structured output with tables, sections, and summaries
- Built in memory per chat session

---

## Example Queries

**Single Stock Analysis:**
```
"Give me details about Tesla"
"Is Apple overvalued?"
"What's the financial health of Microsoft?"
```

**Comparative Analysis:**
```
"Compare Apple and Microsoft"
"Should I invest in Google or Amazon?"
"Oracle vs Salesforce - which is better?"
```

**Investment Recommendations:**
```
"Should I invest in Tesla?"
"Is Alphabet a good buy right now?"
"What are the risks of investing in NVIDIA?"
```

---

## Tech Stack

### Core Technologies
- **AI Framework**: OpenAI GPT-4.1 (agent-based architecture)
- **Financial Data**: Alpha Vantage API
- **Deployment**: Streamlit Cloud
- **Language**: Python 3.11+

### Key Libraries
- `openai-agents`: Agent orchestration and tool calling
- `streamlit`: Web interface
- `requests`: API integration
- `python-dotenv`: Environment management

### Agent Architecture
- **Multi-tool orchestration**: Agent autonomously selects which financial APIs to call
- **Caching layer**: LRU cache for API response optimization
- **Error handling**: Graceful degradation for API failures
- **Seed-based reproducibility**: Consistent outputs for testing

---

## Project Structure
```
stock-analysis-agent/
├── app.py              # Streamlit web interface
├── agent.py            # AI agent logic and orchestration
├── tools.py            # Financial API integration (Alpha Vantage)
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

---

## How It Works

1. **User Query**: Natural language question about stocks
2. **Agent Reasoning**: GPT-4.1 determines which financial data is needed
3. **Tool Execution**: Agent calls relevant APIs (ticker search, financials, pricing)
4. **Data Synthesis**: Agent analyzes data across multiple statements
5. **Response Generation**: Structured output with tables, insights, and recommendations

**Example Flow:**
```
Query: "Compare Tesla and Ford"
  ↓
Agent calls: find_ticker("Tesla") → TSLA
             find_ticker("Ford") → F
             get_income_statement(TSLA)
             get_income_statement(F)
             get_balance_sheet(TSLA)
             get_balance_sheet(F)
             price_data(TSLA)
             price_data(F)
  ↓
Agent synthesizes comparative analysis
  ↓
Output: Formatted tables + insights + recommendation
```

---

## API Integration

### Alpha Vantage Functions Used
- `SYMBOL_SEARCH`: Convert company names to ticker symbols
- `INCOME_STATEMENT`: Annual financial performance data
- `BALANCE_SHEET`: Asset and liability statements
- `CASH_FLOW`: Cash flow statements
- `TIME_SERIES_DAILY`: Current stock prices

### Rate Limiting & Optimization
- **Free tier limit**: 25 API calls/day
- **Caching strategy**: LRU cache with 100-item capacity
- **Efficiency**: ~4-5 API calls per unique stock analysis
- **Result**: ~5-7 unique stock analyses per day with caching

---

## Sample Output

**Query**: "Should I invest in Alphabet or Tesla? What would you say?"

**Response includes:**
- Stock price comparison table
- Key balance sheet metrics (assets, liabilities, equity, cash)
- Cash flow & profitability comparison
- Recent growth trends (2022-2024)
- Summary table (market cap, profitability, cash reserves, growth, risk)
- Investment conclusion with balanced recommendation
- Disclaimer about analysis vs. financial advice

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