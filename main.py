from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "API Online", 
        "manual": "Adicione /buscar?q=termo na URL para pesquisar imagens."
    }

@app.get("/buscar")
def buscar_imagem(q: str):
    # Endpoint otimizado para evitar links quebrados (canonicalurl)
    # iiprop=url|canonicalurl garante que tenhamos o link da página e o link direto
    url_wikimedia = (
        f"https://commons.wikimedia.org/w/api.php?"
        f"action=query&format=json&origin=*&generator=images&titles={q}"
        f"&gimlimit=10&prop=imageinfo&iiprop=url|canonicalurl"
    )
    
    try:
        response = requests.get(url_wikimedia, timeout=10)
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        
        resultado = []
        for page in pages.values():
            if "imageinfo" in page:
                info = page["imageinfo"][0]
                # Priorizamos o canonicalurl pois ele abre a página de visualização segura
                resultado.append({
                    "titulo": page.get("title", "Sem título"),
                    "link_direto": info.get("url"),
                    "pagina_da_imagem": info.get("canonicalurl")
                })
        
        return {
            "termo": q,
            "total_encontrado": len(resultado),
            "resultados": resultado
        }
        
    except Exception as e:
        return {"erro": "Falha ao conectar com a Wikimedia", "detalhes": str(e)}
