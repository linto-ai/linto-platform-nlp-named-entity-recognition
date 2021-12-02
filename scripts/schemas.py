from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class Article(BaseModel):
    # Schema for a single article in a batch of articles to process
    text: str


class RequestModel(BaseModel):
    # Schema for a request consisting a batch of articles, and component configuration
    articles: List[Article]
    component_cfg: Optional[Dict[str, Dict[str, Any]]] = None


class NerResponseModel(BaseModel):
    # Schema for the expected response and depends on what you
    # return from get_data.

    class Batch(BaseModel):
        class Entity(BaseModel):
            text: str
            label: str
            start: int
            end: int

        text: str
        ents: List[Entity] = []

    ner: List[Batch]
