#!/bin/bash

# Generate a random 12-character alphanumeric access key
access_key=$(tr -dc 'A-Za-z0-9' </dev/urandom | head -c 12)

# Generate a random 24-character alphanumeric secret key
secret_key=$(tr -dc 'A-Za-z0-9' </dev/urandom | head -c 24)

# Create the minio-secret.yaml file
cat <<EOF > minio-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: minio-secret
  namespace: default
type: Opaque
stringData:
  access_key: $access_key
  secret_key: $secret_key
EOF

echo "Generated minio-secret.yaml with access_key and secret_key."

