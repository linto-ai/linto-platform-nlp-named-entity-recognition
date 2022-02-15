FROM lintoai/linto-platform-nlp-core:latest
LABEL maintainer="gshang@linagora.com"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ner /usr/src/app/ner
COPY celery_app /usr/src/app/celery_app
COPY http_server /usr/src/app/http_server
COPY document /usr/src/app/document
COPY docker-entrypoint.sh wait-for-it.sh ./

ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app/ner"

#HEALTHCHECK --interval=15s CMD curl -fs http://0.0.0.0/health || exit 1

ENTRYPOINT ["./docker-entrypoint.sh"]