import datetime
import uuid
from typing import Type, Optional, List, Callable

from pydantic import BaseModel, Field, field_validator


cities_dict = {
    "באר-שבע": "308",
    "בנימינה": "1957",
    "הרצליה": "314",
    "זכרון-יעקב": "1948",
    "חיפה": "307",
    "ירושלים": "306",
    "קיסריה": "1573",
    "ראשון-לציון": "1951",
    "תל-אביב": "249",
}


class MCPTask(BaseModel):
    type: str
    content: str
    lang: str
    timestamp: str
    context_id: str
    metadata: dict


class SearchParameters(BaseModel):
    location: str
    #     = Field(
    #     description="The city or area for the events",
    #     examples=["Tel Aviv", "Jerusalem"],
    # )
    timeframe: str
        # (Optional)[str] = Field(
        # default=None,
        # description="When the events should take place",
        # examples=["this weekend", "next Thursday", "tomorrow night"],
    # )
    # event_types: List[str] = Field(
    #     default_factory=list,
    #     description="Types of events mentioned",
    #     examples=[["concerts", "live music"], ["art exhibitions"], ["food festivals"]],
    # )
    # preferences: List[str] = Field(
    #     default_factory=list,
    #     description="Specific preferences or requirements",
    #     examples=[["family friendly", "outdoors"], ["low cost"], ["accessible venue"]],
    # )


def create_mcp_task(message_type:str, task:str, language: str) -> MCPTask:
    mcp_task = MCPTask(
        type=message_type,
        content=task,
        lang=language,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        context_id=str(uuid.uuid4()),
        metadata={}
    )
    return mcp_task



def get_headers_and_params(location_id, dates):
    params = {
        'webId': 'web__eventim-co-il',
        'language': 'iw',
        'retail_partner': 'EIL',
        'city_ids': [
            location_id,
            'null',
        ],
        'date_from': dates.start_date,
        'date_to': dates.end_date,
        'sort': 'DateAsc',
        'reco_variant': 'A',
    }
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
