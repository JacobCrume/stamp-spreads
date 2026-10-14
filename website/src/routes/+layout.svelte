<script lang="ts">
	import type { Snippet } from 'svelte';
	import ChatWidget from '../lib/ChatWidget.svelte';
	let { children }: { children: Snippet } = $props();
</script>

<svelte:head>
	<title>STAMP — Peel. Press. Toast.</title>
	<meta
		name="description"
		content="Stamp: Single-serve peel-and-press spread discs for toast. No knife, no open jar."
	/>
</svelte:head>

<div class="site-container">
	<header class="site-header">
		<div class="header-inner">
			<a href="/" class="brand-link">
				<img src="/logo.png" alt="STAMP" class="brand-logo" />
			</a>
			<nav class="site-nav">
				<a href="/" class="nav-link">Home</a>
				<a href="/flavours" class="nav-link">Flavours</a>
				<button
					type="button"
					class="nav-link chat-btn"
					onclick={() => {
						if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent('stamp:open-chat'));
					}}>Ask Stamp</button
				>
			</nav>
		</div>
	</header>

	<main class="site-main">
		{@render children()}
	</main>

	<ChatWidget />

	<footer class="site-footer">
		<div class="footer-inner">
			<div class="footer-col">
				<div class="footer-brand">STAMP</div>
				<p class="footer-tagline">Peel. Press. Toast.</p>
				<p class="footer-desc">
					10 g single-serve spread portions on food-safe release film. Pantry-stable for 12 months
					unopened.
				</p>
			</div>
			<div class="footer-col">
				<h4 class="footer-heading">Navigation</h4>
				<ul class="footer-links">
					<li><a href="/">Home</a></li>
					<li><a href="/flavours">Flavours & Range</a></li>
					<li>
						<button
							type="button"
							class="footer-link-btn"
							onclick={() => {
								if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent('stamp:open-chat'));
							}}>Customer Support Bot</button
						>
					</li>
				</ul>
			</div>
			<div class="footer-col">
				<h4 class="footer-heading">Product Integrity</h4>
				<p class="footer-note">
					$5.00 NZD per 8-stamp sheet ($6.25 / 100 g). No false certification marks or therapeutic
					claims. Produced in a facility handling milk, gluten, and peanuts.
				</p>
			</div>
		</div>
		<div class="footer-bottom">
			<p>© 2026 Stamp Spreads Ltd — Auckland, New Zealand. All rights reserved.</p>
		</div>
	</footer>
</div>

<style>
	@font-face {
		font-family: 'Manrope';
		src: url('/fonts/Manrope-400.ttf') format('truetype');
		font-weight: 400;
		font-style: normal;
	}
	@font-face {
		font-family: 'Manrope';
		src: url('/fonts/Manrope-500.ttf') format('truetype');
		font-weight: 500;
		font-style: normal;
	}
	@font-face {
		font-family: 'Manrope';
		src: url('/fonts/Manrope-600.ttf') format('truetype');
		font-weight: 600;
		font-style: normal;
	}
	@font-face {
		font-family: 'Manrope';
		src: url('/fonts/Manrope-700.ttf') format('truetype');
		font-weight: 700;
		font-style: normal;
	}

	:global(*) {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}

	:global(body) {
		font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		background-color: #fcfbfe;
		color: #1a1024;
		line-height: 1.6;
		-webkit-font-smoothing: antialiased;
	}

	.site-container {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	.site-header {
		position: sticky;
		top: 0;
		z-index: 50;
		background-color: #ffffff;
		border-bottom: 2px solid #e24bff;
		box-shadow: 0 2px 10px rgba(59, 7, 100, 0.05);
	}

	.header-inner {
		max-width: 1120px;
		margin: 0 auto;
		padding: 0.75rem 1.5rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.brand-link {
		display: flex;
		align-items: center;
		text-decoration: none;
	}

	.brand-logo {
		height: 38px;
		width: auto;
		border-radius: 4px;
	}

	.site-nav {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}

	.nav-link {
		font-weight: 600;
		font-size: 0.95rem;
		color: #3b0764;
		text-decoration: none;
		transition: color 0.15s ease;
	}

	.nav-link:hover {
		color: #e24bff;
	}

	.chat-btn {
		background-color: #3b0764;
		color: #ffffff !important;
		padding: 0.5rem 1rem;
		border-radius: 6px;
		transition: background-color 0.15s ease;
	}

	.chat-btn:hover {
		background-color: #550a8a;
	}

	.site-main {
		flex: 1;
	}

	.site-footer {
		background-color: #3b0764;
		color: #ffffff;
		padding: 3rem 1.5rem 1.5rem;
		border-top: 3px solid #e24bff;
	}

	.footer-inner {
		max-width: 1120px;
		margin: 0 auto;
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
		gap: 2.5rem;
	}

	.footer-brand {
		font-size: 1.8rem;
		font-weight: 800;
		letter-spacing: -0.02em;
		color: #e24bff;
		margin-bottom: 0.25rem;
	}

	.footer-tagline {
		font-weight: 700;
		font-size: 1.05rem;
		margin-bottom: 0.75rem;
		color: #ffffff;
	}

	.footer-desc {
		font-size: 0.88rem;
		opacity: 0.85;
		line-height: 1.5;
	}

	.footer-heading {
		font-size: 1.05rem;
		font-weight: 700;
		color: #e24bff;
		margin-bottom: 0.75rem;
	}

	.footer-links {
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.footer-links a,
	.footer-link-btn {
		color: #ffffff;
		text-decoration: none;
		font-size: 0.9rem;
		opacity: 0.85;
		transition: opacity 0.15s;
		background: transparent;
		border: none;
		cursor: pointer;
		padding: 0;
		text-align: left;
		font-family: inherit;
	}

	.footer-links a:hover,
	.footer-link-btn:hover {
		opacity: 1;
		color: #e24bff;
	}

	.footer-note {
		font-size: 0.85rem;
		opacity: 0.8;
		line-height: 1.5;
	}

	.footer-bottom {
		max-width: 1120px;
		margin: 2.5rem auto 0;
		padding-top: 1.5rem;
		border-top: 1px solid rgba(226, 75, 255, 0.2);
		text-align: center;
		font-size: 0.82rem;
		opacity: 0.7;
	}

	@media (max-width: 640px) {
		.header-inner {
			padding: 0.75rem 1rem;
		}
		.site-nav {
			gap: 0.75rem;
		}
		.nav-link {
			font-size: 0.88rem;
		}
		.chat-btn {
			padding: 0.4rem 0.75rem;
		}
	}
</style>
