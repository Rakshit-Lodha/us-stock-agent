import os
import requests
from functools import lru_cache
from agents import function_tool

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