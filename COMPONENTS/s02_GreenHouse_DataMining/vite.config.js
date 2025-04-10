import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'
import fs from 'fs';
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    https: {
      key: fs.readFileSync('/etc/letsencrypt/live/vps.joselp.com/privkey.pem'),
      cert: fs.readFileSync('/etc/letsencrypt/live/vps.joselp.com/fullchain.pem'),
    },
    host: true, 
    port: 80,
    allowedHosts: [
      'greenhouseiot-production.up.railway.app',  // Agregar dominio permitido
      'localhost',  // Permitir acceso desde localhost
      'greenhouse.joselp.com',
      'vps.joselp.com',
    ],
    watch: {
      usePolling: true,
    },
  },
});


