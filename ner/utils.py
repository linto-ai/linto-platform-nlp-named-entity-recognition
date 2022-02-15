from typing import Dict, Any

from spacy.tokens import Doc

__all__ = ["get_data"]

def get_data(doc: Doc) -> Dict[str, Any]:
    """Extract the data to return from the REST API given a Doc object. Modify
    this function to include other data."""
    def map_fun(ent) -> dict:
        return {"text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char}
    
    return {"text": doc.text, "ents": list(map(map_fun, doc.ents))}