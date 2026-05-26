const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = 5000;
const SECRET_KEY = "corposucre_secret_key_2026";

app.use(cors());
app.use(express.json());

// Endpoint de Autenticación utilizado por la interfaz clínica
app.post('/auth/token', (req, res) => {
    const { username, password } = req.body;

    // Validación de las credenciales institucionales
    if (username === 'admin' && password === 'corposucre2026') {
        // Generación del Token JWT firmado
        const token = jwt.sign({ sub: username, role: 'admin' }, SECRET_KEY, { expiresIn: '1h' });
        return res.json({ access_token: token });
    }

    return res.status(401).json({ error: "Credenciales inválidas o servicio caído." });
});

app.listen(PORT, () => {
    console.log(`Servidor de Autenticación de Seguridad corriendo en el puerto ${PORT}`);
});
