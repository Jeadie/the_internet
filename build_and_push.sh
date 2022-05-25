#!/bin/bash
#
# Builds and uploads a single docker image to ECR. ECR repository and AWS account
# pre-set. Docker must be authenticated with credentials from the AWS ECR
# repository.

if [ $# -ne 1 ]
then
     echo "Need image name. ./build_and_push.sh IMAGE"
     echo " IMAGE is one of: nginx, the_internet"
     return 
fi

IMAGE=$1


cd $IMAGE
docker build -t 383495223751.dkr.ecr.us-east-1.amazonaws.com/$IMAGE:latest .
docker push 383495223751.dkr.ecr.us-east-1.amazonaws.com/$IMAGE:latest
cd -
