import os
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

app = FastAPI()


def download_and_save(width: int, height: int, filename: str) -> str:
    """Download from place.dog and save to the project directory. Returns saved path."""
    url = f"https://place.dog/{width}/{height}"
    response = requests.get(url)

    # Local path on the host machine
    #save_dir = "/home/cblanchet/Documents/Camunda_Project/Place_dog_images"
    
    save_dir = "/app/Place_dog_images" # Path inside the Docker container
    

    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return save_path
    else:
        raise HTTPException(status_code=502, detail=f"Failed to download image: {response.status_code}")


@app.get("/download-dog")
def download_dog(
    width: Optional[int] = Query(300, ge=1, description="Image width"),
    height: Optional[int] = Query(200, ge=1, description="Image height"),
    filename: Optional[str] = Query("doggo.jpeg", description="Filename to save as"),
):
    """Endpoint to download a dog image and save it to the project folder.

    Example: /download-dog?width=400&height=300&filename=mydog.jpg
    """
    # Simple filename sanitization: prevent path traversal
    filename = os.path.basename(filename)

    try:
        saved = download_and_save(width, height, filename)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse({"saved_path": saved, "message": "Image saved 🐾"})


if __name__ == "__main__":
    # Allow running the script directly for quick tests
    path = download_and_save(300, 200, "doggo.jpeg")
    print(f"Image saved as {path} 🐾")