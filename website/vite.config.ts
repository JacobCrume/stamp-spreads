import adapter from '@sveltejs/adapter-vercel';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';

declare const process: { cwd: () => string; env: Record<string, string | undefined> };

export default defineConfig(({ mode }) => {
	// Load environment variables from .env / .env.local into process.env
	const env = loadEnv(mode, process.cwd(), '');
	process.env = { ...process.env, ...env };

	return {
		plugins: [
			sveltekit({
				compilerOptions: {
					// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
					runes: ({ filename }) =>
						filename.split(/[/\\]/).includes('node_modules') ? undefined : true
				},
				adapter: adapter()
			})
		]
	};
});

