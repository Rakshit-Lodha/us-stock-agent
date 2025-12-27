import os
import requests
from functools import lru_cache
from agents import function_tool
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))


# API setup
stock_api = os.getenv("ALPHA_VANTAGE_API_KEY")
url = "https://www.alphavantage.co/query"

@function_tool
def find_ticker(text: str) -> str:
    """Based on the natural language query, use this function to find the ticker symbol"""

    # params = {
    #     "function": "SYMBOL_SEARCH",
    #     "keywords": text,
    #     "apikey": stock_api
    # }

    # response = requests.get(url, params)

    # data = response.json()

    # ticker = (data.get('bestMatches')[0]).get('1. symbol')

    return _find_ticker(text)


@lru_cache(maxsize = 100)
def _find_ticker(text: str) -> str:
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": text,
        "apikey": stock_api
    }

    response = requests.get(url, params)

    data = response.json()

    ticker = data.get('bestMatches')

    filter_region = []

    for t in ticker:
        if t.get('4. region') == 'United States':
            filter_region.append(t)

    return filter_region[0].get('1. symbol')


@function_tool
def get_income_statement(ticker: str) -> str:
    """Based on the ticker you can find the income statement of the company from this
    function. This will fetch both quarterly and annual income statements.
    """
    # params = {
    #     "function": "INCOME_STATEMENT",
    #     "symbol": ticker,
    #     "apikey": stock_api
    # }

    # income_statement = requests.get(url,params)

    # income_statement_data = income_statement.json()

    # annual_data = income_statement_data.get('annualReports')

    # filtered_data = []

    # for report in annual_data:
    #     filtered_data.append({
    #         'fiscalDateEnding': report.get('fiscalDateEnding'),
    #         'grossProfit': report.get('grossProfit'),
    #         'totalRevenue': report.get('totalRevenue'),
    #         'costOfRevenue': report.get('costOfRevenue'),
    #         'costofGoodsAndServicesSold': report.get('costofGoodsAndServicesSold'),
    #         'operatingIncome': report.get('operatingIncome'),
    #         'operatingExpenses': report.get('operatingExpenses'),
    #         'researchAndDevelopment': report.get('researchAndDevelopment'),
    #         'sellingGeneralAndAdministrative': report.get('sellingGeneralAndAdministrative'),
    #         'netInterestIncome': report.get('netInterestIncome'),
    #         'interestIncome': report.get('interestIncome'),
    #         'depreciationAndAmortization': report.get('depreciationAndAmortization'),
    #         'incomeBeforeTax': report.get('incomeBeforeTax'),
    #         'incomeTaxExpense': report.get('incomeTaxExpense'),
    #         'ebit': report.get('ebit'),
    #         'ebitda': report.get('ebitda'),
    #         'netIncome': report.get('netIncome'),
    #     })

    return _get_income_statement(ticker)


@lru_cache(maxsize = 100)
def _get_income_statement(ticker: str) -> str:
    """Based on the ticker you can find the income statement of the company from this
    function. This will fetch both quarterly and annual income statements.
    """

    params = {
        "function": "INCOME_STATEMENT",
        "symbol": ticker,
        "apikey": stock_api
    }

    income_statement = requests.get(url,params)

    income_statement_data = income_statement.json()

    annual_data = income_statement_data.get('annualReports')

    filtered_data = []

    for report in annual_data:
        filtered_data.append({
            'fiscalDateEnding': report.get('fiscalDateEnding'),
            'grossProfit': report.get('grossProfit'),
            'totalRevenue': report.get('totalRevenue'),
            'costOfRevenue': report.get('costOfRevenue'),
            'costofGoodsAndServicesSold': report.get('costofGoodsAndServicesSold'),
            'operatingIncome': report.get('operatingIncome'),
            'operatingExpenses': report.get('operatingExpenses'),
            'researchAndDevelopment': report.get('researchAndDevelopment'),
            'sellingGeneralAndAdministrative': report.get('sellingGeneralAndAdministrative'),
            'netInterestIncome': report.get('netInterestIncome'),
            'interestIncome': report.get('interestIncome'),
            'depreciationAndAmortization': report.get('depreciationAndAmortization'),
            'incomeBeforeTax': report.get('incomeBeforeTax'),
            'incomeTaxExpense': report.get('incomeTaxExpense'),
            'ebit': report.get('ebit'),
            'ebitda': report.get('ebitda'),
            'netIncome': report.get('netIncome'),
        })

    return filtered_data


