import datetime
import uuid


def create_mcp_task(message_type:str, task:str, language: str) -> dict:
    mcp_task = {
        "type": message_type,
        "content": task,
        "lang": language,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "context_id": str(uuid.uuid4()),
        "metadata": {}
    }
    return mcp_task



def get_headers_and_params(raw_info_sub_task: str):
    ## Extract relevant params from raw_info_sub_task

    # params = {
    #     "webId": "web__eventim-co-il",
    #     "language": "iw",
    #     "retail_partner": "EIL",
    #     "city_ids": ["249", "null"],
    #     "date_from": "2025-05-02",
    #     "date_to": "2025-05-03",
    #     "sort": "DateAsc",
    #     "reco_variant": "A"
    # }

    params = {
        'webId': 'web__eventim-co-il',
        'language': 'iw',
        'retail_partner': 'EIL',
        'city_ids': [
            '249',
            'null',
        ],
        'date_from': '2025-05-02',
        'date_to': '2025-05-03',
        'sort': 'DateAsc',
        'reco_variant': 'A',
    }

    # headers = {
    #     "accept": "*/*",
    #     "accept-language": "en-US,en;q=0.9",
    #     "oidc-client-id": "web__eventim-co-il",
    #     "origin": "https://www.eventim.co.il",
    #     "priority": "u=1, i",
    #     "referer": "https://www.eventim.co.il/",
    #     "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": '"macOS"',
    #     "sec-fetch-dest": "empty",
    #     "sec-fetch-mode": "cors",
    #     "sec-fetch-site": "cross-site",
    #     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    #     "x-requested-with": "XMLHttpRequest"
    # }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'oidc-client-id': 'web__eventim-co-il',
        'origin': 'https://www.eventim.co.il',
        'priority': 'u=1, i',
        'referer': 'https://www.eventim.co.il/',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    return params, headers
