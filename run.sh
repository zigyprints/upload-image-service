#!/bin/bash


echo "Installing dependencies..."
pip install -r "requirements.txt"

echo "Setting environment variables..."
export CLOUDINARY_CLOUD_NAME="djpw5ipx1"
export CLOUDINARY_API_KEY="199759849613114"
export CLOUDINARY_API_SECRET="bppsR3BOJl0vmL3hd5YT0Frs9kk"

uvicorn your_web_app:app --reload --host 0.0.0.0 --port 8000

