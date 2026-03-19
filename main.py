from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from urllib.parse import quote

app = FastAPI()

# ISSO É O QUE LIBERA O ACESSO PARA O SEU SITE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite acesso de qualquer lugar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "online", "message": "API de Imagens Pronta"}

@app.get("/buscar/{q}")
def buscar(q: str):
    termo_seguro = quote(f"File:{q.strip()}")
    url_wikimedia = (
        f"https://commons.wikimedia.org/w/api.php?"
        f"action=query&format=json&origin=*&generator=search"
        f"&gsrsearch={termo_seguro}&gsrlimit=1&prop=imageinfo&iiprop=url"
    )
    
    try:
        headers = {'User-Agent': 'MeuBuscadorIA/1.0'}
        response = requests.get(url_wikimedia, headers=headers, timeout=5)
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        
        for page in pages.values():
            if "imageinfo" in page:
                return {"termo": q, "link": page["imageinfo"][0]["url"]}
        
        return {"termo": q, "link": "Não encontrado"}
    except Exception as e:
        return {"termo": q, "link": f"Erro: {str(e)}"}
