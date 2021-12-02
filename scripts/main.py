import os
import spacy
import components
from scripts.schemas import *
from spacy.tokens import Doc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_health import health
from dotenv import load_dotenv

# To force the GPU usage: spacy.require_gpu()
spacy.prefer_gpu()

# Parse environment variables.
# variable and its value in the .envdefault file will be set, only if the variable is missing or empty in the current enviroment.
load_dotenv(".envdefault", override=False)

# Supported languages and corresponding model names
LM_MAP = {
    "fr": "spacy/xx_ent_wiki_sm-3.2.0/xx_ent_wiki_sm/xx_ent_wiki_sm-3.2.0",
    "en": "spacy/xx_ent_wiki_sm-3.2.0/xx_ent_wiki_sm/xx_ent_wiki_sm-3.2.0"
    }

# Load models
MODELS = {LM_MAP[lang]: spacy.load(os.environ.get("ASSETS_PATH_IN_CONTAINER") + '/' + LM_MAP[lang]) for lang in os.environ.get("APP_LANG").split(" ")}
print(f"Loaded {len(MODELS)} models: {MODELS.keys()}")

# Set up the FastAPI app and define the endpoints
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Health check
def healthy():
    return {"linto-platform-nlp-named-entity-recognition": "online"}
app.add_api_route("/health", health([healthy]))

# Named Entity Recognition
def get_data(doc: Doc) -> Dict[str, Any]:
    """Extract the data to return from the REST API given a Doc object. Modify
    this function to include other data."""
    ents = [
        {
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
        }
        for ent in doc.ents
    ]
    return {"text": doc.text, "ents": ents}

@app.post("/ner/{lang}", summary="Named Entity Recognition", response_model=NerResponseModel)
def ner(lang: str, query: RequestModel):
    """Process a batch of articles and return the entities predicted by the
    given model. Each record in the data should have a key "text".
    """
    if lang in LM_MAP.keys():
        model_name = LM_MAP[lang]
        if model_name not in MODELS.keys():
            raise RuntimeError(f"Model {model_name} for language {lang} is not loaded.")
        nlp = MODELS[model_name]
    else:
        raise ValueError(f"Language {lang} is not supported.")
    
    response_body = []
    texts = (article.text for article in query.articles)
    for doc in nlp.pipe(texts, component_cfg=query.component_cfg):
        response_body.append(get_data(doc))
    return {"ner": response_body}