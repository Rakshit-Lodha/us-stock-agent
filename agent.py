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
    cash_flow_statement
)

global_session = SQLiteSession("test_conversation")


async def _agent_builder(query):

    agent = Agent(
        name = "Data Finder",
        # model = 'gpt-4o-mini',
        instructions = f"""
        You are a stock analyser and your job is to understand the {query} and then use the tools available at your disposal 
        to answer to the user. 

        Make sure that you ONLY get data from tools and in case the query cannot be solved by tools, empathetically refuse to answer
        the user query. 

        It is recommended you use tables, if you're doing any comparison either between 2 or more companies or you're 
        showing the data of more than 1 year. 
        """,
        tools = [
            price_data,
            cash_flow_statement,
            find_ticker,
            get_balance_sheet,
            get_income_statement,
        ],
        model_settings = ModelSettings(
            tool_choice = "auto",
            seed = 0,
            temperature = 0.3
        )
    )

    result = await Runner.run(agent, query, session = global_session)

    return result.final_output