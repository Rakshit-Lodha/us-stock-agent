import requests
from openai import OpenAI
import json
from dotenv import load_dotenv
load_dotenv()
import os
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
from agents import Agent, Runner, function_tool, ModelSettings, SQLiteSession

from functools import lru_cache

from tools import (
    find_ticker,
    price_data,
    get_income_statement,
    get_balance_sheet,
    cash_flow_statement,
    earnings_analysis
)

global_session = SQLiteSession("test_conversation")


async def _agent_builder(query):

    agent = Agent(
        name = "Data Finder",
        model = 'gpt-4o-mini',
        instructions = f"""
        You are a stock analyser and your job is to understand the {query} and then use the tools available at your disposal 
        to answer to the user. 

        Make sure that you ONLY get data from tools and in case the query cannot be solved by tools, empathetically refuse to answer
        the user query. 

        It is recommended you use tables, if you're doing any comparison either between 2 or more companies or you're 
        showing the data of more than 1 year. 

        You can use the {earnings_analysis} tool in case the user wants to know what happened in the latest earnings call of a particular
        company.

        However, you should always try to back it up with financial data first. 
        
        EXCEPTION:
        If the user is specifically asking to summarise the earning call data you are supposed to simply just print out
        the output you're getting from {earnings_analysis}.
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
            temperature = 0.3
        )
    )

    result = await Runner.run(agent, query, session = global_session)

    return result.final_output