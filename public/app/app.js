// Alternative entry point for shared hosting
const express = require('express')
const next = require('next')

const dev = false
const app = next({ dev })
const handle = app.getRequestHandler()

const server = express()

app.prepare().then(() => {
  console.log('CarsEmpire PWA starting...')
  
  // Handle all requests
  server.all('*', (req, res) => {
    return handle(req, res)
  })
  
  const port = process.env.PORT || 3000
  server.listen(port, (err) => {
    if (err) throw err
    console.log(`> CarsEmpire PWA ready on port ${port}`)
  })
})
