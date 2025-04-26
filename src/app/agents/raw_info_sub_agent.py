from typing import Optional, List, Callable
import typing

from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, Body
import os
import requests

from src.utils import get_headers_and_params

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

class APIParams(BaseModel):
    location: str = Field(
        description="The city or area for the events",
        min_length=1,
        examples=["Tel Aviv", "Jerusalem"],
    )
    timeframe: Optional[str] = Field(
        default=None,
        description="When the events should take place",
        examples=["this weekend", "next Thursday", "tomorrow night"],
    )
    event_types: List[str] = Field(
        default_factory=list,
        description="Types of events mentioned",
        examples=[["concerts", "live music"], ["art exhibitions"], ["food festivals"]],
    )
    preferences: List[str] = Field(
        default_factory=list,
        description="Specific preferences or requirements",
        examples=[["family friendly", "outdoors"], ["low cost"], ["accessible venue"]],
    )

def extract_search_params(raw_info_sub_task):
    # Use LLM to extract structured parameters
    instructions = """
    Extract search parameters from the input.
    Return a JSON with these fields, when possible:
    - location: the city or area
    - timeframe: when the events should take place
    - event_types: types of events mentioned
    - preferences: specific preferences or requirements
    """
    response = client.responses.parse(
        model="gpt-4o",
        input=raw_info_sub_task,
        instructions=instructions,

    )

@app.post("/api/raw-info")
def get_raw_info(raw_info_sub_task_mcp: dict = Body(...)):
    print(f"Endpoint called with: {raw_info_sub_task_mcp}")

    events_url = "https://public-api.eventim.com/websearch/search/api/exploration/v2/productGroups"

    extracted_params = extract_search_params(raw_info_sub_task_mcp["content"])

    params, headers = get_headers_and_params(raw_info_sub_task_mcp["content"])
    print(f'params are: {params}')
    response = requests.get(events_url, params=params, headers=headers)
    print(f'response is: {response}')
    return response.json()
