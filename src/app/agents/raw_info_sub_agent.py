from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, Body
import os
import requests

from src.utils import get_headers_and_params

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()


@app.post("/api/raw-info")
def get_raw_info(raw_info_sub_task_mcp: dict = Body(...)):
    print(f"Endpoint called with: {raw_info_sub_task_mcp}")

    events_url = "https://public-api.eventim.com/websearch/search/api/exploration/v2/productGroups"

    params, headers = get_headers_and_params(raw_info_sub_task_mcp["content"])
    print(f'params are: {params}')
    response = requests.get(events_url, params=params, headers=headers)
    print(f'response is: {response}')
    return response.json()
