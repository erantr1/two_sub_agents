# # main.py
# # Entry point for the two_sub_agents project.
# import datetime
# import uuid
# import pycld2 as cld2
#
# from dotenv import load_dotenv
# from openai import OpenAI
# from pydantic import BaseModel
# from agents import main_agent, raw_info_sub_agent, process_info_sub_agent
# from typing import Optional
# import os
# import logging
#
# load_dotenv()
#
# class TaskValidity(BaseModel):
#     is_task: bool
#
# def get_task_from_user() -> str:
#     return input("What task would you like to perform?\n")
#
#
# def create_json_task(task:str, language: str):
#     json_task = {
#         "type": "text",
#         "content": task,
#         "lang": language,
#         "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
#         "context_id": uuid.uuid4(),
#         "metadata": None
#     }
#     return json_task
#
#
# def check_if_valid_and_return_json(task: str, client: OpenAI) -> tuple[bool, Optional[dict]]:
#     instructions = """
#             Determine if the user input is a valid information request or query that would require processing by an LLM system.
#
#             A valid request includes:
#             - Questions seeking specific information or data
#             - Requests for analysis, summarization, or processing of information
#             - Queries that require searching, retrieving, or aggregating data
#
#             Invalid inputs include:
#             - Random text with no clear question or information need
#             - Single words without context
#             - Nonsensical statements
#             - Empty strings
#             - Instructions to perform physical actions that an AI system cannot do
#
#             Respond with is_task = true if the input represents a valid information request, otherwise is_task = false.
#             Requests can be in any language, including Hebrew, English, etc.
#             """
#
#     response = client.responses.parse(
#         model = "gpt-4o",
#         input = task,
#         instructions = instructions,
#         text_format = TaskValidity
#     )
#     is_task = response.output[0].content[0].parsed.is_task ## check if .parsed should be replaced with .text
#
#     if is_task:
#         _, _, language = cld2.detect(task)[0][1]
#         json_task = create_json_task(task=task, language=language)
#         return True, json_task
#     else:
#         return False, None
#
#
# def main():
#     api_key = os.getenv("OPENAI_API_KEY")
#     client = OpenAI(api_key=api_key)
#
#     # Setting up a gate
#     task = get_task_from_user()
#     is_task, json_task = check_if_valid_and_return_json(task, client)
#     print("✔️ Valid task!" if is_task else "❌ Not a task. Try again.")
#     while not is_task:
#         task = get_task_from_user()
#         is_task, json_task = check_if_valid_and_return_json(task, client)
#         print("✔️ Valid task!" if is_task else "❌ Not a task. Try again.")
#
#     # Decomposing the main task into 2 sub-tasks
#     raw_info_sub_task, process_info_sub_task = main_agent.get_sub_tasks(json_task, client)
#
#
#
# if __name__ == '__main__':
#     main()
