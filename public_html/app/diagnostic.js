// Diagnostic server to identify the exact issue
const fs = require('fs')
const path = require('path')

console.log('=== CarsEmpire PWA Diagnostic Server ===')
console.log('Node.js version:', process.version)
console.log('Platform:', process.platform)
console.log('Architecture:', process.arch)
console.log('Working directory:', process.cwd())
console.log('Environment:', process.env.NODE_ENV || 'development')
console.log('Port:', process.env.PORT || 3000)

// Check if required files exist
const filesToCheck = [
  'package.json',
  'server.js',
  'app.js',
  '.next',
  '.next/server',
  '.next/static',
  'public',
  'public/manifest.json',
  'public/sw.js'
]

console.log('\n=== File System Check ===')
filesToCheck.forEach(file => {
  const exists = fs.existsSync(file)
  console.log(`${exists ? '✅' : '❌'} ${file}: ${exists ? 'EXISTS' : 'MISSING'}`)
  
  if (exists && fs.statSync(file).isDirectory()) {
    try {
      const contents = fs.readdirSync(file)
      console.log(`   Contents: ${contents.slice(0, 5).join(', ')}${contents.length > 5 ? '...' : ''}`)
    } catch (err) {
      console.log(`   Error reading directory: ${err.message}`)
    }
  }
})

// Check package.json
console.log('\n=== Package.json Analysis ===')
try {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'))
  console.log('✅ package.json is valid JSON')
  console.log('Dependencies:', Object.keys(packageJson.dependencies || {}))
  console.log('Scripts:', Object.keys(packageJson.scripts || {}))
} catch (err) {
  console.log('❌ package.json error:', err.message)
}

// Check if Next.js can be loaded
console.log('\n=== Next.js Module Check ===')
try {
  const next = require('next')
  console.log('✅ Next.js module loaded successfully')
  console.log('Next.js version:', require('next/package.json').version)
} catch (err) {
  console.log('❌ Next.js module error:', err.message)
  console.log('Error details:', err.stack)
}

// Check if React can be loaded
console.log('\n=== React Module Check ===')
try {
  const react = require('react')
  console.log('✅ React module loaded successfully')
} catch (err) {
  console.log('❌ React module error:', err.message)
}

// Check if Express can be loaded
console.log('\n=== Express Module Check ===')
try {
  const express = require('express')
  console.log('✅ Express module loaded successfully')
} catch (err) {
  console.log('❌ Express module error:', err.message)
}

// Start a simple HTTP server
const port = process.env.PORT || 3000
const http = require('http')

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' })
  res.end(`
    <html>
      <head>
        <title>CarsEmpire PWA Diagnostic</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
          .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
          h1 { color: #0041ff; text-align: center; }
          .status { background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0; }
          .error { background: #ffe6e6; padding: 15px; border-radius: 5px; margin: 20px 0; }
          .success { background: #e6ffe6; padding: 15px; border-radius: 5px; margin: 20px 0; }
          pre { background: #f8f8f8; padding: 15px; border-radius: 5px; overflow-x: auto; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>🔍 CarsEmpire PWA Diagnostic</h1>
          <div class="success">
            <h3>✅ Diagnostic Server Running</h3>
            <p>This server is working correctly. Check the console logs for detailed diagnostics.</p>
          </div>
          <div class="status">
            <h3>📋 Next Steps:</h3>
            <ol>
              <li>Check the console logs in cPanel for detailed error information</li>
              <li>Look for any missing files or dependencies</li>
              <li>Verify that all required modules can be loaded</li>
              <li>Check file permissions and directory structure</li>
            </ol>
          </div>
          <div class="status">
            <h3>🔧 Common Issues:</h3>
            <ul>
              <li><strong>Missing .next directory:</strong> The Next.js build might not be complete</li>
              <li><strong>Missing dependencies:</strong> Run "NPM Install" in cPanel</li>
              <li><strong>File permissions:</strong> Ensure all files are readable by Node.js</li>
              <li><strong>Memory issues:</strong> Shared hosting might have memory limitations</li>
            </ul>
          </div>
          <button onclick="location.reload()" style="background: #0041ff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Refresh Page</button>
        </div>
      </body>
    </html>
  `)
})

server.listen(port, () => {
  console.log(`\n=== Diagnostic Server Started ===`)
  console.log(`Server running on port ${port}`)
  console.log(`Access: http://localhost:${port}`)
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`)
})
