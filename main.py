from fastapi import FastAPI
import requests
from urllib.parse import quote

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Busca Inteligente Ativa", "msg": "Use /buscar?q=termo"}
@app.get("/buscar")
def buscar_v3(q: str):
    termo_seguro = quote(f"File:{q}")
    
    # Mudamos para 'generator=search' com 'prop=imageinfo' 
    # e pedimos especificamente a 'url' já validada pela Wikipedia
    url_wikimedia = (
        f"https://commons.wikimedia.org/w/api.php?"
        f"action=query&format=json&origin=*&generator=search"
        f"&gsrsearch={termo_seguro}&gsrlimit=10"
        f"&prop=imageinfo&iiprop=url" # Aqui a Wikipedia gera o link real e testado
    )
    
    try:
        headers = {'User-Agent': 'BuscadorPesquisador/1.2'}
        response = requests.get(url_wikimedia, headers=headers, timeout=10)
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        
        resultado = []
        for page in pages.values():
            if "imageinfo" in page:
                # O segredo: a Wikipedia já nos dá a URL pública funcional aqui
                url_real = page["imageinfo"][0]["url"]
                resultado.append({
                    "titulo": page.get("title"),
                    "link": url_real
                })
        
        return {"resultados": resultado}
        
    except Exception as e:
        return {"erro": str(e)}
