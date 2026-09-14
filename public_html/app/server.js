const http = require('http');
const path = require('path');
const fs = require('fs');

const port = process.env.PORT || 3000;
const hostname = '0.0.0.0';

const server = http.createServer((req, res) => {
    console.log(`Request received: ${req.url}`);

    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    // Handle preflight requests
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    // Serve static files
    const publicPath = path.join(__dirname);
    let requestedPath = path.join(publicPath, req.url);

    // Prevent directory traversal
    if (!requestedPath.startsWith(publicPath)) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('403 Forbidden');
        return;
    }

    // Default to index.html for root requests
    if (req.url === '/' || req.url === '') {
        requestedPath = path.join(publicPath, 'index.html');
    }

    // Check if the requested path is a file
    if (fs.existsSync(requestedPath) && fs.lstatSync(requestedPath).isFile()) {
        const ext = path.extname(requestedPath).toLowerCase();
        let contentType = 'application/octet-stream';

        switch (ext) {
            case '.html':
                contentType = 'text/html';
                break;
            case '.js':
                contentType = 'text/javascript';
                break;
            case '.css':
                contentType = 'text/css';
                break;
            case '.json':
                contentType = 'application/json';
                break;
            case '.png':
                contentType = 'image/png';
                break;
            case '.jpg':
            case '.jpeg':
                contentType = 'image/jpeg';
                break;
            case '.gif':
                contentType = 'image/gif';
                break;
            case '.svg':
                contentType = 'image/svg+xml';
                break;
            case '.ico':
                contentType = 'image/x-icon';
                break;
            case '.webmanifest':
                contentType = 'application/manifest+json';
                break;
        }

        res.writeHead(200, { 'Content-Type': contentType });
        fs.createReadStream(requestedPath).pipe(res);
        return;
    }

    // Serve the main PWA application
    if (req.url === '/' || req.url === '/index.html') {
        try {
            const indexPath = path.join(__dirname, 'index.html');
            if (fs.existsSync(indexPath)) {
                res.writeHead(200, { 'Content-Type': 'text/html' });
                fs.createReadStream(indexPath).pipe(res);
                return;
            }
        } catch (err) {
            console.log('Error serving index.html:', err.message);
        }
    }

    // Default response (fallback)
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CarsEmpire PWA - Loading...</title>
            <link rel="manifest" href="/manifest.json">
            <meta name="theme-color" content="#0041ff">
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background: linear-gradient(135deg, #0041ff, #0066ff); 
                    color: white; 
                    min-height: 100vh; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                }
                .container { text-align: center; }
                .spinner { 
                    width: 40px; 
                    height: 40px; 
                    border: 4px solid rgba(255,255,255,0.3); 
                    border-top: 4px solid white; 
                    border-radius: 50%; 
                    animation: spin 1s linear infinite; 
                    margin: 0 auto 20px; 
                }
                @keyframes spin { 
                    0% { transform: rotate(0deg); } 
                    100% { transform: rotate(360deg); } 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="spinner"></div>
                <h1>🚗 CarsEmpire PWA</h1>
                <p>Loading your car services platform...</p>
            </div>
        </body>
        </html>
    `);
});

server.listen(port, hostname, () => {
    console.log(`\n=== CarsEmpire PWA Server Started ===`);
    console.log(`Server running on http://${hostname}:${port}`);
    console.log(`Access your PWA at: http://${hostname}:${port}`);
    console.log(`API Base URL: ${process.env.NEXT_PUBLIC_API_URL || 'Not Set'}`);
    console.log(`App Base URL: ${process.env.NEXT_PUBLIC_APP_URL || 'Not Set'}`);

    // Diagnostic checks
    console.log('\n--- Diagnostic Checks ---');
    const filesToCheck = ['package.json', 'index.html', 'logo.svg', 'manifest.json'];
    filesToCheck.forEach(file => {
        const exists = fs.existsSync(file);
        console.log(`${exists ? '✅' : '❌'} ${file}: ${exists ? 'EXISTS' : 'MISSING'}`);
    });

    console.log('-------------------------');
});