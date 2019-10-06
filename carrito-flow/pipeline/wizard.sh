#! /bin/bash

export readonly PIPELINE='carrito-flow'
export readonly PROJECT=$(gcloud config get-value project 2> /dev/null)
export readonly BUCKET=${PROJECT}-${PIPELINE}

function activate_config(){
    if ! gcloud config configurations describe pycon 2> /dev/null; then
        gcloud config configurations create pycon
    fi
}

function activate_apis(){
    gcloud services enable dataflow.googleapis.com
}

function bucket(){
    BUCKET=$(gcloud config get-value project 2> /dev/null)-${PIPELINE}
    gsutil mb -c regional -l europe-west1 gs://${BUCKET}
}

function init() {
    activate_apis
    bucket
}

function venv(){
    virtualenv -p python2.7 venv
    source venv/bin/activate
    pip install -r requirements.txt
}

function init_pubsub() {
    $(gcloud beta emulators pubsub env-init)
}

function run(){
    source venv/bin/activate
    init_pubsub
    python pipeline.py --output carrito --streaming
}

function run_dataflow(){
    source venv/bin/activate
    python pipeline.py --runner DataflowRunner --job_name ${PIPELINE}-dataflow-job --project ${PROJECT} --staging_location "gs://${BUCKET}/staging" --temp_location "gs://${BUCKET}/temp" --output gs://${BUCKET}/carrito --streaming --experiments=allow_non_updatable_job parameter
}

function template(){
    source venv/bin/activate
    python pipeline.py --runner DataflowRunner --project ${PROJECT} --staging_location "gs://${BUCKET}/staging" --temp_location "gs://${BUCKET}/temp" --template_location "gs://${BUCKET}/templates/${PIPELINE}-template"
}

function run_job() {
    gcloud dataflow jobs run ${PIPELINE}-job --gcs-location=gs://${BUCKET}/templates/${PIPELINE}-template --region europe-west1 --parameters output=gs://${BUCKET}/carrito
}

$@
