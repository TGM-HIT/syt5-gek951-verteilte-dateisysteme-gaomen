# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
from minio import Minio
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
MINIO_API_HOST = os.getenv('MINIO_API_HOST', "http://minio-service:9000")  # Use Kubernetes service name

# Initialize the MinIO client
minio_client = Minio(
    MINIO_API_HOST.replace("http://", "").replace("https://", ""),
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)

# Initialize the Flask app
app = Flask(__name__)

# Ensure bucket exists, create it if not
BUCKET_NAME = "test-bucket"
if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)

# Routes go here (same as before)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
