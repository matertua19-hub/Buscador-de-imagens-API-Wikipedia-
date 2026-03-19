from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API Online", "instrucao": "Use /buscar?q=termo"}

@app.get("/buscar")
def buscar_imagem(q: str):
    # Endpoint da Wikimedia para buscar imagens baseadas em um termo
    url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&origin=*&generator=images&titles={q}&gimlimit=10&prop=imageinfo&iiprop=url"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Extraindo apenas as URLs das imagens
        pages = data.get("query", {}).get("pages", {})
        urls = [info["imageinfo"][0]["url"] for page in pages.values() if "imageinfo" in page for info in page["imageinfo"]]
        
        return {"termo_buscado": q, "total": len(urls), "urls": urls}
    except Exception as e:
        return {"erro": str(e)}
