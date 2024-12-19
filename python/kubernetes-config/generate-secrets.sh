#!/bin/bash

# Generate a random 12-byte access key and encode it with proper Base64 padding
access_key=$(head -c 12 /dev/urandom | base64 -w 0)

# Generate a random 24-byte secret key and encode it with proper Base64 padding
secret_key=$(head -c 24 /dev/urandom | base64 -w 0)

# Create the minio-secret.yaml file
cat <<EOF > minio-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: minio-secret
  namespace: default
type: Opaque
data:
  access_key: $access_key
  secret_key: $secret_key
EOF

echo "Generated minio-secret.yaml with access_key and secret_key."

