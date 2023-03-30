import os
import sys
import spacy
from time import time

from ner import logger
from ner.processing.utils import get_data

__all__ = ["logger", "get_data", "LM_MAP", "MODELS"]

logger.info("Loading language model(s)...")
start = time()

# Supported languages and corresponding model names
LM_MAP = {
    "fr": "spacy/xx_ent_wiki_sm-3.2.0/xx_ent_wiki_sm/xx_ent_wiki_sm-3.2.0",
    "en": "spacy/xx_ent_wiki_sm-3.2.0/xx_ent_wiki_sm/xx_ent_wiki_sm-3.2.0"
    }

try:
    MODELS = {LM_MAP[lang]: spacy.load(os.environ.get("ASSETS_PATH_IN_CONTAINER") + '/' + LM_MAP[lang]) for lang in os.environ.get("APP_LANG").split(" ")}
except Exception as err:
    raise Exception("Failed to load model(s): {}".format(str(err))) from err
    sys.exit(-1)

logger.info(f"(t={time() - start}s). Loaded {len(MODELS)} models: {MODELS.keys()}.")