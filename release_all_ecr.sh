#!/bin/bash
#
# Builds both `nginx` and `the_internet` images and publishes them to ECR. 
# Authenticates with Docker before attempting to push.


aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 383495223751.dkr.ecr.us-east-1.amazonaws.com
if [[ $? -eq 1 ]]
then
    exit
fi

./build_and_push.sh the_internet
./build_and_push.sh nginx
