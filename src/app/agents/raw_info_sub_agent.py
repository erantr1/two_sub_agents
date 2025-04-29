from typing import Optional, List, Callable
import typing

from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, Body
import os
import requests

from src.utils import get_headers_and_params, SearchParameters

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()


def extract_search_params(raw_info_sub_task):
    # Use LLM to extract structured parameters
    instructions = """
    Extract search parameters from the input.
    Return a JSON with these fields, when possible:
    - location: the city or area
    - timeframe: when the events should take place
    """
    # - event_types: types of events mentioned
    # - preferences: specific preferences or requirements

    response = client.responses.parse(
        model="gpt-4o",
        input=raw_info_sub_task,
        instructions=instructions,
        text_format=SearchParameters
    )
    return response

@app.post("/api/raw-info")
def get_raw_info(raw_info_sub_task_mcp: dict = Body(...)):
    print(f"Endpoint called with: {raw_info_sub_task_mcp}")

    events_url = "https://public-api.eventim.com/websearch/search/api/exploration/v2/productGroups"

    extracted_params = extract_search_params(raw_info_sub_task_mcp["content"]).output[0].content[0].parsed
    print(f'**** extracted: {extracted_params}')
    print(type(extracted_params))

    params, headers = get_headers_and_params(extracted_params)

    response = requests.get(events_url, params=params, headers=headers)
    return response.json()
