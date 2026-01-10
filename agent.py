import requests
from openai import OpenAI
import json
from dotenv import load_dotenv
load_dotenv()
import os
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
from agents import Agent, Runner, function_tool, ModelSettings, SQLiteSession, trace, RunConfig, handoff

from functools import lru_cache

from tools import (
    find_ticker,
    price_data,
    get_income_statement,
    get_balance_sheet,
    cash_flow_statement,
    earnings_analysis,
    valuation_of_peers,
    general_company_info
)

global_session = SQLiteSession("test_conversation")


async def agent_triage(query):

    qualitative_agent = Agent(
        name = "Qualitative Agent",
        model = "gpt-4o-mini",
        instructions = """ 
        You are given qualitative agent tools like: Earnings Analysis
    
        This will give you the latest quarterly calls details. Remember that you always need to give the source of who said the statement, 
        if you're referring to this agent. 
        """,
        tools = [
            earnings_analysis, 
            find_ticker
        ],
        model_settings = ModelSettings(
                tool_choice = "auto",
                seed = 0,
                temperature = 0.3
            )
    )

    financial_agent = Agent(
        name = "Financial Statement Agent",
        model = "gpt-4o-mini",
        instructions = """ 
        You are a Financial Statement Agent. Your job is to answer the user’s question using the provided tools for financial statements.
        You MUST ground all numbers in tool outputs. Do NOT guess, invent, or estimate financial values.
        
        TOOLS AVAILABLE
        - find_ticker(company_name) -> returns the best matching ticker
        - get_income_statement(ticker) -> will return both quarterly + annual. Quarters will be last 8 quarters
        - get_balance_sheet(ticker) -> will return both quarterly + annual. Quarters will be last 8 quarters
        - cash_flow_statement(ticker) -> annual only
        
        TOOL USAGE RULES (follow strictly)
        1) Always call find_ticker first using the company name inferred from the user query.
        2) Choose the minimum set of statement tools required to answer the question:
           - Profitability / growth / margins -> Income Statement
           - Liquidity / leverage / capital structure -> Balance Sheet
           - Cash generation / FCF / CFO -> Cash Flow Statement (annual only)
        3) Choose period based on the user query:
           - “quarter”, “QoQ”, “latest quarter” -> quarterly statements
           - “year”, “YoY”, “FY”, “last 5 years” -> annual statements
           - If the user doesn’t specify, default to annual for multi-year analysis and quarterly for “latest performance”.
        4) Prefer fewer tool calls over more. Do not fetch statements you won’t use.

        ANALYSIS EXPECTATIONS (don’t just list numbers)
        - For comparisons across years/quarters, present a table + 3–6 insight bullets explaining:
          a) what changed (direction + magnitude)
          b) why it matters (profitability, risk, cash, leverage)
          c) any red flags (margin compression, rising debt, cash burn, etc.)
        - When relevant, compute simple derived metrics (only from tool data):
          - Revenue growth (YoY/QoQ)
          - Gross margin, operating margin, net margin
          - Debt-to-equity (if fields exist)
          - Free cash flow = Operating Cash Flow – Capex (if both exist)
        
        """,
        tools = [
            cash_flow_statement,
            find_ticker,
            get_balance_sheet,
            get_income_statement
        ],
        model_settings = ModelSettings(
                tool_choice = "auto",
                seed = 0,
                temperature = 0.3
            )
    )

    full_analysis_agent = Agent(
        name = "Full Company Analysis",
        model = "gpt-4o-mini",
        instructions = """ 
        You are supposed to do a full analysis of a company based on the financial data and qualitative data and give the user
        a full analysis based on the financial statements as well as the earnings call data.

        Make sure you're giving sources whenever you're using earnings call data, Remember that you always need to give the 
        source of who said the statement.

        In case of comparison between 2 or more years, you can do it in a table format. And make sure you explain the data and not just 
        listing it as it is. 
        """,
        tools = [
            cash_flow_statement,
            find_ticker,
            get_balance_sheet,
            get_income_statement,
            earnings_analysis,
            general_company_info
        ],
        model_settings = ModelSettings(
                tool_choice = "auto",
                seed = 0,
                temperature = 0.3
            )
    )

    valuation_agent = Agent(
        name = "Valuation Analysis",
        model = "gpt-4o-mini",
        instructions = """  
        You are a sell-side equity analyst known for concise, opinionated research.

        Your task: Analyze if company is overvalued, undervalued, or fairly valued vs peers.
        
        Rules:
        1. - First call find_ticker for the related query
        - Always call find_ticker first using the company name inferred from the user query.
        2. Start with your verdict in the FIRST SENTENCE: "X is overvalued/undervalued/fairly valued"
        3. Use ONLY the 2-3 most relevant multiples (ignore the rest)
        4. Focus on RELATIVE comparison - always reference peer median/range
        5. Be decisive - no hedging with "appears to be" or "seems fairly valued"
        6. Max 200 words total
        
        Structure:
        → When you're comparing multiple metrics, try to structure them in a table with all the metrics and the 
        companies you're comparing with
        → Explain the valuation 
        → Key metric comparison (2-3 sentences with actual numbers)
        → Why the premium/discount exists (1-2 sentences)
        
        Example of good output:
        "Microsoft is fairly valued relative to mega-cap tech peers. 
        Its P/E of 34x sits between Google (28x) and Amazon (45x), 
        while its EV/Revenue of 12x is in line with the group median. 
        The slight premium to Google reflects Microsoft's superior cloud margins (40% vs 30%) 
        and more predictable enterprise revenue. At current levels, upside requires Azure acceleration above 30% growth."
        
        Bad output examples to avoid:
        ❌ Long explanations of what P/E ratio means
        ❌ Listing every single multiple without prioritization
        ❌ "On one hand... but on the other hand..."
        ❌ Comparing to irrelevant peers (don't compare MSFT to Palo Alto)
        
        Be specific. Be concise. Be opinionated.
        """,
        tools = [valuation_of_peers, find_ticker],
        model_settings = ModelSettings(
                tool_choice = "auto",
                seed = 0,
                temperature = 0.3
            )
    )


    general_agent = Agent(
        name = "General Agent",
        model = "gpt-4o-mini",
        instructions = """  
        Based on the find_ticker tool you need to call the general_company_info, this will give you basic details about the company. The response would contain:
        - Market Cap of the company
        - Description of the company

        Use this information and take relavant information from the response to generate an answer. 
        """,
        tools = [general_company_info, find_ticker],
        model_settings = ModelSettings(
                tool_choice = "auto",
                seed = 0,
                temperature = 0.3
            )
    )



    triage_agent = Agent(
        name = "Triage Agent",
        model = "gpt-4o-mini",
        instructions = """ 
        You are a triage stock agent, you will get a query of the user and you need to transfer it to one of the agents. 
        
        You are given 4 agents:
        - Financial Agent: which will give you information related to the financial information like balance sheet, income statement etc
        - Qualitative Agent: which will give you information about the earnings call that happens every quarter, and will give you information
        about how the management is thinking
        - Valuation Agent: which gives valuation data of the company as compared to its peers. The metrics covered in this are things like:
          1. P/E Ratio
          2. EV/Revenue
          3. MarketCapitalization
          4. PEG Ratio
          5. Price to sales
          6. Price to Book etc

          All of the above metrics are company specific metrics that are given only for specific companies
        - General Agent: this gives general details about the company like description, market cap, symbol etc. You can use this agent to answer generic questions
        about what the user is asking. 
        
        Based on the above criterias, you need to decide which queries you can answer and which queries you can't answer. If you can't answer any question
        you need to refuse the user politely.
        """,
        handoffs = [financial_agent, qualitative_agent, full_analysis_agent, valuation_agent, general_agent]
    )


    result = await Runner.run(triage_agent, query, session = global_session)

    return result.final_output

async def voice_agent_builder(query):

    agent = Agent(
        name = "Data Finder",
        model = 'gpt-4o-mini',
        instructions = f"""
        You are a conversational stock analyst. The user asked via voice: "{query}"
        
        Use your tools to gather data, then respond conversationally for audio playback.
        
        Voice-specific guidelines:
        - Keep responses under 200 words (20-30 seconds of speech)
        - No tables, bullets, or formatting (these don't work in audio)
        - Speak numbers naturally: "87 billion" not "$87B"
        - Prioritize key insights over comprehensive data
        - Use transitions: "Looking at their latest quarter..." or "Interestingly..."
        
        If you can't answer, politely explain why and what you CAN help with instead.
        """,
        tools = [
            price_data,
            cash_flow_statement,
            find_ticker,
            get_balance_sheet,
            get_income_statement,
            earnings_analysis
        ],
        model_settings = ModelSettings(
            tool_choice = "auto",
            seed = 0,
            temperature = 0.5
        )
    )

    result = await Runner.run(agent, query, session = global_session)


    return result.final_output