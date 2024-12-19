# Route for uploading files
from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from minio import Minio
from dotenv import load_dotenv
import os
from io import BytesIO

# Load environment variables from .env file
load_dotenv()
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
MINIO_API_HOST = os.getenv('MINIO_API_HOST', "http://minio-service:9000")  # Use Kubernetes service name
PART_SIZE = 5 * 1024 * 1024

# Initialize the MinIO client
minio_client = Minio(
    MINIO_API_HOST.replace("http://", "").replace("https://", ""),
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)

# Initialize the Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')  # Secret key for flash messages

# Ensure bucket exists, create it if not
BUCKET_NAME = "test-bucket"
if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)

# Route for uploading files
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        
        if file:
            # Get the filename
            filename = file.filename
            
            # Upload the file to MinIO
            try:
                minio_client.put_object(BUCKET_NAME, filename, file.stream, -1, part_size=PART_SIZE)
                flash('File uploaded successfully!', 'success')
            except Exception as e:
                flash(f'Error uploading file: {str(e)}', 'danger')
            return redirect(url_for('upload_file'))
        
        flash('No file selected!', 'danger')
        return redirect(url_for('upload_file'))

    # List uploaded files
    try:
        files = minio_client.list_objects(BUCKET_NAME)
        file_list = [file.object_name for file in files]
    except Exception as e:
        flash(f'Error fetching files: {str(e)}', 'danger')
        file_list = []
    
    return render_template('upload.html', files=file_list)

# Route to view a file's content
@app.route('/files/view/<filename>')
def view_file(filename):
    try:
        # Get the file content
        response = minio_client.get_object(BUCKET_NAME, filename)
        file_content = response.read().decode('utf-8')  # Assuming it's a text-based file
        response.close()
        response.release_conn()
    except Exception as e:
        flash(f'Error reading file: {str(e)}', 'danger')
        file_content = None

    return render_template('view_file.html', filename=filename, content=file_content)

# Route to download a file
@app.route('/files/download/<filename>')
def download_file(filename):
    try:
        # Get the file from MinIO
        response = minio_client.get_object(BUCKET_NAME, filename)
        return send_file(BytesIO(response.read()), as_attachment=True, download_name=filename)
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('upload_file'))

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
