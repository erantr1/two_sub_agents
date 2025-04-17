from openai import OpenAI
from fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mcp = FastMCP("Main Agent")


class SubTasks(BaseModel):
    raw_info_sub_task: str
    process_info_sub_task: str


@mcp.tool()
def create_sub_tasks(json_task: dict):
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
        input=json_task["content"],
        instructions=instructions,
        text_format=SubTasks
    )
    response_model = response.output[0].content[0].parsed
    return response_model.raw_info_sub_task, response_model.process_info_sub_task


@mcp.tool()
def create_and_orchestrate_sub_tasks(json_task: str):
    raw_info_sub_task, process_info_sub_task = create_sub_tasks(json_task)
    print(f'task 1: {raw_info_sub_task}\ntask 2: {process_info_sub_task}')
