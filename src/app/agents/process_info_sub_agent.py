import json

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
def process_raw_info(info):
    processed_info = "success"
    return processed_info


async def handle(ws):
    """
    One‑shot handler: wait for an optional trigger from the main agent,
    build the final summary, send it back, then close.
    """
    raw = await ws.recv()
    info = json.loads(raw)
    result = process_raw_info(info)
    await ws.send(json.dumps(result))


async def main():
    # listens on ws://localhost:8765
    async with websockets.serve(handle, "0.0.0.0", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())