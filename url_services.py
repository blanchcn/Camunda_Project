import httpx

async def fetch_animal_picture_urls(animal_type: str, count) -> list[str]:
    api_urls = {
        'dog': 'https://place.dog/200/300',
        'bear': 'https://placebear.com/200/300'
    }

    url = api_urls.get(animal_type.lower())
    if not url:
        raise ValueError(f"Unsupported animal type: {animal_type}")

    async with httpx.AsyncClient() as client:
        # For demonstration, it returns the same URL multiple times
        print(f"DEBUG: Valeur de ma variable URL :{[url] * count}")
        return [url] * count