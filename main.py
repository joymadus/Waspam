
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI()

# Serve your static frontend
app.mount("/", StaticFiles(directory="wabigimg", html=True), name="static")

# Upload directory for images
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Upload an image
@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

# List uploaded images
@app.get("/api/images")
def list_images():
    return {"images": os.listdir(UPLOAD_DIR)}

# Serve uploaded image
@app.get("/api/image/{filename}")
def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
