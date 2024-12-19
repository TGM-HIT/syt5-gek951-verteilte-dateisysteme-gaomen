#!/bin/bash

# Path to the minio-secret.yaml file
SECRET_FILE="minio-secret.yaml"

# Check if the minio-secret.yaml file exists
if [ ! -f "$SECRET_FILE" ]; then
  echo "$SECRET_FILE does not exist. Exiting."
  exit 1
fi

kubectl apply -f minio-secret.yaml
kubectl apply -f minio-pvc.yaml
kubectl apply -f minio-deployment.yaml
kubectl apply -f flask-deployment.yaml
