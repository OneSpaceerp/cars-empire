// Robust server with better error handling for shared hosting
const { createServer } = require('http')
const { parse } = require('url')

console.log('Starting CarsEmpire PWA server...')
console.log('Environment:', process.env.NODE_ENV)
console.log('Port:', process.env.PORT || 3000)

// Try to load Next.js, but handle errors gracefully
let next, app, handle

try {
  next = require('next')
  console.log('Next.js loaded successfully')
} catch (err) {
  console.error('Failed to load Next.js:', err.message)
  console.log('Falling back to simple server...')
  
  // Fallback server
  const port = process.env.PORT || 3000
  const server = require('http').createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html' })
    res.end(`
      <html>
        <head>
          <title>CarsEmpire PWA</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #0041ff; text-align: center; }
            .status { background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .error { background: #ffe6e6; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .btn { background: #0041ff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
          </style>
        </head>
        <body>
          <div class="container">
            <h1>🚗 CarsEmpire PWA</h1>
            <div class="status">
              <h3>✅ Server is Running</h3>
              <p>Node.js server is working correctly on port ${port}</p>
            </div>
            <div class="error">
              <h3>⚠️ Next.js Issue</h3>
              <p>Next.js failed to load. This might be due to missing dependencies.</p>
              <p><strong>Error:</strong> ${err.message}</p>
            </div>
            <div class="status">
              <h3>🔧 Troubleshooting Steps:</h3>
              <ol>
                <li>Run "NPM Install" in cPanel</li>
                <li>Check if all files are uploaded correctly</li>
                <li>Verify package.json dependencies</li>
                <li>Try restarting the application</li>
              </ol>
            </div>
            <button class="btn" onclick="location.reload()">Refresh Page</button>
          </div>
        </body>
      </html>
    `)
  })
  
  server.listen(port, () => {
    console.log(`Fallback server running on port ${port}`)
  })
  
  process.exit(0)
}

// If Next.js loaded successfully, proceed with normal setup
const dev = false
const hostname = process.env.HOSTNAME || 'localhost'
const port = parseInt(process.env.PORT, 10) || 3000

app = next({ dev, hostname, port })
handle = app.getRequestHandler()

app.prepare().then(() => {
  console.log('Next.js app prepared successfully')
  
  createServer(async (req, res) => {
    try {
      console.log('Handling request:', req.url)
      const parsedUrl = parse(req.url, true)
      await handle(req, res, parsedUrl)
    } catch (err) {
      console.error('Error occurred handling', req.url, err)
      res.statusCode = 500
      res.end('internal server error')
    }
  })
    .once('error', (err) => {
      console.error('Server error:', err)
      process.exit(1)
    })
    .listen(port, hostname, () => {
      console.log(`> CarsEmpire PWA ready on http://${hostname}:${port}`)
      console.log(`> Environment: ${process.env.NODE_ENV || 'development'}`)
    })
})
.catch((err) => {
  console.error('Failed to prepare Next.js app:', err)
  process.exit(1)
})
