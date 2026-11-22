import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import { resolve } from 'node:path';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  base: '/app',
  build: {
    emptyOutDir: true,
    outDir: resolve(__dirname, 'dist'),
  },
  plugins: [
    react(),
    tailwindcss(),
    tsconfigPaths({
      configNames: ['tsconfig.json'],
    }),
  ],
  // used for development purposes - allows hot-reloading
  server: {
    host: '0.0.0.0',
    port: 8080,
    proxy: {
      '/api': {
        target: process.env.API_BASE_URL,
      },
    },
    strictPort: true,
  },
});
