# Place Dog FastAPI

This small FastAPI app exposes an endpoint to download a placeholder dog image from `place.dog` and save it to a local folder.

## Requirements

Install dependencies (preferably in a virtualenv):

```bash
pip install -r requirements.txt
```

## Run the app

Start the server with uvicorn from the project root:

```bash
uvicorn "REST API:app" --host 0.0.0.0 --port 8000 --reload
```

Note: the file is named `REST API.py`. If your shell/uvicorn has trouble with the space in the filename, you can rename it or run:

```bash
python3 "REST API.py"
```

## Endpoint

GET /download-dog

Query parameters:
- width (int, default 300)
- height (int, default 200)
- filename (string, default doggo.jpeg)

Example:

```bash
curl "http://127.0.0.1:8000/download-dog?width=400&height=300&filename=mydog.jpg"
```

The image will be saved to `/home/cblanchet/Documents/Camunda_Project/Place_dog_images`.
