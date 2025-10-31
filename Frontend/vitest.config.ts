import { defineConfig } from 'vitest/config';
import { fileURLToPath, URL } from 'node:url';
import { resolve } from 'path';
import { configDefaults } from 'vitest/config';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [vue()],
    test: {
        environment: 'happy-dom',
        root: fileURLToPath(new URL('./', import.meta.url)),
        coverage: {
            reporter: ['text', 'json', 'html'],
        },
        exclude: ['tests/e2e/**', ...configDefaults.exclude, 'packages/template/*']
    },
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
    },
});