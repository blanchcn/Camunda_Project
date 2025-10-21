import os
from typing import Optional
import asyncio

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import httpx  # client HTTP asynchrone

app = FastAPI()


async def download_and_save(width: int, height: int, filename: str) -> str:
    """Asynchronously download from place.dog and save to the project directory. Returns saved path."""
    url = f"https://place.dog/{width}/{height}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

     # Local path on the host machine
    #save_dir = "/home/cblanchet/Documents/Camunda_Project/Place_dog_images"
    
    save_dir = "/app/Place_dog_images" # Path inside the Docker container
    save_path = os.path.join(save_dir, filename)

    if response.status_code == 200:
        # Use asyncio.to_thread to write file without blocking the event loop
        await asyncio.to_thread(_write_file_bytes, save_path, response.content)
        return save_path
    else:
        raise HTTPException(status_code=502, detail=f"Failed to download image: {response.status_code}")


def _write_file_bytes(path: str, data: bytes) -> None:
    """Blocking helper to write bytes to a file (run via asyncio.to_thread)."""
    with open(path, "wb") as f:
        f.write(data)


@app.get("/download-dog")
async def download_dog(
    width: Optional[int] = Query(300, ge=1, description="Image width"),
    height: Optional[int] = Query(200, ge=1, description="Image height"),
    filename: Optional[str] = Query("doggo.jpeg", description="Filename to save as"),
):
    """Async endpoint to download a dog image and save it to the project folder.

    Example: /download-dog?width=400&height=300&filename=mydog.jpg
    """
    # Simple filename sanitization: prevent path traversal
    filename = os.path.basename(filename)

    try:
        saved = await download_and_save(width, height, filename)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse({"saved_path": saved, "message": "Image saved 🐾"})


if __name__ == "__main__":
    # Allow running the script directly for quick tests
    import asyncio

    async def _test():
        path = await download_and_save(300, 200, "doggo.jpeg")
        print(f"Image saved as {path} 🐾")

    asyncio.run(_test())