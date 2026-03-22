// api/buscar.js
import axios from 'axios';

export default async function handler(req, res) {
    const { tema, tipo } = req.query;

    try {
        // 1. Lógica para o Unsplash
        if (tipo === 'unsplash') {
            const response = await axios.get(`https://api.unsplash.com/search/photos`, {
                params: { query: tema, per_page: 1 },
                headers: { Authorization: `Client-ID ${process.env.UNSPLASH_KEY}` }
            });
            return res.json({ url: response.data.results[0]?.urls.regular || null });
        }

        // 2. Lógica para o Pixabay
        if (tipo === 'pixabay') {
            const response = await axios.get(`https://pixabay.com/api/`, {
                params: { key: process.env.PIXABAY_KEY, q: tema, image_type: 'photo' }
            });
            return res.json({ url: response.data.hits[0]?.largeImageURL || null });
        }

        // 3. Lógica para o Giphy
        if (tipo === 'giphy') {
            const response = await axios.get(`https://api.giphy.com/v1/gifs/search`, {
                params: { api_key: process.env.GIPHY_KEY, q: tema, limit: 1, rating: 'g' }
            });
            return res.json({ url: response.data.data[0]?.images.original.url || null });
        }

        res.status(400).json({ error: 'Provedor inválido' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Erro ao processar busca' });
    }
                             }

