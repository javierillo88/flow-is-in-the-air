#! /bin/bash


function venv(){
    virtualenv -p python2.7 venv
    source venv/bin/activate
    pip install -r requirements.txt
}

function run(){
    source venv/bin/activate
    python utils.py
}

$@
