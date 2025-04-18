from openai import OpenAI
from fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mcp = FastMCP("Process Info Sub-Agent")

@mcp.tool()
def open_inter_agents_web_socket():
    pass


@mcp.tool()
def process_raw_info(info):
    pass