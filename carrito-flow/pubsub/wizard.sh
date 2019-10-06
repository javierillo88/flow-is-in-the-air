#! /bin/bash

export readonly PROJECT=$(gcloud config get-value project 2> /dev/null)

function create_topic() {
    gcloud pubsub topics create carrito
}

function init() {
    create_topic
}

function venv(){
    virtualenv -p python3.7 venv
    source venv/bin/activate
    pip install -r requirements.txt
}

function start_pubsub() {
    gcloud beta emulators pubsub start --project=${PROJECT}
}

function init_pubsub() {
    $(gcloud beta emulators pubsub env-init)
}


function create_topic_local(){
    source venv/bin/activate

    init_pubsub
    python publisher.py ${PROJECT} create carrito
}

$@
