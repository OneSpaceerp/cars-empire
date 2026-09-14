# 🔧 CarsEmpire PWA - Troubleshooting Guide

## 503 Service Unavailable Error

### Quick Fixes to Try:

1. **Run NPM Install**
   - In cPanel Node.js interface, click "Run NPM Install"
   - Wait for installation to complete

2. **Restart the Application**
   - Click "RESTART" button in cPanel
   - Wait 30 seconds and try accessing the site again

3. **Check Application Status**
   - Look for any error messages in cPanel
   - Check if the application is actually running

### Alternative Startup Files:

If `server.js` doesn't work, try changing the startup file to:
- `app.js` (Express-based server)
- `index.js` (if you create one)

### Environment Variables Check:

Make sure these are set in cPanel:
- `NODE_ENV=production`
- `PORT=3000`
- `NEXT_PUBLIC_API_URL=https://carsempire.net/api`
- `NEXT_PUBLIC_APP_URL=https://app.carsempire.net`

### Common Issues:

1. **Missing Dependencies**
   - Solution: Run "NPM Install" in cPanel

2. **Wrong Startup File**
   - Try changing from `server.js` to `app.js`

3. **Port Conflicts**
   - Check if port 3000 is available
   - Try changing PORT environment variable

4. **File Permissions**
   - Ensure all files are readable by the Node.js process

### Debug Steps:

1. Check the application logs in cPanel
2. Verify all files are uploaded correctly
3. Test with a simple Node.js app first
4. Contact hosting support if issues persist

### Alternative Deployment:

If Node.js continues to fail, consider:
- Static export deployment
- Serverless deployment (Vercel/Netlify)
- Docker deployment
