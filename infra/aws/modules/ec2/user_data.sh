#!/bin/bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo usermod -aG docker ubuntu
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${image_uri%/*}
docker pull ${image_uri}
docker run --rm ${image_uri}
