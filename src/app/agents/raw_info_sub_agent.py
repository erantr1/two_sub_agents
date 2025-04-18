from openai import OpenAI
from fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mcp = FastMCP("Raw Info Sub-Agent")


@mcp.tool()
def get_raw_info(raw_info_sub_task: str):
    instructions = """
    You received a task to gather some information from the web.
    In order to get the information you need to use APIs of relevant sources.
    
    """
    response = client.responses.parse(
        model="gpt-4o",
        input=raw_info_sub_task,
        instructions=instructions
    )
    response_model = response.output[0].content[0].text
    ## if using BaseModel - response_model = response.output[0].content[0].parsed

    raw_info = []
    ## raw_info.append() API calls with REST

    return response_model