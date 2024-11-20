import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
  extensions: ['.svelte'],
  preprocess: [vitePreprocess()],
  kit: {
    adapter: adapter(),
    alias: {
      $lib: 'src/lib',  // Alias correctly mapped
    },
  },
};
export default config;
