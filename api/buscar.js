export default async function handler(req, res) {
    // 1. CONFIGURAÇÃO DE SEGURANÇA (CORS)
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

    // Responde rapidamente a requisições de verificação (browser preflight)
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    const { tema, tipo } = req.query;

    try {
        // --- BUSCA NO UNSPLASH ---
        if (tipo === 'unsplash') {
            const response = await fetch(`https://api.unsplash.com/search/photos?query=${encodeURIComponent(tema)}&per_page=1`, {
                headers: { 'Authorization': `Client-ID ${process.env.UNSPLASH_KEY}` }
            });
            const data = await response.json();
            return res.json({ url: data.results?.[0]?.urls?.regular || null });
        }

        // --- BUSCA NO PIXABAY ---
        if (tipo === 'pixabay') {
            const response = await fetch(`https://pixabay.com/api/?key=${process.env.PIXABAY_KEY}&q=${encodeURIComponent(tema)}&image_type=photo`);
            const data = await response.json();
            return res.json({ url: data.hits?.[0]?.largeImageURL || null });
        }

        // --- BUSCA NO GIPHY ---
        if (tipo === 'giphy') {
            const response = await fetch(`https://api.giphy.com/v1/gifs/search?api_key=${process.env.GIPHY_KEY}&q=${encodeURIComponent(tema)}&limit=1&rating=g`);
            const data = await response.json();
            return res.json({ url: data.data?.[0]?.images?.original?.url || null });
        }

        res.status(400).json({ error: 'Tipo inválido' });
    } catch (error) {
        res.status(500).json({ error: 'Erro interno no servidor' });
    }
}
