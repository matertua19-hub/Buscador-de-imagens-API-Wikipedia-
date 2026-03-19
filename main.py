from fastapi import FastAPI
import requests
from urllib.parse import quote # Importação vital para evitar erros de URL

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API Online", "msg": "Use /buscar?q=termo"}

@app.get("/buscar")
def buscar_imagem(q: str):
    # O quote(q) transforma "História de Alagoas" em "Hist%C3%B3ria%20de%20Alagoas"
    termo_seguro = quote(q)
    
    url_wikimedia = (
        f"https://commons.wikimedia.org/w/api.php?"
        f"action=query&format=json&origin=*&generator=images&titles={termo_seguro}"
        f"&gimlimit=10&prop=imageinfo&iiprop=url|canonicalurl"
    )
    
    try:
        # User-Agent é importante para que a Wikipedia saiba quem está pedindo
        headers = {'User-Agent': 'BuscadorLLM/1.0 (contato@exemplo.com)'}
        response = requests.get(url_wikimedia, headers=headers, timeout=10)
        
        # Se a Wikipedia der erro, capturamos aqui antes de tentar ler o JSON
        if response.status_code != 200:
            return {"erro": f"Erro da Wikipedia: {response.status_code}"}
            
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        if not pages:
            return {"aviso": "Nenhuma imagem encontrada para este termo.", "termo": q}

        resultado = []
        for page in pages.values():
            if "imageinfo" in page:
                info = page["imageinfo"][0]
                resultado.append({
                    "titulo": page.get("title"),
                    "link_direto": info.get("url"),
                    "pagina_da_imagem": info.get("canonicalurl")
                })
        
        return {"termo": q, "total": len(resultado), "resultados": resultado}
        
    except Exception as e:
        return {"erro": "Falha técnica", "detalhes": str(e)}
