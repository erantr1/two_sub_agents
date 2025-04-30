import json
from http.client import responses

from langsmith.utils import with_cache
from openai import OpenAI
from fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import asyncio, json, websockets

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mcp = FastMCP("Process Info Sub-Agent")


@mcp.tool()
def process_raw_info(info, process_info_sub_task):
    # instructions = """
    # You are given a JSON with events details.
    # Extract only live shows
    # """
    # response = client.responses.parse(
    #     model="gpt-4o",
    #     input=info,
    #     instructions=instructions
    # )
    # response_model = response.output[0].content[0].text
    # return response_model
    return "success"


async def handle(ws):
    """
    One‑shot handler: wait for an optional trigger from the main agent,
    build the final summary, send it back, then close.
    """
    message = await ws.recv()
    data = json.loads(message)

    raw = data.get("raw_info")
    process_info_sub_task_mcp = data.get("task")

    print(f'$$$ raw: {raw}; task: {process_info_sub_task_mcp} $$$')

    result = process_raw_info(raw, process_info_sub_task_mcp["content"])

    print(f'$$$ result: {result} $$$')

    await ws.send(json.dumps(result))


async def main():
    # listens on ws://localhost:8765
    async with websockets.serve(handle, "0.0.0.0", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())