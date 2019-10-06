#! /bin/bash

export readonly PIPELINE='carrito-flow'
export readonly PROJECT=$(gcloud config get-value project 2> /dev/null)
export readonly BUCKET=${PROJECT}-${PIPELINE}

function activate_config(){
    if ! gcloud config configurations describe pycon 2> /dev/null; then
        gcloud config configurations create pycon
    fi
}

function login(){
    gcloud init --skip-diagnostics
    gcloud auth application-default login
}

function activate_apis(){
    gcloud services enable dataflow.googleapis.com
    gcloud services enable datastore.googleapis.com
    gcloud services enable pubsub.googleapis.com
}

function bucket(){
    BUCKET=$(gcloud config get-value project 2> /dev/null)-${PIPELINE}
    gsutil mb -c regional -l europe-west1 gs://${BUCKET}
}

function create_app(){
    gcloud app create --region=europe-west
}

function init() {
    activate_config
    login
    activate_apis
    bucket
    create_app
}

function init_pubsub() {
    $(gcloud beta emulators pubsub env-init)
}

function venv(){
    virtualenv -p python3.7 venv
    source venv/bin/activate
    pip install -r requirements-local.txt
}

function run(){
    source venv/bin/activate
    init_pubsub
    export GOOGLE_CLOUD_PROJECT=${PROJECT}
    python main.py
}

function deploy(){
    gcloud app deploy -q .
}

$@
