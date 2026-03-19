from fastapi import FastAPI, HTTPException
import requests
from urllib.parse import quote

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Online", "msg": "Use /buscar/termo"}

# MUDANÇA CHAVE: O termo 'q' agora faz parte da rota {q}
@app.get("/buscar/{q}")
def buscar_v5(q: str):
    if not q or len(q.strip()) == 0:
        raise HTTPException(status_code=400, detail="Termo de busca vazio")

    # Tratamento de segurança e prefixo para a Wikipedia
    termo_limpo = q.strip()
    termo_seguro = quote(f"File:{termo_limpo}")
    
    url_wikimedia = (
        f"https://commons.wikimedia.org/w/api.php?"
        f"action=query&format=json&origin=*&generator=search"
        f"&gsrsearch={termo_seguro}&gsrlimit=10"
        f"&prop=imageinfo&iiprop=url"
    )
    
    try:
        headers = {'User-Agent': 'BuscadorRobustoIA/1.5'}
        response = requests.get(url_wikimedia, headers=headers, timeout=10)
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        
        if not pages:
            return {"aviso": "Nenhuma imagem encontrada", "termo": termo_limpo, "resultados": []}

        resultado = []
        for page in pages.values():
            if "imageinfo" in page:
                resultado.append({
                    "titulo": page.get("title"),
                    "link": page["imageinfo"][0]["url"]
                })
        
        return {
            "termo_processado": termo_limpo,
            "total": len(resultado),
            "resultados": resultado
        }
        
    except Exception as e:
        return {"erro": "Falha na comunicação com Wikipedia", "detalhes": str(e)}
