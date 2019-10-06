#! /bin/bash

export readonly PIPELINE='sw-2'
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

function bucket(){
    BUCKET=$(gcloud config get-value project 2> /dev/null)-${PIPELINE}
    gsutil mb -c regional -l europe-west1 gs://${BUCKET}
}

function copy_files(){
    gsutil cp -r ../dataset gs://${BUCKET}/dataset
}

function activate_apis(){
    gcloud services enable dataflow.googleapis.com
    gcloud services enable datastore.googleapis.com
}

function create_datastore(){
    gcloud app create --region=europe-west
}

function init() {
    activate_config
    login
    bucket
    copy_files
    activate_apis
    create_datastore
}

function venv(){
    virtualenv -p python2.7 venv
    source venv/bin/activate
    pip install -r requirements.txt
}

function start_datastore() {
    gcloud beta emulators datastore start &
}

function init_datastore() {
    $(gcloud beta emulators datastore env-init)
}

function _datastore_database_wait_until_ready() {
    while ! curl ${DATASTORE_HOST} &> /dev/null ; do
        echo 'Waiting for database connection...'
        sleep 2
    done
}

function _shutdown_datastore_database() {
    init_datastore
    curl -X POST ${DATASTORE_HOST}/shutdown
}

function view() {
    init_datastore
    dsui
}

function run(){
    source venv/bin/activate
    start_datastore
    init_datastore
    _datastore_database_wait_until_ready
    python pipeline.py --kind starships --dataset ${PROJECT}
}

function run_dataflow(){
    source venv/bin/activate
    python pipeline.py --runner DataflowRunner --job_name ${PIPELINE}-dataflow-job --project ${PROJECT} --staging_location "gs://${BUCKET}/staging" --temp_location "gs://${BUCKET}/temp" --dataset ${PROJECT} --kind starships --namespace sw
}

function template(){
    source venv/bin/activate
    python pipeline.py --runner DataflowRunner --project ${PROJECT} --staging_location "gs://${BUCKET}/staging" --temp_location "gs://${BUCKET}/temp" --template_location "gs://${BUCKET}/templates/${PIPELINE}-template" --setup_file ./setup.py
    gsutil cp ${PIPELINE}-template_metadata "gs://${BUCKET}/templates/"
}

function run_job() {
    gcloud dataflow jobs run ${PIPELINE}-job --gcs-location=gs://${BUCKET}/templates/${PIPELINE}-template --region europe-west1 --parameters dataset=${PROJECT},kind=starships,namespace=sw
}

$@
