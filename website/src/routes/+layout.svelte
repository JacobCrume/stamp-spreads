<script lang="ts">
	import type { Snippet } from 'svelte';
	import ChatWidget from '../lib/ChatWidget.svelte';
	import Wordmark from '../lib/Wordmark.svelte';
	import { themeState } from '../lib/theme.svelte';

	let { children }: { children: Snippet } = $props();

	// Color definitions for the floating dynamic header
	const themeColors = {
		hero: {
			bg: '#240340',
			border: '#e24bff',
			text: '#e24bff',
			btnBg: '#e24bff',
			btnText: '#240340'
		},
		steps: {
			bg: '#3b0764',
			border: '#e24bff',
			text: '#e24bff',
			btnBg: '#e24bff',
			btnText: '#3b0764'
		},
		butter: {
			bg: '#4a3000',
			border: '#ffd640',
			text: '#ffd640',
			btnBg: '#ffd640',
			btnText: '#4a3000'
		},
		raspberry: {
			bg: '#460820',
			border: '#ff467a',
			text: '#ff467a',
			btnBg: '#ff467a',
			btnText: '#460820'
		},
		yeast: {
			bg: '#240340',
			border: '#e24bff',
			text: '#e24bff',
			btnBg: '#e24bff',
			btnText: '#240340'
		},
		peanut: {
			bg: '#4e2408',
			border: '#ff8c30',
			text: '#ff8c30',
			btnBg: '#ff8c30',
			btnText: '#4e2408'
		},
		mixed: {
			bg: '#240340',
			border: '#e24bff',
			text: '#e24bff',
			btnBg: '#e24bff',
			btnText: '#240340'
		}
	};

	let currentTheme = $derived(themeColors[themeState.active] || themeColors.hero);
</script>

<svelte:head>
	<title>STAMP — Peel. Press. Toast.</title>
	<meta
		name="description"
		content="Stamp: Single-serve peel-and-press spread discs for toast. Bold flat breakfast innovation with no knife and no open jar."
	/>
</svelte:head>

<div class="site-container">
	<!-- FLOATING DYNAMIC HEADER - MATCHES BACKGROUND SECTION COLOR -->
	<header
		class="site-header floating-header"
		style:background-color={currentTheme.bg}
		style:border-color={currentTheme.border}
		style:color={currentTheme.text}
	>
		<div class="header-inner">
			<a href="/" class="brand-link" style:color={currentTheme.text}>
				<div class="header-wordmark-wrap">
					<Wordmark color={currentTheme.text} />
				</div>
			</a>
			<nav class="site-nav">
				<a href="/#steps" class="nav-link" style:color={currentTheme.text}>Gesture</a>
				<a href="/#flavours" class="nav-link" style:color={currentTheme.text}>Flavours</a>
				<a href="/flavours" class="nav-link" style:color={currentTheme.text}>Specs</a>
				<button
					type="button"
					class="nav-link chat-btn"
					style:background-color={currentTheme.btnBg}
					style:color={currentTheme.btnText}
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
				<div class="footer-brand-wrap">
					<Wordmark color="#e24bff" />
				</div>
				<p class="footer-tagline">PEEL. PRESS. TOAST.</p>
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

	/* FLOATING DYNAMIC HEADER - FLAT WITH NO SHADOW OR GLOW */
	.floating-header {
		position: fixed;
		top: 16px;
		left: 50%;
		transform: translateX(-50%);
		width: calc(100% - 32px);
		max-width: 1080px;
		border-radius: 9999px;
		z-index: 1000;
		border: 2px solid;
		transition:
			background-color 0.28s ease,
			border-color 0.28s ease,
			color 0.28s ease;
	}

	.header-inner {
		padding: 0.7rem 1.4rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.brand-link {
		display: flex;
		align-items: center;
		text-decoration: none;
	}

	.header-wordmark-wrap {
		width: 110px;
		display: block;
	}

	.site-nav {
		display: flex;
		align-items: center;
		gap: 1.15rem;
	}

	.nav-link {
		text-decoration: none;
		font-weight: 800;
		font-size: 0.92rem;
		transition: all 0.15s ease;
		background: transparent;
		border: none;
		cursor: pointer;
		font-family: inherit;
		letter-spacing: 0.02em;
	}

	.nav-link:hover {
		opacity: 0.8;
	}

	.chat-btn {
		padding: 0.45rem 1.15rem;
		border-radius: 9999px;
		font-weight: 900;
		font-size: 0.88rem;
		letter-spacing: 0.03em;
		border: none;
		cursor: pointer;
		transition: all 0.15s ease;
	}

	.chat-btn:hover {
		transform: scale(1.04);
	}

	.site-main {
		flex: 1;
	}

	/* FLAT FOOTER */
	.site-footer {
		background-color: #1a0230;
		border-top: 3px solid #e24bff;
		color: #f4c7ff;
		padding: 4.5rem 1.5rem 2.5rem;
	}

	.footer-inner {
		max-width: 1140px;
		margin: 0 auto;
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
		gap: 2.5rem;
	}

	.footer-brand-wrap {
		width: 140px;
		margin-bottom: 0.75rem;
	}

	.footer-tagline {
		font-weight: 900;
		font-size: 1.05rem;
		margin-bottom: 0.75rem;
		color: #f4c7ff;
		letter-spacing: 0.06em;
	}

	.footer-desc {
		font-size: 0.92rem;
		color: #d896ff;
		line-height: 1.5;
	}

	.footer-heading {
		font-size: 1.05rem;
		font-weight: 800;
		color: #e24bff;
		margin-bottom: 1rem;
		letter-spacing: 0.03em;
		text-transform: uppercase;
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
		max-width: 1140px;
		margin: 3rem auto 0;
		padding-top: 1.5rem;
		border-top: 1px solid rgba(226, 75, 255, 0.25);
		text-align: center;
		font-size: 0.85rem;
		color: #b56be8;
	}

	@media (max-width: 640px) {
		.floating-header {
			top: 10px;
			width: calc(100% - 20px);
		}
		.header-inner {
			padding: 0.55rem 0.9rem;
		}
		.header-wordmark-wrap {
			width: 88px;
		}
		.site-nav {
			gap: 0.5rem;
		}
		.nav-link {
			font-size: 0.8rem;
		}
		.chat-btn {
			padding: 0.35rem 0.75rem;
			font-size: 0.8rem;
		}
		.site-footer {
			padding: 3rem 1rem 1.5rem;
		}
		.footer-inner {
			grid-template-columns: 1fr;
			gap: 1.75rem;
		}
	}
</style>
