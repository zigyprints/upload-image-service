from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cloudinary.uploader
import cloudinary.api
import os

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

app = FastAPI()

# Define CORS Configuration
origins = [
    "http://localhost",  # Add the URLs of your frontend apps here
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5000",
    "http://localhost:8000",
    "http://3.110.190.23"
    "http://3.110.190.23:3000"
]

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET",
                   "POST",
                   "PUT",
                   "DELETE",
                   "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"]
)

print("Cloudinary configuration:"
      f"\n\tCloud name: {os.getenv('CLOUDINARY_CLOUD_NAME')}"
      f"\n\tAPI key: {os.getenv('CLOUDINARY_API_KEY')}"
      f"\n\tAPI secret: {os.getenv('CLOUDINARY_API_SECRET')}")

# Retrieve stickers from Cloudinary in a specific folder


@app.get("/get_sticker/{folder}/{sticker_id}")
def get_sticker(folder: str, sticker_id: str):
    try:
        sticker_url = cloudinary.api.resource(f"{folder}/{sticker_id}")["url"]
        return {"sticker_url": sticker_url}
    except cloudinary.exceptions.Error as e:
        raise HTTPException(status_code=404, detail="Sticker not found")

# Upload stickers to a specific folder in Cloudinary


@app.post("/upload_sticker/{folder}/")
async def upload_sticker(folder: str, file: UploadFile):
    try:
        # Upload the sticker to Cloudinary with the specified folder
        response = cloudinary.uploader.upload(file.file, folder=folder)

        # Extract the sticker's public ID from the response
        sticker_id = response["public_id"]

        return {"sticker_id": sticker_id}
    except cloudinary.exceptions.Error as e:
        raise HTTPException(status_code=500, detail="Sticker upload failed")

# Get a range of images from a specific folder in the Cloudinary bucket


@app.get("/get_images_range/{folder}/{start}/{end}")
def get_images_range(folder: str, start: int, end: int):
    try:
        # Fetch a list of images in the specified folder within the specified range
        images = cloudinary.api.resources(
            type="upload",
            prefix=folder,
            max_results=100,  # Adjust max_results as needed
        )
        return images["resources"][start:end]
    except cloudinary.exceptions.Error as e:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve images")


if __name__ == "__main__":
    import uvicorn

    # To start the FastAPI server, run the following command:
    # uvicorn your_script_name:app --reload
