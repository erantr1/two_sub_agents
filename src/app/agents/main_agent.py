import requests
from openai import OpenAI
from fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import BaseModel
from pprint import pprint
import os
import asyncio, json, websockets

from src.app.agents import raw_info_sub_agent, process_info_sub_agent
from src.utils import get_headers_and_params, MCPTask
from src.utils import create_mcp_task

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mcp = FastMCP("Main Agent")


class SubTasks(BaseModel):
    raw_info_sub_task: str
    process_info_sub_task: str


@mcp.tool()
def create_sub_tasks(mcp_task: MCPTask):
    instructions = """
                Determine if the user input is a valid information request or query.
                If it is a valid request, divide it into 2 sub-tasks. 

                A valid request includes:
                - Questions seeking specific information or data
                - Requests for analysis, summarization, or processing of information
                - Queries that require searching, retrieving, or aggregating data

                Invalid inputs include:
                - Random text with no clear question or information need
                - Single words without context
                - Nonsensical statements
                - Empty strings
                - Instructions to perform physical actions that an AI system cannot do

                Sub-tasks division:
                - The 1st sub-task should focus on gathering raw information through external data sources using REST API calls. This includes identifying what data needs to be retrievedץ It should EXPLICITLY extract and include all key parameters needed for the API query, such as: locations, dates, event types, categories, or any other search criteria mentioned by the user. Be as specific as possible about these parameters as they will be used to construct API calls. This task will be handled by a dedicated agent that specializes in REST API interactions.
                - The 2nd sub-task should focus on filtering, processing, and analyzing the raw info collected in sub-task 1 to generate insights tailored to the user's needs. It should EXPLICITLY specify what aspects of the data to prioritize, how to rank or filter results, what preferences to consider, and what format the final recommendations should take. This task will be handled by an agent that specializes in data processing and real-time analysis via WebSocket connections.

                Note: both sub-tasks should be in the same language as the original task.
                """
    ## make sure that sub-tasks are in the same language as the original
    response = client.responses.parse(
        model="gpt-4o",
        input=mcp_task.content,
        instructions=instructions,
        text_format=SubTasks
    )
    response_model = response.output[0].content[0].parsed
    return response_model.raw_info_sub_task, response_model.process_info_sub_task



@mcp.tool()
def talk(raw_info: dict, process_info_sub_task_mcp: MCPTask) -> dict:
    async def _ws():
        async with websockets.connect("ws://127.0.0.1:8765") as ws:
            message = {
                "raw_info": raw_info,
                "task": process_info_sub_task_mcp.model_dump()
            }
            await ws.send(json.dumps(message))
            response = await ws.recv()
            return json.loads(response)
    return asyncio.run(_ws())


@mcp.tool()
def create_and_orchestrate_sub_tasks(mcp_task: MCPTask):
    raw_info_sub_task, process_info_sub_task = create_sub_tasks(mcp_task)

    raw_info_sub_task_mcp = create_mcp_task(message_type="raw info task", task=raw_info_sub_task,
                                            language=mcp_task.lang)
    process_info_sub_task_mcp = create_mcp_task(message_type="process info task", task=process_info_sub_task,
                                            language=mcp_task.lang)

    print(f'\ntask 1: {raw_info_sub_task}\ntask 2: {process_info_sub_task}\n')
    pprint(f'task 1 mcp: {raw_info_sub_task_mcp} task 2 mcp: {process_info_sub_task_mcp}')

    try:
        response = requests.post("http://localhost:8000/api/raw-info",
                                json=raw_info_sub_task_mcp.model_dump())
        response.raise_for_status()
        raw_info = response.json()
        print(json.dumps(raw_info, ensure_ascii=False, indent=2))
    except requests.exceptions.RequestException as e:
        raw_info = None
        print(f"Error calling raw-info endpoint: {e}")


    processed_info = talk(raw_info, process_info_sub_task_mcp)
    pprint(processed_info)
