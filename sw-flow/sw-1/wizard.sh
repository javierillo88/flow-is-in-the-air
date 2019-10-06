#! /bin/bash

export readonly PIPELINE='sw-1'
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
}


function bucket(){
    BUCKET=$(gcloud config get-value project 2> /dev/null)-${PIPELINE}
    gsutil mb -c regional -l europe-west1 gs://${BUCKET}
}

function copy_files(){
    gsutil cp -r ../dataset gs://${BUCKET}/dataset
}

function init() {
    activate_config
    login
    activate_apis
    bucket
    copy_files
}

function venv(){
    virtualenv -p python2.7 venv
    source venv/bin/activate
    pip install -r requirements.txt
}

function run(){
    source venv/bin/activate
    python pipeline.py --input ../dataset/people.json --output names
}

function run_dataflow(){
    source venv/bin/activate
    python pipeline.py --runner DataflowRunner --job_name ${PIPELINE}-dataflow-job --project ${PROJECT} --staging_location "gs://${BUCKET}/staging" --temp_location "gs://${BUCKET}/temp" --input "gs://${BUCKET}/dataset/people.json" --output "gs://${BUCKET}/output/names"
}

function template(){
    source venv/bin/activate
    python pipeline.py --runner DataflowRunner --project ${PROJECT} --staging_location "gs://${BUCKET}/staging" --temp_location "gs://${BUCKET}/temp" --template_location "gs://${BUCKET}/templates/${PIPELINE}-template"
    gsutil cp ${PIPELINE}-template_metadata "gs://${BUCKET}/templates/"
}

function run_job() {
    gcloud dataflow jobs run ${PIPELINE}-job --gcs-location=gs://${BUCKET}/templates/${PIPELINE}-template --region europe-west1 --parameters input=gs://${BUCKET}/dataset/people.json,output=gs://${BUCKET}/output/names
}

$@
