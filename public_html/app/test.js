// Simple test server to verify Node.js is working
const http = require('http')

const port = process.env.PORT || 3000

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' })
  res.end(`
    <html>
      <head><title>CarsEmpire PWA Test</title></head>
      <body>
        <h1>🚗 CarsEmpire PWA Test Server</h1>
        <p>✅ Node.js is working!</p>
        <p>Port: ${port}</p>
        <p>Environment: ${process.env.NODE_ENV || 'development'}</p>
        <p>Time: ${new Date().toISOString()}</p>
      </body>
    </html>
  `)
})

server.listen(port, () => {
  console.log(`Test server running on port ${port}`)
})
