# Entry point for the two_sub_agents project.
import datetime
import uuid
import pycld2 as cld2

from dotenv import load_dotenv
from fastmcp import FastMCP
from openai import OpenAI
from pydantic import BaseModel
from src.app.agents import main_agent
from src.utils import create_json_task
from typing import Optional
import os
import logging

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mcp = FastMCP("Task Orchestration")

@mcp.tool()
def detect_language_and_return_json(task: str) -> dict:
    is_reliable, _, details = cld2.detect(task) ## maybe get lang from user
    if is_reliable and details:
        language_code = details[0][1]
    else:
        language_code = "und"  # undetermined
    json_task = create_json_task(task=task, language=language_code)
    return json_task


def get_task_from_user() -> str:
    return input("What task would you like to perform?\n")


@mcp.tool()
def task_topic():
    task = get_task_from_user()
    json_task = detect_language_and_return_json(task)
    print(f'task:\n{json_task}')

    # Decomposing the main task into 2 sub-tasks
    # raw_info_sub_task, process_info_sub_task = main_agent.create_sub_tasks(json_task)
    # print(f'task 1: {raw_info_sub_task}\ntask 2: {process_info_sub_task}')

    main_agent.create_and_orchestrate_sub_tasks(json_task)


if __name__ == '__main__':
    mcp.run()
