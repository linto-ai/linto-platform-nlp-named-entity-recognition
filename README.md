# linto-platform-nlp-named-entity-recognition

## Description
This repository is for building a Docker image for LinTO's NLP service: Named Entity Recognition on the basis of [linto-platform-nlp-core](https://github.com/linto-ai/linto-platform-nlp-core), can be deployed along with [LinTO stack](https://github.com/linto-ai/linto-platform-stack) or in a standalone way (see Develop section in below).

linto-platform-nlp-named-entity-recognition is backed by [spaCy](https://spacy.io/) v3.0+ featuring transformer-based pipelines, thus deploying with GPU support is highly recommeded for inference efficiency.

LinTo's NLP services adopt the basic design concept of spaCy: [component and pipeline](https://spacy.io/usage/processing-pipelines), components are decoupled from the service and can be easily re-used in other projects, components are organised into pipelines for realising specific NLP tasks. 

This service uses [FastAPI](https://fastapi.tiangolo.com/) to serve spaCy's build-in components as pipelines:
- `ner`: Named Entity Recognition

## Usage

See documentation : [https://doc.linto.ai](https://doc.linto.ai)

## Deploy

With our proposed stack [https://github.com/linto-ai/linto-platform-stack](https://github.com/linto-ai/linto-platform-stack)

# Develop

## Build and run
1 Download models into `./assets` on the host machine (can be stored in other places).
```bash
cd linto-platform-nlp-named-entity-recognition/
bash scripts/download_models.sh
```

2 configure running environment variables
```bash
mv .envdefault .env
# cat .envdefault
# APP_LANG=fr en | Running language of application, "fr en", "fr", etc.
# ASSETS_PATH_ON_HOST=./assets | Storage path of models on host. (only applicable when docker-compose is used)
# ASSETS_PATH_IN_CONTAINER=/app/assets | Volume mount point of models in container. (only applicable when docker-compose is used)
# SERVICE_MODE=http
# CONCURRENCY=1 | Number of processing workers. (only applicable when docker-compose is used)
```

4 Build image
```bash
sudo docker build --tag lintoai/linto-platform-nlp-named-entity-recognition:latest .
```
or
```bash
sudo docker-compose build
```

5 Run container with GPU support, make sure that [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installing-on-ubuntu-and-debian) and GPU driver are installed.
```bash
sudo docker run --gpus all \
--rm -p 80:80 \
-v $PWD/assets:/app/assets:ro \
--env-file .env \
lintoai/linto-platform-nlp-named-entity-recognition:latest \
--workers 1
```
or
```bash
sudo docker-compose up
```
<details>
  <summary>Check running with CPU only setting</summary>
  
  - remove `--gpus all` from the first command.
  - remove `runtime: nvidia` from the `docker-compose.yml` file.
</details>


6 Navigate to `http://localhost/docs` in your browser, to explore the REST API interactively. See the examples for how to query the API.

## Specification for `http://localhost/ner/{lang}`

### Supported languages
| {lang} | Model | `ner` Labels | Size |
| --- | --- | --- | --- |
| `en` | [xx_ent_wiki_sm-3.2.0](https://github.com/explosion/spacy-models/releases/tag/xx_ent_wiki_sm-3.2.0) | `LOC`, `MISC`, `ORG`, `PER` | 11 MB |
| `fr` | [xx_ent_wiki_sm-3.2.0](https://github.com/explosion/spacy-models/releases/tag/xx_ent_wiki_sm-3.2.0) | `LOC`, `MISC`, `ORG`, `PER` | 11 MB |

### Request
```json
{
  "articles": [
    {
      "text": "Apple Inc. is an American multinational technology company that specializes in consumer electronics, computer software and online services."
    },
    {
      "text": "Apple was founded in 1976 by Steve Jobs, Steve Wozniak and Ronald Wayne to develop and sell Wozniak's Apple I personal computer."
    }
  ]
}
```

### Response
```json
{
  "ner": [
    {
      "text": "Apple Inc. is an American multinational technology company that specializes in consumer electronics, computer software and online services.",
      "ents": [
        {
          "text": "Apple Inc",
          "label": "ORG",
          "start": 0,
          "end": 9
        },
        {
          "text": "American",
          "label": "MISC",
          "start": 17,
          "end": 25
        }
      ]
    },
    {
      "text": "Apple was founded in 1976 by Steve Jobs, Steve Wozniak and Ronald Wayne to develop and sell Wozniak's Apple I personal computer.",
      "ents": [
        {
          "text": "Apple",
          "label": "ORG",
          "start": 0,
          "end": 5
        },
        {
          "text": "Steve Jobs",
          "label": "PER",
          "start": 29,
          "end": 39
        },
        {
          "text": "Steve Wozniak",
          "label": "PER",
          "start": 41,
          "end": 54
        },
        {
          "text": "Ronald Wayne",
          "label": "PER",
          "start": 59,
          "end": 71
        },
        {
          "text": "Wozniak",
          "label": "PER",
          "start": 92,
          "end": 99
        },
        {
          "text": "Apple I",
          "label": "MISC",
          "start": 102,
          "end": 109
        }
      ]
    }
  ]
}
```
