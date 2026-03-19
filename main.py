from fastapi import FastAPI
import requests
from urllib.parse import quote

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Busca Inteligente Ativa", "msg": "Use /buscar?q=termo"}

@app.get("/buscar")
def buscar_v2(q: str):
    termo_seguro = quote(q)
    
        # Adicionamos 'File:' ao termo para que a busca foque em arquivos de imagem
    termo_seguro = quote(f"File:{q}")
    
    url_wikimedia = (
        f"https://commons.wikimedia.org/w/api.php?"
        f"action=query&format=json&origin=*&generator=search"
        f"&gsrsearch={termo_seguro}&gsrlimit=10"
        f"&prop=imageinfo&iiprop=url|canonicalurl"
    )

    
    try:
        headers = {'User-Agent': 'BuscadorInteligente/1.1'}
        response = requests.get(url_wikimedia, headers=headers, timeout=10)
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        
        if not pages:
            return {"aviso": "Nada encontrado. Tente outro termo.", "termo": q}

        resultado = []
        for page in pages.values():
            # Filtramos para garantir que estamos pegando apenas arquivos de imagem
            if "imageinfo" in page:
                info = page["imageinfo"][0]
                resultado.append({
                    "titulo": page.get("title"),
                    "link_direto": info.get("url"),
                    "pagina_da_imagem": info.get("canonicalurl")
                })
        
        return {
            "termo_buscado": q,
            "total": len(resultado),
            "resultados": resultado
        }
        
    except Exception as e:
        return {"erro": "Erro na busca", "detalhes": str(e)}