@function_tool
def get_balance_sheet(ticker: str) -> str:
    """Based on the ticker you can find the balance sheet of the company from this
    function. This will fetch both quarterly and annual income statements.
    """

    # params = {
    #     "function": "BALANCE_SHEET",
    #     "symbol": ticker,
    #     "apikey": stock_api
    # }

    # balance_sheet = requests.get(url,params)

    # balance_sheet_data = balance_sheet.json()

    # annual_data = balance_sheet_data.get('annualReports')

    # filtered_data = []

    # for report in annual_data:
    #     filtered_data.append({
    #         'fiscalDateEnding': report.get('fiscalDateEnding'),
    #         'totalAssets': report.get('totalAssets'),
    #         'totalCurrentAssets': report.get('totalCurrentAssets'),
    #         'cashAndCashEquivalentsAtCarryingValue': report.get('cashAndCashEquivalentsAtCarryingValue'),
    #         'inventory': report.get('inventory'),
    #         'totalNonCurrentAssets': report.get('totalNonCurrentAssets'),
    #         'accumulatedDepreciationAmortizationPPE': report.get('accumulatedDepreciationAmortizationPPE'),
    #         'sellingGeneralAndAdministrative': report.get('sellingGeneralAndAdministrative'),
    #         'totalLiabilities': report.get('totalLiabilities'),
    #         'interestIncome': report.get('interestIncome'),
    #         'totalCurrentLiabilities': report.get('totalCurrentLiabilities'),
    #         'currentLongTermDebt': report.get('currentLongTermDebt'),
    #         'totalShareholderEquity': report.get('totalShareholderEquity'),
    #         'retainedEarnings': report.get('retainedEarnings'),
    #     })

    return _get_balance_sheet(ticker)


@lru_cache
def _get_balance_sheet(ticker: str) -> str:

    params = {
        "function": "BALANCE_SHEET",
        "symbol": ticker,
        "apikey": stock_api
    }

    balance_sheet = requests.get(url,params)

    balance_sheet_data = balance_sheet.json()

    annual_data = balance_sheet_data.get('annualReports')

    filtered_data = []

    for report in annual_data:
        filtered_data.append({
            'fiscalDateEnding': report.get('fiscalDateEnding'),
            'totalAssets': report.get('totalAssets'),
            'totalCurrentAssets': report.get('totalCurrentAssets'),
            'cashAndCashEquivalentsAtCarryingValue': report.get('cashAndCashEquivalentsAtCarryingValue'),
            'inventory': report.get('inventory'),
            'totalNonCurrentAssets': report.get('totalNonCurrentAssets'),
            'accumulatedDepreciationAmortizationPPE': report.get('accumulatedDepreciationAmortizationPPE'),
            'sellingGeneralAndAdministrative': report.get('sellingGeneralAndAdministrative'),
            'totalLiabilities': report.get('totalLiabilities'),
            'interestIncome': report.get('interestIncome'),
            'totalCurrentLiabilities': report.get('totalCurrentLiabilities'),
            'currentLongTermDebt': report.get('currentLongTermDebt'),
            'totalShareholderEquity': report.get('totalShareholderEquity'),
            'retainedEarnings': report.get('retainedEarnings'),
        })

    return filtered_data


@function_tool
def cash_flow_statement(ticker: str) -> str:
    """Based on the ticker found out using the function find_ticker(text) you can find the balance sheet of the company from this
    function. This will fetch both quarterly and annual cash flow statement.
    """

    # params = {
    #     "function": "CASH_FLOW",
    #     "symbol": ticker,
    #     "apikey": stock_api
    # }

    # cash_flow = requests.get(url,params)

    # cash_flow_data = cash_flow.json()

    # annual_filter = cash_flow_data.get('annualReports')

    # final_cash_flow_data = []

    # for cash_flow in annual_filter:
    #     final_cash_flow_data.append({
    #         'fiscalDateEnding': cash_flow.get('fiscalDateEnding'),
    #         'operatingCashflow': cash_flow.get('operatingCashflow'),
    #         'cashflowFromInvestment': cash_flow.get('cashflowFromInvestment'),
    #         'cashflowFromFinancing': cash_flow.get('cashflowFromFinancing'),
    #         'netIncome': cash_flow.get('netIncome')
    #     })

    return _cash_flow_statement(ticker)


