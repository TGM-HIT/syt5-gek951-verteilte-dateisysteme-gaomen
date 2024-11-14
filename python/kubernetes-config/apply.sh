kubectl apply -f minio-secret.yaml
kubectl apply -f minio-pvc.yaml
kubectl apply -f minio-deployment.yaml
kubectl apply -f flask-deployment.yaml
