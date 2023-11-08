#!/bin/bash

docker image build -t fast_api .
cd /docker
docker compose up -d
