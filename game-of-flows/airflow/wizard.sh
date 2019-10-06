#! /bin/bash

function run() {
    docker-compose -f docker-compose.yaml up
}

$@