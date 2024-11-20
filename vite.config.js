import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [sveltekit()],
    optimizeDeps: {
        include: ['@supabase/supabase-js'], // Ensure Supabase is bundled properly
    },
    ssr: {
        noExternal: ['@supabase/supabase-js'], // Prevent SSR issues with Supabase
    },
        define: {
            'process.env': process.env,
        },
    });
