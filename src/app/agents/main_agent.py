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
                - The 1st sub-task should focus on gathering raw information that is relevant for the user's needs.
                - The 2nd sub-task should focus on filtering, processing and analyzing the raw info collected in
                  sub-task 1 in order to adjust the output for the user's needs 
                
                Note: both sub-tasks should be in the same language of the original task.
                """
    # make sure that sub-tasks are in the same language as the original
    response = client.responses.parse(
        model="gpt-4o",
        input=mcp_task.content,
        instructions=instructions,
        text_format=SubTasks
    )
    response_model = response.output[0].content[0].parsed
    return response_model.raw_info_sub_task, response_model.process_info_sub_task


# @mcp.tool()
# def create_apis(raw_info_sub_task: str):
    # instructions = """
    #             You are given a user task. Suggest 1-3 public APIs that can help complete it.
    #             The output should be a list of URLs.
    #             """
    # response = client.responses.parse(
    #     model="gpt-4o",
    #     input=raw_info_sub_task,
    #     instructions=instructions,
    #     text_format=ApisList
    # )
    # response_model = response.output[0].content[0].parsed
    # return response_model.apis_list
# def create_apis():
#     events_url = "https://public-api.eventim.com/websearch/search/api/exploration/v2/productGroups"
#     params, headers = structure_api()
#     return events_url, params, headers


@mcp.tool()
def talk(raw_info: dict) -> dict:
    async def _ws():
        async with websockets.connect("ws://127.0.0.1:8765") as ws:
            await ws.send(json.dumps(raw_info))
            return json.loads(await ws.recv())
    return asyncio.run(_ws())


@mcp.tool()
def create_and_orchestrate_sub_tasks(mcp_task: MCPTask):
    raw_info_sub_task, process_info_sub_task = create_sub_tasks(mcp_task)

    raw_info_sub_task_mcp = create_mcp_task(message_type="raw info task", task=raw_info_sub_task,
                                            language=mcp_task.lang)
    process_info_sub_task_mcp = create_mcp_task(message_type="process info task", task=process_info_sub_task,
                                            language=mcp_task.lang)

    print(f'task 1: {raw_info_sub_task}\ntask 2: {process_info_sub_task}')
    pprint(f'task 1 mcp: {raw_info_sub_task_mcp}\ntask 2 mcp: {process_info_sub_task_mcp}')


    # apis_list = create_apis(raw_info_sub_task)
    # print(f'apis list: {apis_list}')

    # events_url, params, headers = create_apis()

    response = requests.post("http://localhost:8000/api/raw-info",
                            json=raw_info_sub_task_mcp.model_dump())
    raw_info = response.json()
    pprint(raw_info)

    # processed_info = talk(raw_info)
    # pprint(processed_info)



    # process_info_sub_agent.process_raw_info()
