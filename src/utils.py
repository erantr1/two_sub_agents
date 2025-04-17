import datetime
import uuid


def create_json_task(task:str, language: str):
    json_task = {
        "type": "text",
        "content": task,
        "lang": language,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "context_id": uuid.uuid4(),
        "metadata": None
    }
    return json_task