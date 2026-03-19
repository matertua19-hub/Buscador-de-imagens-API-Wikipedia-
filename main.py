import asyncio
import httpx # Recomendado para buscas assíncronas em lote
from fastapi import FastAPI
from urllib.parse import quote

app = FastAPI()

async def buscar_uma_imagem(client, termo):
    termo_seguro = quote(f"File:{termo.strip()}")
    url = (
        f"https://commons.wikimedia.org/w/api.php?"
        f"action=query&format=json&origin=*&generator=search"
        f"&gsrsearch={termo_seguro}&gsrlimit=1&prop=imageinfo&iiprop=url"
    )
    try:
        response = await client.get(url, timeout=5)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "imageinfo" in page:
                return {"termo": termo, "link": page["imageinfo"][0]["url"]}
    except:
        return {"termo": termo, "link": "Não encontrado"}
    return {"termo": termo, "link": "Não encontrado"}

@app.post("/batch")
async def buscar_lote(dados: dict):
    # 'texto' seria o que você colou do clipboard (ex: "Maceió, Farol, Alagoas")
    texto = dados.get("texto", "")
    termos = [t.strip() for t in texto.replace("\n", ",").split(",") if t.strip()]
    
    async with httpx.AsyncClient() as client:
        tarefas = [buscar_uma_imagem(client, termo) for termo in termos]
        resultados = await asyncio.gather(*tarefas)
    
    return {"resultados": resultados}
