from typing import Optional, List, Callable
import typing

from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, Body
from datetime import datetime
from langfuse.decorators import observe
import os
import requests

from src.utils import get_headers_and_params, SearchParameters, cities_dict

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()


class Dates(BaseModel):
    start_date: str
    end_date: str


@observe()
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


@observe()
def get_dates(timeframe, location):
    today = datetime.today().strftime("%B %d, %Y")
    instructions = f"""
        Given a time expression like "next week", "upcoming weekend" or "tomorrow", return the corresponding date range.
        Assume today is {today}, and the user is located in {location} (note that in some countries weekends are Friday–Saturday, while in others they're Saturday–Sunday).
        Return both a start and end date in ISO 8601 format (YYYY-MM-DD).
        If the expression refers to a single day, the start and end dates should be identical.
        Strictly return dates exactly in YYYY-MM-DD format, without any additional text or formatting.
    """
    response = client.responses.parse(
        model="gpt-4o",
        instructions=instructions,
        input=timeframe,
        text_format=Dates
    )
    return response.output[0].content[0].parsed


@observe()
def get_location_id(location):
    instructions = f"""
    You are given a location name.

    Use the following dictionary to convert it to the corresponding city ID:

    {cities_dict}

    Return only the ID as a string, e.g. "314".
    If the location is not found, return the string "null".

    Note: the given location name may contain typos or be written in a different language than the dictionary.
    If needed, first translate or transliterate the location name into the language of the dictionary before matching.
    Do not return any explanation or extra text.
    """
    response = client.responses.parse(
        model="gpt-4o",
        instructions=instructions,
        input=location
    )
    return response.output[0].content[0].text


@app.post("/api/raw-info")
@observe()
def get_raw_info(raw_info_sub_task_mcp: dict = Body(...)):
    # print(f"\nEndpoint called with: {raw_info_sub_task_mcp}")
    events_url = "https://public-api.eventim.com/websearch/search/api/exploration/v2/productGroups"
    extracted_params = extract_search_params(raw_info_sub_task_mcp["content"]).output[0].content[0].parsed
    print(f'\n**** extracted: {extracted_params}')

    location = extracted_params.location
    location_id = get_location_id(location)
    dates = get_dates(extracted_params.timeframe, location)

    print(f'#### location id: {location_id}')
    print(f'#### dates: {dates}')

    params, headers = get_headers_and_params(location_id, dates)

    response = requests.get(events_url, params=params, headers=headers)
    return response.json()
