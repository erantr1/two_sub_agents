

from openai import OpenAI


class RawInfoSubTask:
    # json
    pass


class ProcessInfoSubTask:
    # json
    pass


class SubTasks:
    raw_info_sub_task: RawInfoSubTask
    process_info_sub_task: ProcessInfoSubTask


def get_sub_tasks(json_task: dict, client: OpenAI):
    instructions = """

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
