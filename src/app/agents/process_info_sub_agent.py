import json
from http.client import responses

from langfuse.decorators import observe
from langfuse.decorators import langfuse_context
# from openai import OpenAI
from langfuse.openai import OpenAI
from langfuse.openai import openai
openai.langfuse_debug = True
from fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import asyncio, json, websockets

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mcp = FastMCP("Process Info Sub-Agent")


@mcp.tool()
@observe()
def process_raw_info(info, process_info_sub_task):
    instructions = f"""
    You are given an event data JSON (serialized as a string) and a task description.
    Parse the JSON and follow the task instructions.

    Task:
    {process_info_sub_task}

    Note: Some fields may be missing. Focus on event name, start date, rating, and location if available.
    """

    response = client.responses.parse(
        model="gpt-4o",
        input=json.dumps(info, ensure_ascii=False),
        instructions=instructions
    )
    response_model = response.output[0].content[0].text
    # response_model = response.output[0].content[0].parsed
    return response_model

@observe()
async def handle(ws):
    """
    One‑shot handler: wait for an optional trigger from the main agent,
    build the final summary, send it back.
    """
    try:
        ## Add validation for the incoming data
        message = await ws.recv()
        data = json.loads(message)

        raw = data.get("raw_info")
        process_info_sub_task_mcp = data.get("task")
        print(f'$$$ raw: {raw}; task: {process_info_sub_task_mcp} $$$')
        result = process_raw_info(raw, process_info_sub_task_mcp["content"])
        print(f'$$$ result: {result} $$$')

        await ws.send(json.dumps(result))
    finally:
        await langfuse_context.flush()

@observe()
async def main():
    # listens on ws://localhost:8765
    async with websockets.serve(handle, "0.0.0.0", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())