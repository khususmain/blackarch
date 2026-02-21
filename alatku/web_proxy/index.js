const http = require('http');
const https = require('https');

http.createServer((req, res) => {
    const fullUrl = new URL(req.url, `http://${req.headers.host}`);
    let targetUrl = fullUrl.searchParams.get('url');

    if (!targetUrl) {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        return res.end(`
            <style>
                body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background: #0f0f0f; color: #ff0000; }
                .container { background: #1e1e1e; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; }
                input { padding: 15px; width: 350px; border-radius: 8px; border: 1px solid #333; background: #121212; color: white; font-size: 16px; }
                button { padding: 15px 25px; border-radius: 8px; border: none; background: #ff0000; color: white; cursor: pointer; font-weight: bold; font-size: 16px; margin-top: 15px; transition: 0.3s; }
                button:hover { background: #cc0000; transform: scale(1.05); }
                h1 { margin-bottom: 20px; font-size: 28px; letter-spacing: -1px; }
            </style>
            <div class="container">
                <h1>ASTRO PROXY V2</h1>
                <form action="/" method="GET">
                    <input name="url" placeholder="https://youtube.com" required>
                    <br>
                    <button type="submit">SURF SECURELY</button>
                </form>
                <p style="color: #666; margin-top: 20px; font-size: 12px;">Note: YouTube might be slow due to heavy asset loading.</p>
            </div>
        `);
    }

    if (!targetUrl.startsWith('http')) targetUrl = 'https://' + targetUrl;

    try {
        const parsedUrl = new URL(targetUrl);
        const options = {
            hostname: parsedUrl.hostname,
            port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
            path: parsedUrl.pathname + parsedUrl.search,
            method: req.method,
            headers: {
                ...req.headers,
                host: parsedUrl.hostname,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'referer': parsedUrl.origin,
                'origin': parsedUrl.origin
            }
        };

        delete options.headers['accept-encoding']; // Avoid compressed data for easier rewriting if needed

        const proxyReq = (parsedUrl.protocol === 'https:' ? https : http).request(options, (proxyRes) => {
            // Handle Redirects
            if ([301, 302, 307, 308].includes(proxyRes.statusCode) && proxyRes.headers.location) {
                const redirUrl = new URL(proxyRes.headers.location, targetUrl).href;
                res.writeHead(302, { 'Location': `/?url=${encodeURIComponent(redirUrl)}` });
                return res.end();
            }

            // Inject Base Tag and Rewrite Links for HTML
            const contentType = proxyRes.headers['content-type'] || '';
            if (contentType.includes('text/html')) {
                res.writeHead(proxyRes.statusCode, { ...proxyRes.headers, 'content-encoding': 'identity' });
                let body = '';
                proxyRes.on('data', chunk => { body += chunk; });
                proxyRes.on('end', () => {
                    const baseTag = `<base href="${parsedUrl.origin}${parsedUrl.pathname}">`;
                    // Simple regex to rewrite common links to stay in proxy
                    let updatedBody = body.replace(/href="\/([^"]+)"/g, `href="/?url=${encodeURIComponent(parsedUrl.origin)}/$1"`);
                    updatedBody = updatedBody.replace('<head>', `<head>${baseTag}`).replace('<HEAD>', `<HEAD>${baseTag}`);
                    res.end(updatedBody || body);
                });
            } else {
                res.writeHead(proxyRes.statusCode, proxyRes.headers);
                proxyRes.pipe(res);
            }
        });

        proxyReq.on('error', (e) => {
            res.writeHead(500);
            res.end('<h1>Proxy Error</h1><p>' + e.message + '</p>');
        });

        req.pipe(proxyReq);
    } catch (err) {
        res.writeHead(400);
        res.end('Invalid URL format.');
    }
}).listen(9095, '0.0.0.0');
