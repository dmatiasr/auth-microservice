#!/bin/bash
docker build . -t poc-authenticator
docker run -p 3210:8080 -d poc-authenticator
echo "Service running localhost:3210"
