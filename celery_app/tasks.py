import spacy
import components

from typing import Dict, List

from celery_app.celeryapp import celery

from ner import logger
from ner.processing import LM_MAP, MODELS
from ner.processing.utils import get_data


@celery.task(name="ner_task")
def ner_task(lang: str, texts: List[str], component_cfg: Dict = {}):
    """ ner_task """
    logger.info('NER task received')

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

    