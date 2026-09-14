// Simple server that doesn't require Next.js
const http = require('http')
const fs = require('fs')
const path = require('path')

const port = process.env.PORT || 3000

console.log('Starting simple CarsEmpire PWA server...')
console.log('Port:', port)
console.log('Environment:', process.env.NODE_ENV || 'development')

// Check if required files exist
const filesToCheck = [
  'package.json',
  '.next',
  'public',
  'public/manifest.json'
]

console.log('\n=== File System Check ===')
filesToCheck.forEach(file => {
  const exists = fs.existsSync(file)
  console.log(`${exists ? '✅' : '❌'} ${file}: ${exists ? 'EXISTS' : 'MISSING'}`)
})

// Check package.json
try {
  if (fs.existsSync('package.json')) {
    const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'))
    console.log('✅ package.json is valid')
    console.log('Dependencies:', Object.keys(packageJson.dependencies || {}))
  } else {
    console.log('❌ package.json not found')
  }
} catch (err) {
  console.log('❌ package.json error:', err.message)
}

// Check if .next directory has content
if (fs.existsSync('.next')) {
  try {
    const nextContents = fs.readdirSync('.next')
    console.log('✅ .next directory contents:', nextContents.slice(0, 5))
  } catch (err) {
    console.log('❌ .next directory error:', err.message)
  }
}

const server = http.createServer((req, res) => {
  console.log('Handling request:', req.url)
  
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200)
    res.end()
    return
  }
  
  // Serve static files from public directory
  if (req.url.startsWith('/public/') || req.url === '/manifest.json' || req.url === '/sw.js') {
    const filePath = path.join(__dirname, 'public', req.url.replace('/public/', ''))
    
    if (fs.existsSync(filePath)) {
      const ext = path.extname(filePath)
      const contentType = {
        '.json': 'application/json',
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.html': 'text/html',
        '.ico': 'image/x-icon',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.svg': 'image/svg+xml'
      }[ext] || 'text/plain'
      
      res.writeHead(200, { 'Content-Type': contentType })
      fs.createReadStream(filePath).pipe(res)
      return
    }
  }
  
  // Serve the main PWA application
  if (req.url === '/' || req.url === '/index.html') {
    try {
      const indexPath = path.join(__dirname, 'index.html')
      if (fs.existsSync(indexPath)) {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        fs.createReadStream(indexPath).pipe(res)
        return
      }
    } catch (err) {
      console.log('Error serving index.html:', err.message)
    }
  }
  
  // Default response (fallback)
  res.writeHead(200, { 'Content-Type': 'text/html' })
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
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #0041ff, #0066ff); color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .container { text-align: center; }
            .spinner { width: 40px; height: 40px; border: 4px solid rgba(255,255,255,0.3); border-top: 4px solid white; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
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
  `)
})

server.listen(port, () => {
  console.log(`\n=== Simple Server Started ===`)
  console.log(`Server running on port ${port}`)
  console.log(`Access: http://localhost:${port}`)
})