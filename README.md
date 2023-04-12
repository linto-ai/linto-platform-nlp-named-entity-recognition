# linto-platform-nlp-named-entity-recognition

## Description
This repository is for building a Docker image for LinTO's NLP service: Named Entity Recognition on the basis of [linto-platform-nlp-core](https://github.com/linto-ai/linto-platform-nlp-core), can be deployed along with [LinTO stack](https://github.com/linto-ai/linto-platform-stack) or in a standalone way (see Develop section in below).

LinTo's NLP services adopt the basic design concept of spaCy: [component and pipeline](https://spacy.io/usage/processing-pipelines), components (located under the folder `components/`) are decoupled from the service and can be easily re-used in other spaCy projects, components are organised into pipelines for realising specific NLP tasks. 

This service can be launched in two ways: REST API and Celery task, with and without GPU support.

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
cp .envdefault .env
```

| Environment Variable | Description | Default Value |
| --- | --- | --- |
| `APP_LANG` | A space-separated list of supported languages for the application | fr en |
| `ASSETS_PATH_ON_HOST` | The path to the assets folder on the host machine | ./assets |
| `ASSETS_PATH_IN_CONTAINER` | The volume mount point of models in container | /app/assets |
| `LM_MAP` | A JSON string that maps each supported language to its corresponding language model | {"fr":"spacy/xx_ent_wiki_sm-3.2.0/xx_ent_wiki_sm/xx_ent_wiki_sm-3.2.0","en":"spacy/xx_ent_wiki_sm-3.2.0/xx_ent_wiki_sm/xx_ent_wiki_sm-3.2.0"} |
| `SERVICE_MODE` | The mode in which the service is served, either "http" (REST API) or "task" (Celery task) | "http" |
| `CONCURRENCY` | The maximum number of requests that can be handled concurrently | 1 |
| `USE_GPU` | A flag indicating whether to use GPU for computation or not, either "True" or "False" | True |
| `SERVICE_NAME` | The name of the micro-service | ner |
| `SERVICES_BROKER` | The URL of the broker server used for communication between micro-services | "redis://localhost:6379" |
| `BROKER_PASS` | The password for accessing the broker server | None |

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
lintoai/linto-platform-nlp-named-entity-recognition:latest
```
<details>
  <summary>Check running with CPU only setting</summary>
  
  - remove `--gpus all` from the first command.
  - set `USE_GPU=False` in the `.env`.
</details>

or

```bash
sudo docker-compose up
```
<details>
  <summary>Check running with CPU only setting</summary>
  
  - remove `runtime: nvidia` from the `docker-compose.yml` file.
  - set `USE_GPU=False` in the `.env`.
</details>


6 If running under `SERVICE_MODE=http`, navigate to `http://localhost/docs` in your browser, to explore the REST API interactively. See the examples for how to query the API. If running under `SERVICE_MODE=task`, plese refers to the individual section in the end of this README.

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

## Testing Celery mode locally
1 Install Redis on your local machine, and run it with:
```bash
redis-server --protected-mode no --bind 0.0.0.0 --loglevel debug
```

2 Make sure in your `.env`, these two variables are set correctly as `SERVICE_MODE=task` and `SERVICES_BROKER=redis://172.17.0.1:6379`

Then start your docker container with either `docker run` or `docker-compose up` as shown in the previous section.

3 On your local computer, run this python script: 
```python
from celery import Celery
celery = Celery(broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
r = celery.send_task(
    'ner_task', 
    (
        'en', 
        [
            "Apple Inc. is an American multinational technology company that specializes in consumer electronics, computer software and online services.",
            "Apple was founded in 1976 by Steve Jobs, Steve Wozniak and Ronald Wayne to develop and sell Wozniak's Apple I personal computer."
        ],
        {"ner": {"top_n": 3}}
    ),
    queue='ner')
r.get()
```

