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



def structure_api():
    params = {
        "webId": "web__eventim-co-il",
        "language": "iw",
        "retail_partner": "EIL",
        "city_ids": ["249", "null"],  # you can experiment with removing "null"
        "sort": "DateAsc",
        "reco_variant": "A"
    }

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "oidc-client-id": "web__eventim-co-il",
        "origin": "https://www.eventim.co.il",
        "priority": "u=1, i",
        "referer": "https://www.eventim.co.il/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    return params, headers
