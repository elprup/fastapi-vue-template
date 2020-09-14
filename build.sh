#!/bin/bash
function fvtlog() {
    echo 【 FastAPIVueTemplate Build 】====\> $@
}

build_dir=$(pwd)
client_dir=$(pwd)/frontend
server_dir=$(pwd)/backend

ENV=$1
ENV="${ENV:-production}"

function buildClient() {
    fvtlog "start building client for FastAPIVueTemplate..."
    cd $client_dir
    yarn install && yarn run lint --no-fix && yarn run build --mode $ENV
}

function buildServer() {
    fvtlog "start build server for FastAPIVueTemplate"
    rm -rf $server_dir/public
    cd $build_dir
    mv $client_dir/dist $server_dir/public
}

buildClient
buildServer