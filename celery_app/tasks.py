import os
from typing import Dict, List

import spacy

from celery_app.celeryapp import celery
from ner import get_data

LM_MAP = {
    "fr": "spacy/xx_ent_wiki_sm-3.2.0/xx_ent_wiki_sm/xx_ent_wiki_sm-3.2.0",
    "en": "spacy/xx_ent_wiki_sm-3.2.0/xx_ent_wiki_sm/xx_ent_wiki_sm-3.2.0"}

# Load models
MODELS = {LM_MAP[lang]: spacy.load(os.environ.get("ASSETS_PATH_IN_CONTAINER") + '/' + LM_MAP[lang]) for lang in os.environ.get("APP_LANG").split(" ")}
print(f"Loaded {len(MODELS)} models: {MODELS.keys()}")

@celery.task(name="ner_task")
def ner_task(lang: str, texts: List[str], component_cfg: Dict = {}):
    """ ner_task """
    # Check language availability
    if lang in LM_MAP.keys():
        model_name = LM_MAP[lang]
        if model_name not in MODELS.keys():
            raise RuntimeError(f"Model {model_name} for language {lang} is not loaded.")
        nlp = MODELS[model_name]
    else:
        raise ValueError(f"Language {lang} is not supported.")

    response_body = []
    
    for doc in nlp.pipe(texts, component_cfg=component_cfg):
        response_body.append(get_data(doc))

    return {"ner": response_body}

    