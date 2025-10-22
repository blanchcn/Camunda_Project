# PlaceAnimals REST API based FastAPI

This small FastAPI app exposes an endpoint to download a placeholder danimal images from animal providers and save it to a local disk.

## Requirements

Install dependencies (preferably in a virtualenv):

```bash
pip install -r requirements.txt
```

## Run the app

Start the server with uvicorn from the project root:

```bash
uvicorn "main:app" --host 0.0.0.0 --port 8000 --reload
```

Note: the file is named `main.py`.

```bash
python3 "main.py"
```

## Endpoint

Query parameters:
- width (int, default 300)
- height (int, default 200)
- count (int, number of images to download)
- filename (string, user chosen name)

Examples:

```bash
curl "http://127.0.0.1:8000/api/animal_type}/{width}/{height}/{count}?filename=file_name.jpeg"

curl "http://127.0.0.1:8000/api/dog/300/200/2?filename=Idefix_dog.jpeg"
curl "http://127.0.0.1:8000/api/dog/300/200/3"
```

The image will be saved to, for local project `/home/cblanchet/Documents/Camunda_Project/Place_images`.
The image will be saved to, for Docker Compose container `/app/Place_images`.

sync endpoint to download one or more images from animal providers and save it/them to the local disk at /app/Place_images/

    Examples:

        - /api/{animal_type}/{width}/{height}/{count}?filename=file_name.jpeg
        - 1 Bear image example: /api/bear/300/200/1?filename=teddybear.jpeg (if no filename is provided in Query URL, defaults to bear_{sequence}.jpeg)
        - 3 Dog images example: /api/dog/300/200/3?filename=Idefix_dog.jpeg (if no filename is provided in Query URL, defaults to dog_{sequence}.jpeg)
    

## This local REST API on my PC. Locally launched, Docker container launched or Docker Compose launched

    https://127.0.0.1/api/{animal_type}/{width}/{height}/{count}/

## This NGrok internet gateway URL maps to the local FastAPI server

(Please ensure my PC is running and ngrok tunnel is active on my side)

    https://vagal-histomorphologically-lucila.ngrok-free.de/{animal_type}/api/{width}/{height}/{count}

## See Swagger docs for more details at:

    http://127.0.0.1:8000/docs#/

    https://vagal-histomorphologically-lucila.ngrok-free.dev/docs#/


## Project current state

Current REST API endpoint allow you to retrieve images from:
    - Different animal provider web sites
    - Animal types
    - With image width selection
    - With image lenght selection
    - With number of image to download in once.

The project is Docker containered ready and also Docker Compose ready with a volume mapping to local PC to see downloaded image and keep persitance as container are stateless.

## Next dev steps:

- Store images and metadata into a database like alchemy
- Build the second endpoint to retrieve the last image downloaded from each animal provider websites
- Build a quick GUI with Streamlit

