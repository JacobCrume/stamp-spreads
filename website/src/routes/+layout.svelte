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
				<a href="/#flavours" class="nav-link">Flavours</a>
				<a href="/flavours" class="nav-link">Specs & Nutrition</a>
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
					10 g single-serve spread portions on food-safe release film. 12 months ambient pantry stability.
				</p>
			</div>
			<div class="footer-col">
				<h4 class="footer-heading">Range & Navigation</h4>
				<ul class="footer-links">
					<li><a href="/#steps">The 3-Step Gesture</a></li>
					<li><a href="/#flavours">4 Launch Flavours</a></li>
					<li><a href="/flavours">Full Nutritional Specs</a></li>
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
					$5.00 NZD per 8-stamp sheet ($6.25 / 100 g). No false certification marks or therapeutic claims. Produced in a facility handling milk, gluten, and peanuts.
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

	:global(html) {
		scroll-behavior: smooth;
		background-color: #3b0764;
	}

	:global(body) {
		font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		background-color: #3b0764;
		color: #f4c7ff;
		line-height: 1.6;
		-webkit-font-smoothing: antialiased;
		overflow-x: hidden;
	}

	.site-container {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		background-color: #3b0764;
	}

	.site-header {
		position: sticky;
		top: 0;
		z-index: 100;
		background-color: #240340;
		border-bottom: 2px solid #e24bff;
		box-shadow: 0 4px 20px rgba(226, 75, 255, 0.15);
	}

	.header-inner {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0.85rem 1.5rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.brand-link {
		display: flex;
		align-items: center;
		text-decoration: none;
	}

	.brand-logo {
		height: 44px;
		width: auto;
		display: block;
		filter: drop-shadow(0 2px 8px rgba(226, 75, 255, 0.4));
	}

	.site-nav {
		display: flex;
		align-items: center;
		gap: 1.25rem;
	}

	.nav-link {
		color: #e24bff;
		text-decoration: none;
		font-weight: 700;
		font-size: 0.95rem;
		transition: all 0.15s ease;
		background: transparent;
		border: none;
		cursor: pointer;
		font-family: inherit;
	}

	.nav-link:hover {
		color: #ff9eff;
		transform: translateY(-1px);
	}

	.chat-btn {
		background: #e24bff;
		color: #3b0764;
		padding: 0.5rem 1.15rem;
		border-radius: 9999px;
		font-weight: 800;
		font-size: 0.9rem;
		letter-spacing: 0.02em;
		box-shadow: 0 2px 12px rgba(226, 75, 255, 0.4);
	}

	.chat-btn:hover {
		background: #ff85ff;
		color: #240340;
		box-shadow: 0 4px 18px rgba(226, 75, 255, 0.6);
		transform: translateY(-2px);
	}

	.site-main {
		flex: 1;
	}

	.site-footer {
		background-color: #1a0230;
		border-top: 3px solid #e24bff;
		color: #f4c7ff;
		padding: 4rem 1.5rem 2.5rem;
	}

	.footer-inner {
		max-width: 1200px;
		margin: 0 auto;
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
		gap: 2.5rem;
	}

	.footer-brand {
		font-size: 2.2rem;
		font-weight: 800;
		letter-spacing: -0.02em;
		color: #e24bff;
		margin-bottom: 0.25rem;
	}

	.footer-tagline {
		font-weight: 800;
		font-size: 1.1rem;
		margin-bottom: 0.75rem;
		color: #f4c7ff;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.footer-desc {
		font-size: 0.92rem;
		color: #d896ff;
		line-height: 1.5;
	}

	.footer-heading {
		font-size: 1.1rem;
		font-weight: 800;
		color: #e24bff;
		margin-bottom: 1rem;
		letter-spacing: 0.02em;
	}

	.footer-links {
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}

	.footer-links a,
	.footer-link-btn {
		color: #f4c7ff;
		text-decoration: none;
		font-size: 0.92rem;
		transition: all 0.15s;
		background: transparent;
		border: none;
		cursor: pointer;
		padding: 0;
		text-align: left;
		font-family: inherit;
		font-weight: 600;
	}

	.footer-links a:hover,
	.footer-link-btn:hover {
		color: #e24bff;
		transform: translateX(3px);
	}

	.footer-note {
		font-size: 0.88rem;
		color: #d896ff;
		line-height: 1.5;
	}

	.footer-bottom {
		max-width: 1200px;
		margin: 3rem auto 0;
		padding-top: 1.5rem;
		border-top: 1px solid rgba(226, 75, 255, 0.25);
		text-align: center;
		font-size: 0.85rem;
		color: #b56be8;
	}

	@media (max-width: 640px) {
		.header-inner {
			padding: 0.75rem 1rem;
		}
		.brand-logo {
			height: 36px;
		}
		.site-nav {
			gap: 0.6rem;
		}
		.nav-link {
			font-size: 0.82rem;
			padding: 0.3rem 0.4rem;
		}
		.chat-btn {
			padding: 0.35rem 0.75rem;
			font-size: 0.82rem;
		}
		.site-footer {
			padding: 2.5rem 1rem 1.5rem;
		}
		.footer-inner {
			grid-template-columns: 1fr;
			gap: 1.75rem;
		}
	}
</style>
