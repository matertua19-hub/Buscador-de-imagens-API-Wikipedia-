from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from urllib.parse import quote

app = FastAPI()

# Permite que o seu HTML fale com a API sem bloqueios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/buscar/{q}")
def buscar(q: str):
    termo_seguro = quote(f"File:{q.strip()}")
    url_wikimedia = (
        f"https://commons.wikimedia.org/w/api.php?"
        f"action=query&format=json&origin=*&generator=search"
        f"&gsrsearch={termo_seguro}&gsrlimit=1&prop=imageinfo&iiprop=url"
    )
    try:
        response = requests.get(url_wikimedia, timeout=5)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "imageinfo" in page:
                return {"termo": q, "link": page["imageinfo"][0]["url"]}
        return {"termo": q, "link": "Não encontrado"}
    except:
        return {"termo": q, "link": "Erro na busca"}