@lru_cache
def _cash_flow_statement(ticker: str) -> str:
    """Based on the ticker found out using the function find_ticker(text) you can find the balance sheet of the company from this
    function. This will fetch both quarterly and annual cash flow statement.
    """

    params = {
        "function": "CASH_FLOW",
        "symbol": ticker,
        "apikey": stock_api
    }

    cash_flow = requests.get(url,params)

    cash_flow_data = cash_flow.json()

    annual_filter = cash_flow_data.get('annualReports')

    final_cash_flow_data = []

    for cash_flow in annual_filter:
        final_cash_flow_data.append({
            'fiscalDateEnding': cash_flow.get('fiscalDateEnding'),
            'operatingCashflow': cash_flow.get('operatingCashflow'),
            'cashflowFromInvestment': cash_flow.get('cashflowFromInvestment'),
            'cashflowFromFinancing': cash_flow.get('cashflowFromFinancing'),
            'netIncome': cash_flow.get('netIncome')
        })

    return final_cash_flow_data



@function_tool
def price_data(ticker: str) -> str:
    """ 
    Based on the ticker, we need to find the price of the stock through this.
    """

    # params = {
    #     "function": "TIME_SERIES_DAILY",
    #     "symbol": ticker,
    #     "outputsize": "compact",
    #     "apikey": stock_api
    # }

    # response = requests.get(url,params)

    # response_json = response.json()

    # filtered_json = response_json['Time Series (Daily)']

    # close_price = []

    # for date, values in filtered_json.items():
    #     close_price.append(
    #         {
    #             'date': date,
    #             'close': values['4. close']
    #         }
    #     )

    # latest_price = close_price[0]

    return _price_data(ticker)


@lru_cache
def _price_data(ticker: str) -> str:
    """ 
    Based on the ticker, we need to find the price of the stock through this.
    """

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "compact",
        "apikey": stock_api
    }

    response = requests.get(url,params)

    response_json = response.json()

    filtered_json = response_json['Time Series (Daily)']

    close_price = []

    for date, values in filtered_json.items():
        close_price.append(
            {
                'date': date,
                'close': values['4. close']
            }
        )

    latest_price = close_price[0]

    return latest_price


@function_tool
def earnings_analysis(ticker: str) -> str:
    """ 
    Based on the ticker, you will find a 10-12 point analysis related to the latest earnings report. 
    You can use it in case the user wants to do some kind of qualitative analysis
    """

    return _earnings_analysis(ticker)

@lru_cache
def _earnings_analysis(ticker: str) -> str:
    """
    Based on the ticker, you will find a 10-12 point analysis related to the latest earnings report. 
    You can use it in case the user wants to do some kind of qualitative analysis
    """

    final_transcript = []

    final_quarter = []

    while final_transcript == []:
        today = datetime.now()
    
        year = today.year
        month = today.month
    
        if month in [1,2,3]:
            quarter = 'Q4'
            year -= 1
        elif month in [4,5,6]:
            quarter = 'Q1'
        elif month in [7,8,9]:
            quarter = 'Q2'
        else:
            quarter = 'Q3'
    
        final = f'{year}{quarter}'
    
        params = {
            "function": "EARNINGS_CALL_TRANSCRIPT",
            "symbol": ticker,
            "apikey": stock_api,
            "quarter": final
        }

        response = requests.get(url, params)

        final_json = response.json()

        transcript = final_json.get('transcript')

        quarter = final_json.get('quarter')

        final_transcript.append(transcript)

        final_quarter.append(quarter)

    
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": f""" 
           You will be given the full earnings call transcript in {final_transcript}.

            Your task is to extract **7–10 investor-relevant insights** strictly based on what 
            **Apple management said** in the transcript.
            
            Rules you MUST follow:
            1. Use ONLY information explicitly stated by Apple executives (CEO, CFO, or Investor Relations).  
               Do NOT include analyst opinions, assumptions, or external interpretation.
            2. Each point must represent a **distinct insight**, not a restatement of another point.
            3. For every point, clearly mention **who said it** (name + role).
            4. Do NOT use generic phrases such as “strong performance”, “positive outlook”, or “solid results” 
            unless backed by specific data or commentary.
            5. Each point must explain **why this matters to a long-term investor** 
            (growth, margins, cash flow, competitive position, or strategic direction).
            6. Prefer **synthesis over repetition** — combine numbers with management commentary where relevant.
            7. Do NOT introduce any facts, estimates, or forward views not explicitly stated in the transcript.
            
            Output format:
            - Heading: Analysis of the earnings call ({final_quarter})
            - Numbered list (7–10 points)
            - 2–4 sentences per point
            - End each point with: *(Source: Name, Title)*
            
            Tone:
            - Analytical
            - Investor-oriented
            - Neutral and factual

            Don't only include positive or negative points, try to include both
            """}
        ], temperature = 0.3
    )

    return response.choices[0].message.content