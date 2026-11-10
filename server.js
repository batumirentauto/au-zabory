const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  let reqPath = decodeURI(req.url.split('?')[0]);

  // Health check
  if (reqPath === '/health' || reqPath === '/api/health') {
    res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('OK');
    return;
  }

  // Strip leading /fencing or /au-zabory prefix if passed through reverse proxy
  if (reqPath.startsWith('/fencing/')) {
    reqPath = reqPath.slice('/fencing'.length);
  } else if (reqPath === '/fencing') {
    reqPath = '/';
  } else if (reqPath.startsWith('/au-zabory/')) {
    reqPath = reqPath.slice('/au-zabory'.length);
  } else if (reqPath === '/au-zabory') {
    reqPath = '/';
  }

  // Default root to hub / index
  if (reqPath === '/' || reqPath === '') {
    reqPath = '/index.html';
  }

  let filePath = path.join(__dirname, reqPath);

  // If path is a direct slug (e.g. /underwood-fencing-and-gates), check sites/<slug>/index.html
  if (!fs.existsSync(filePath)) {
    const slugWithoutSlash = reqPath.replace(/^\/+|\/+$/g, '');
    const siteSlugPath = path.join(__dirname, 'sites', slugWithoutSlash, 'index.html');
    if (fs.existsSync(siteSlugPath)) {
      filePath = siteSlugPath;
    }
  }

  // If directory, load index.html inside it
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    filePath = path.join(filePath, 'index.html');
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found');
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';
    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': 'public, max-age=3600'
    });
    res.end(data);
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`AU Zabory server running on port ${PORT}`);
});
