from enum import unique
import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import httpx  # client HTTP asynchrone
import asyncio

import uuid

from url_services  import fetch_animal_picture_urls


app = FastAPI()

# REST API called Functions -----------------------------------

async def download_and_save(animal_type: str, width: int, height: int, filename: str, count: int) -> list[str]:
    """
    Asynchronously download from animal providers and save to disk.
    fetch_animal_picture_urls returns a list[str] — we take the first url item when count==1 or more if count>1.

    """

    # This local REST API on my PC. Locally launched, Docker container launched or Docker Compose launched
    #url = f"https://127.0.0.1/api/{animal_type}/{width}/{height}/{count}"

    # This NGrok internet gateway URL maps to the local FastAPI server (Please ensure my PC is running and ngrok tunnel is active on my side)
    #url = f"https://vagal-histomorphologically-lucila.ngrok-free.de/{animal_type}/api/{width}/{height}/{count}"
    save_multiple_paths: list[str] = []

    # get list of URLs
    url_list = await fetch_animal_picture_urls(animal_type, count)
    if not url_list:
        raise HTTPException(status_code=500, detail="No URL returned by provider")

    for url in url_list:
        # take next url (string)
        #url = url_list[next_url]
        # debug print: should show a proper url string starting with http/https
        print("DEBUG: downloading from URL ->", url)

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url)
            except httpx.RequestError as e:
                raise HTTPException(status_code=502, detail=f"Error fetching URL {url}: {str(e)}")
        

        # Local path on the host machine
        #save_dir = "/home/cblanchet/Documents/Camunda_Project/Place_images/"
    
        # Path inside the Docker container
        save_dir = "/app/Place_images/"

           # Determine default filename if not provided
        if filename is None:
            unique_sequence = str(uuid.uuid4().hex[:8])
            filename = f"{animal_type}_{unique_sequence }.jpeg"
            save_path = os.path.join(save_dir, filename)
            print("DEBUG: variable sale_path (QUERY MODE) ->", save_path)
        
        else:
            # Simple filename sanitization: prevent path traversal
            filename = os.path.basename(filename)
            save_path = os.path.join(save_dir, filename)

        if response.status_code == 200:
            # Use asyncio.to_thread to write file without blocking the event loop
            await asyncio.to_thread(_write_file_bytes, save_path, response.content)
            filename = None
            save_multiple_paths.append(save_path)
            print("DEBUG: Files saved ->", save_path + "\n" + "\n".join(save_multiple_paths))
        else:
            raise HTTPException(status_code=502, detail=f"Failed to download image: {response.status_code}")
        
    return save_multiple_paths
            


def _write_file_bytes(path: str, data: bytes) -> None:
    """Blocking helper to write bytes to a file (run via asyncio.to_thread)."""
    with open(path, "wb") as f:
        f.write(data)

# Routes ----------------------------------------


@app.get("/api/{animal_type}/{width}/{height}/{count}")
async def download_image(
    animal_type: str,
    width: int = 300, # Image width
    height: int = 200, #Image height
    count: int = 1, # Number of images to download
    filename: Optional[str] = Query(None, description="Filename to save as"), #choose image filename (include .JPG extension)
    
):
    
    """Async endpoint to download an image from animal providers and save it to the local folder /app/Place_images/

    Examples:\n
        - /api/{animal_type}/{width}/{height}/{count}?filename=teddybear.jpeg
        - 1 Bear image example: /api/bear/300/200/1?filename=teddybear.jpeg (if no filename is provided in Query URL, defaults to bear_{sequence}.jpeg)
        - 3 Dog images example: /api/dog/300/200/3?filename=Idefix_dog.jpeg (if no filename is provided in Query URL, defaults to dog_{sequence}.jpeg)
    """
 
    try:
        saved = await download_and_save(animal_type, width, height, filename, count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return JSONResponse({"saved_path": saved, "message": "Image saved 🐾"})


# Allow running the script directly for quick tests

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)