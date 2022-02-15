#!/bin/bash
set -ea

echo "RUNNING NER"

# Launch parameters, environement variables and dependencies check
if [ -z "$SERVICE_MODE" ]
then
    echo "ERROR: Must specify a serving mode: [ http | task ]"
    exit -1
else
    if [ "$SERVICE_MODE" = "http" ] 
    then
        echo "RUNNING NER HTTP SERVER"
        ls
        /opt/conda/bin/python http_server/ingress.py --debug
    elif [ "$SERVICE_MODE" == "task" ]
    then
        if [[ -z "$SERVICES_BROKER" ]]
        then 
            echo "ERROR: SERVICES_BROKER variable not specified, cannot start celery worker."
            return -1
        fi
        /usr/src/app/wait-for-it.sh $(echo $SERVICES_BROKER | cut -d'/' -f 3) --timeout=20 --strict -- echo " $SERVICES_BROKER (Service Broker) is up"
        echo "RUNNING NER CELERY WORKER"
        celery --app=celery_app.celeryapp worker -Ofair -n nlp_${SERVICE_NAME}_worker@%h --queues=${SERVICE_NAME} -c ${CONCURRENCY}
    else
        echo "ERROR: Wrong serving command: $1"
        exit -1
    fi
fi

echo "Service stopped"