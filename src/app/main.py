# Entry point for the two_sub_agents project.
import datetime
import uuid
import pycld2 as cld2

from dotenv import load_dotenv
from fastmcp import FastMCP
from openai import OpenAI
from pydantic import BaseModel
from src.app.agents import main_agent
from src.utils import MCPTask, create_mcp_task
from typing import Optional
import os
import logging

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mcp = FastMCP("Task Orchestration")

@mcp.tool()
def detect_language_and_create_mcp_task(message_type:str, task: str) -> MCPTask:
    """Detect the task's language and create a standardized MCP message"""
    is_reliable, _, details = cld2.detect(task) ## maybe get lang from user
    if is_reliable and details:
        language_code = details[0][1]
    else:
        language_code = "und"  # undetermined
    mcp_task = create_mcp_task(message_type=message_type, task=task, language=language_code)
    return mcp_task


def get_task_from_user() -> str:
    return input("What task would you like to perform?\n")


@mcp.tool()
def task_topic():
    task = get_task_from_user()
    mcp_task = detect_language_and_create_mcp_task(message_type="task_assignment", task=task)
    print(f'mcp task:\n{mcp_task}')
    main_agent.create_and_orchestrate_sub_tasks(mcp_task)


if __name__ == '__main__':
    mcp.run()
