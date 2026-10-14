<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import Wordmark from '../lib/Wordmark.svelte';
	import { colorScheme, setSectionTheme, type SectionTheme } from '../lib/theme.svelte';

	let scrollY = $state(0);
	let innerHeight = $state(800);
	let innerWidth = $state(1200);

	// Explosion on threshold
	let isExploded = $state(false);

	// Interactive 3D lift & flip state for each flavour card
	let flipped: Record<string, boolean> = $state({
		butter: false,
		raspberry: false,
		yeast: false,
		peanut: false
	});

	function toggleFlip(id: string) {
		flipped[id] = !flipped[id];
	}

	onMount(() => {
		// Active section observer to smoothly change the global colorScheme object
		const updateActiveSection = () => {
			const sections: { id: string; theme: SectionTheme }[] = [
				{ id: 'hero-section', theme: 'hero' },
				{ id: 'steps-section', theme: 'steps' },
				{ id: 'flavour-butter', theme: 'butter' },
				{ id: 'flavour-raspberry', theme: 'raspberry' },
				{ id: 'flavour-yeast', theme: 'yeast' },
				{ id: 'flavour-peanut', theme: 'peanut' },
				{ id: 'mixed-section', theme: 'mixed' }
			];

			const triggerY = window.innerHeight * 0.45;
			for (const sec of sections) {
				const el = document.getElementById(sec.id);
				if (el) {
					const rect = el.getBoundingClientRect();
					if (rect.top <= triggerY && rect.bottom >= triggerY) {
						setSectionTheme(sec.theme);
						break;
					}
				}
			}
		};

		window.addEventListener('scroll', updateActiveSection, { passive: true });
		updateActiveSection();
	});

	onDestroy(() => {
		if (typeof window !== 'undefined') {
			// clean up
		}
	});

	// Trigger explosion on threshold
	$effect(() => {
		const stepsEl = document.getElementById('steps-section');
		if (stepsEl) {
			const rect = stepsEl.getBoundingClientRect();
			if (rect.top < innerHeight * 0.55 && !isExploded) {
				isExploded = true;
			} else if (rect.top > innerHeight * 0.85 && isExploded) {
				isExploded = false;
			}
		}
	});
</script>

<svelte:window bind:scrollY bind:innerHeight bind:innerWidth />

<svelte:head>
	<title>STAMP — Peel. Press. Toast.</title>
	<meta
		name="description"
		content="Stamp: Single-serve peel-and-press spread discs for toast. Bold flat breakfast innovation with no knife and no open jar."
	/>
</svelte:head>

<!-- SECTION 1: BALANCED, HIGH-IMPACT HERO -->
<section id="hero-section" class="hero-clean-stage">
	<div class="hero-clean-inner">
		<!-- Authentic Drawn STAMP Vector Wordmark (uses colorScheme.primary) -->
		<div class="hero-wordmark-container">
			<Wordmark color={colorScheme.primary} />
		</div>

		<h1 class="hero-tagline">PEEL. PRESS. TOAST.</h1>

		<p class="hero-lead">
			Single-serve 10 g spread discs on release film. Pressed onto hot toast, it softens into an even layer in seconds — no knife, no messy jar, no wash-up.
		</p>

		<!-- Packshot Showcase (Flat Solid, Zero Outlines) -->
		<div class="hero-pack-showcase">
			<div class="hero-pack-wrap">
				<img src="/pack.png" alt="STAMP 8-Stamp Sheet" class="hero-pack-img" />
				<div class="hero-pack-pill">8 DISCS · 80 g</div>
			</div>
		</div>

		<div class="hero-badges-row">
			<span class="hero-badge">$5.00 NZD / Sheet</span>
			<span class="hero-badge">12-Month Pantry Stable</span>
			<span class="hero-badge">No Jar Waste</span>
		</div>

		<div class="hero-actions-row">
			<a href="#flavours" class="hero-btn-primary">Explore The 4 Flavours ↓</a>
			<a href="#steps" class="hero-btn-secondary">How Stamp Works ↓</a>
		</div>
	</div>
</section>

<!-- SECTION 2: THE 3 STEPS WITH THRESHOLD EXPLOSION (FLAT, ZERO OUTLINES) -->
<section id="steps-section" class="steps-stage">
	<div class="steps-inner">
		<div class="section-kicker">THE 3-SECOND GESTURE</div>
		<h2 class="section-title">HOW STAMP WORKS</h2>
		<p class="section-sub">
			Forget sticky jars, table knives, and office sinks. Breakfast happens in three rapid moves.
		</p>

		<!-- Threshold Explosion Status & Interactive Toggle -->
		<div class="threshold-control-bar">
			<button
				type="button"
				class="threshold-btn"
				onclick={() => (isExploded = !isExploded)}
			>
				{isExploded ? '↺ Reset 3 Steps' : '💥 Trigger Explosion'}
			</button>
			<span class="threshold-status">
				{isExploded ? 'Steps exploded past threshold' : 'Scroll past threshold or click to trigger'}
			</span>
		</div>

		<div class="steps-grid {isExploded ? 'exploded' : ''}">
			<!-- Step 1: Explodes Top-Left on threshold -->
			<div class="step-card step-card-1 {isExploded ? 'blast-tl' : ''}">
				<div class="step-badge">01</div>
				<h3 class="step-label">PEEL</h3>
				<p class="step-text">
					Peel one 10 g disc off the food-grade release film. Sits clean and dry in your fingers.
				</p>
				<div class="flat-rule"></div>
			</div>

			<!-- Step 2: Blasts Downwards on threshold -->
			<div class="step-card step-card-2 {isExploded ? 'blast-down' : ''}">
				<div class="step-badge">02</div>
				<h3 class="step-label">PRESS</h3>
				<p class="step-text">
					Press the disc directly onto fresh hot toast. No table knife required.
				</p>
				<div class="flat-rule"></div>
			</div>

			<!-- Step 3: Explodes Top-Right on threshold -->
			<div class="step-card step-card-3 {isExploded ? 'blast-tr' : ''}">
				<div class="step-badge">03</div>
				<h3 class="step-label">SPREAD</h3>
				<p class="step-text">
					Thermal contact melts the disc into toast grooves within 3 seconds. Enjoy clean breakfast.
				</p>
				<div class="flat-rule"></div>
			</div>
		</div>

		{#if isExploded}
			<div class="exploded-banner">
				<div class="alert-box">
					<span class="alert-icon">⚡</span>
					<span>STEPS DISPERSED · PROCEED TO 4 LAUNCH FLAVOURS BELOW</span>
				</div>
			</div>
		{/if}
	</div>
</section>

<!-- SECTIONS 3-6: DEDICATED FULL-SCREEN IMMERSIVE FLAVOUR WORLDS (FLAT, ZERO OUTLINES) -->
<div id="flavours" class="flavour-worlds-list">
	<!-- FLAVOUR 1: SALTED BUTTER -->
	<section id="flavour-butter" class="flavour-screen">
		<div class="flavour-content-grid">
			<div class="flavour-media-side">
				<!-- 3D Lift & Flip Card (Flat Solid Surfaces, No Outline Borders) -->
				<div class="flip-stage">
					<div class="flip-card {flipped.butter ? 'flipped' : ''}">
						<div class="flip-face flip-front">
							<img src="/flavours/butter.png" alt="Salted Butter Stamp Pack" class="flavour-pack-img" />
						</div>
						<div class="flip-face flip-back">
							<img src="/flavours/butter-back.png" alt="Salted Butter Nutritional Panel" class="flavour-pack-img" />
						</div>
					</div>
				</div>

				<!-- Animated Lift & Flip Button (Flat Solid Pill, No Outlines) -->
				<button
					type="button"
					class="flat-flip-trigger"
					class:is-flipped={flipped.butter}
					onclick={() => toggleFlip('butter')}
					aria-label="Lift and flip Salted Butter card"
				>
					<span class="flip-icon-wrap" class:is-rotated={flipped.butter}>
						<svg class="flip-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
							<path d="M21 2v6h-6"></path>
							<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
							<path d="M3 22v-6h6"></path>
							<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
						</svg>
					</span>
					<span class="flip-btn-text">
						{flipped.butter ? 'Flip To Front Pack' : 'Lift & Flip: View Back Ingredients'}
					</span>
					<span class="flip-badge-pill">
						{flipped.butter ? 'BACK PANEL' : '3D LIFT'}
					</span>
				</button>
			</div>

			<div class="flavour-copy-side">
				<div class="flavour-index">01 / FOUR LAUNCH FLAVOURS</div>
				<h2 class="flavour-headline">SALTED BUTTER</h2>
				<p class="flavour-lead">
					Cultured butterfat and salt (78 g fat to 2 g salt). Formulated with low moisture so it is ambient pantry-stable for 12 months, yet melts instantly across hot toast without tearing the crumb.
				</p>

				<div class="flat-specs-grid">
					<div class="flat-spec-item">
						<span class="spec-kicker">FORMULA</span>
						<span class="spec-data">78 g butterfat · 2 g salt</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">ALLERGEN</span>
						<span class="spec-data">CONTAINS MILK</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">STABILITY</span>
						<span class="spec-data">12 Months Ambient</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">PORTION</span>
						<span class="spec-data">10 g Discs · 8 per Sheet</span>
					</div>
				</div>

				<div class="flat-callout">
					Sold as a shelf-stable butter spread, not a pat of fridge butter. Zero added vegetable oils or artificial preservatives.
				</div>
			</div>
		</div>
	</section>

	<!-- FLAVOUR 2: RASPBERRY -->
	<section id="flavour-raspberry" class="flavour-screen">
		<div class="flavour-content-grid">
			<div class="flavour-media-side">
				<!-- 3D Lift & Flip Card (Flat Solid Surfaces, No Outline Borders) -->
				<div class="flip-stage">
					<div class="flip-card {flipped.raspberry ? 'flipped' : ''}">
						<div class="flip-face flip-front">
							<img src="/flavours/raspberry.png" alt="Raspberry Stamp Pack" class="flavour-pack-img" />
						</div>
						<div class="flip-face flip-back">
							<img src="/flavours/raspberry-back.png" alt="Raspberry Nutritional Panel" class="flavour-pack-img" />
						</div>
					</div>
				</div>

				<!-- Animated Lift & Flip Button (Flat Solid Pill, No Outlines) -->
				<button
					type="button"
					class="flat-flip-trigger"
					class:is-flipped={flipped.raspberry}
					onclick={() => toggleFlip('raspberry')}
					aria-label="Lift and flip Raspberry card"
				>
					<span class="flip-icon-wrap" class:is-rotated={flipped.raspberry}>
						<svg class="flip-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
							<path d="M21 2v6h-6"></path>
							<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
							<path d="M3 22v-6h6"></path>
							<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
						</svg>
					</span>
					<span class="flip-btn-text">
						{flipped.raspberry ? 'Flip To Front Pack' : 'Lift & Flip: View Back Ingredients'}
					</span>
					<span class="flip-badge-pill">
						{flipped.raspberry ? 'BACK PANEL' : '3D LIFT'}
					</span>
				</button>
			</div>

			<div class="flavour-copy-side">
				<div class="flavour-index">02 / FOUR LAUNCH FLAVOURS</div>
				<h2 class="flavour-headline">SLOW-COOKED RASPBERRY</h2>
				<p class="flavour-lead">
					150 g of whole raspberries reduced down into every 100 g of thick, jewel-red spread. Brightened with fresh lemon juice and caster sugar.
				</p>

				<div class="flat-specs-grid">
					<div class="flat-spec-item">
						<span class="spec-kicker">FRUIT PROPORTION</span>
						<span class="spec-data">150 g fruit / 100 g spread</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">ALLERGENS</span>
						<span class="spec-data">No Major Recipe Allergens</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">PRESERVATION</span>
						<span class="spec-data">Natural Fruit Solids</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">PORTION</span>
						<span class="spec-data">10 g Discs · 8 per Sheet</span>
					</div>
				</div>

				<div class="flat-callout">
					Whole raspberries, caster sugar, and lemon juice. No artificial gelling agents and no unsupported organic claims.
				</div>
			</div>
		</div>
	</section>

	<!-- FLAVOUR 3: YEAST EXTRACT -->
	<section id="flavour-yeast" class="flavour-screen">
		<div class="flavour-content-grid">
			<div class="flavour-media-side">
				<!-- 3D Lift & Flip Card (Flat Solid Surfaces, No Outline Borders) -->
				<div class="flip-stage">
					<div class="flip-card {flipped.yeast ? 'flipped' : ''}">
						<div class="flip-face flip-front">
							<img src="/flavours/yeast.png" alt="Yeast Extract Stamp Pack" class="flavour-pack-img" />
						</div>
						<div class="flip-face flip-back">
							<img src="/flavours/yeast-back.png" alt="Yeast Extract Nutritional Panel" class="flavour-pack-img" />
						</div>
					</div>
				</div>

				<!-- Animated Lift & Flip Button (Flat Solid Pill, No Outlines) -->
				<button
					type="button"
					class="flat-flip-trigger"
					class:is-flipped={flipped.yeast}
					onclick={() => toggleFlip('yeast')}
					aria-label="Lift and flip Yeast Extract card"
				>
					<span class="flip-icon-wrap" class:is-rotated={flipped.yeast}>
						<svg class="flip-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
							<path d="M21 2v6h-6"></path>
							<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
							<path d="M3 22v-6h6"></path>
							<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
						</svg>
					</span>
					<span class="flip-btn-text">
						{flipped.yeast ? 'Flip To Front Pack' : 'Lift & Flip: View Back Ingredients'}
					</span>
					<span class="flip-badge-pill">
						{flipped.yeast ? 'BACK PANEL' : '3D LIFT'}
					</span>
				</button>
			</div>

			<div class="flavour-copy-side">
				<div class="flavour-index">03 / FOUR LAUNCH FLAVOURS</div>
				<h2 class="flavour-headline">YEAST EXTRACT</h2>
				<p class="flavour-lead">
					Deep, roasted umami paste crafted for toast loyalists. Formulated with 80% concentrated yeast extract and 15.5% barley malt extract for intense, sharp depth.
				</p>

				<div class="flat-specs-grid">
					<div class="flat-spec-item">
						<span class="spec-kicker">YEAST EXTRACT</span>
						<span class="spec-data">80% Concentrated</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">MALT EXTRACT</span>
						<span class="spec-data">15.5% Barley Malt</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">ALLERGEN</span>
						<span class="spec-data">CONTAINS GLUTEN (BARLEY)</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">PORTION</span>
						<span class="spec-data">10 g Discs · 8 per Sheet</span>
					</div>
				</div>

				<div class="flat-callout">
					NOT gluten-free. Contains barley malt extract. No therapeutic or medical treatment claims.
				</div>
			</div>
		</div>
	</section>

	<!-- FLAVOUR 4: ROASTED PEANUT -->
	<section id="flavour-peanut" class="flavour-screen">
		<div class="flavour-content-grid">
			<div class="flavour-media-side">
				<!-- 3D Lift & Flip Card (Flat Solid Surfaces, No Outline Borders) -->
				<div class="flip-stage">
					<div class="flip-card {flipped.peanut ? 'flipped' : ''}">
						<div class="flip-face flip-front">
							<img src="/flavours/peanut.png" alt="Roasted Peanut Stamp Pack" class="flavour-pack-img" />
						</div>
						<div class="flip-face flip-back">
							<img src="/flavours/peanut-back.png" alt="Roasted Peanut Nutritional Panel" class="flavour-pack-img" />
						</div>
					</div>
				</div>

				<!-- Animated Lift & Flip Button (Flat Solid Pill, No Outlines) -->
				<button
					type="button"
					class="flat-flip-trigger"
					class:is-flipped={flipped.peanut}
					onclick={() => toggleFlip('peanut')}
					aria-label="Lift and flip Roasted Peanut card"
				>
					<span class="flip-icon-wrap" class:is-rotated={flipped.peanut}>
						<svg class="flip-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
							<path d="M21 2v6h-6"></path>
							<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
							<path d="M3 22v-6h6"></path>
							<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
						</svg>
					</span>
					<span class="flip-btn-text">
						{flipped.peanut ? 'Flip To Front Pack' : 'Lift & Flip: View Back Ingredients'}
					</span>
					<span class="flip-badge-pill">
						{flipped.peanut ? 'BACK PANEL' : '3D LIFT'}
					</span>
				</button>
			</div>

			<div class="flavour-copy-side">
				<div class="flavour-index">04 / FOUR LAUNCH FLAVOURS</div>
				<h2 class="flavour-headline">ROASTED PEANUT</h2>
				<p class="flavour-lead">
					96% real roasted peanuts with a silky melt. Engineered with a 2.3% vegetable fat fraction so oil never pools or separates in your bag over 12 months.
				</p>

				<div class="flat-specs-grid">
					<div class="flat-spec-item">
						<span class="spec-kicker">PEANUT CONTENT</span>
						<span class="spec-data">96% Roasted Peanuts</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">STABILIZER</span>
						<span class="spec-data">2.3% Anti-Oil Fraction</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">ALLERGEN</span>
						<span class="spec-data">CONTAINS PEANUTS</span>
					</div>
					<div class="flat-spec-item">
						<span class="spec-kicker">PORTION</span>
						<span class="spec-data">10 g Discs · 8 per Sheet</span>
					</div>
				</div>

				<div class="flat-callout">
					96% peanuts, vegetable fat, and sea salt. Zero separated oil pooling; melts across toast instantly.
				</div>
			</div>
		</div>
	</section>
</div>

<!-- SECTION 7: THE MIXED SHEET & CATEGORY DISRUPTION (FLAT, ZERO OUTLINES) -->
<section id="mixed-section" class="mixed-pack-stage">
	<div class="mixed-content-container">
		<div class="mixed-media-col">
			<img src="/flavour-packs.png" alt="All 4 Stamp Flavour Packs" class="mixed-four-packs" />
		</div>

		<div class="mixed-copy-col">
			<div class="mixed-kicker">THE HERO COMBINATION</div>
			<h2 class="mixed-heading">THE MIXED SHEET</h2>
			<p class="mixed-lead">
				Two stamps of each flavour on one 8-stamp card sheet: Salted Butter, Raspberry, Yeast extract, and Roasted Peanut.
			</p>

			<div class="flat-price-card">
				<div class="price-giant">$5.00 NZD</div>
				<div class="price-explainer">
					<strong>$6.25 per 100 g</strong> · 80 g net weight<br />
					Pantry-stable portion convenience, avoiding messy jars and communal knives.
				</div>
			</div>

			<div class="mixed-btn-row">
				<a href="/flavours" class="flat-action-btn">View All Nutrition &amp; Specs →</a>
				<button
					type="button"
					class="flat-outline-btn"
					onclick={() => {
						if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent('stamp:open-chat'));
					}}
				>
					Ask Stamp Assistant
				</button>
			</div>
		</div>
	</div>
</section>

<style>
	/* ALL THEMED ELEMENTS REFER TO THE ONE COLORSCHEME VIA CSS VARIABLES */
	.hero-clean-stage,
	.steps-stage,
	.flavour-screen,
	.mixed-pack-stage,
	.hero-badge,
	.hero-btn-primary,
	.hero-btn-secondary,
	.step-card,
	.threshold-btn,
	.alert-box,
	.flip-face,
	.flat-flip-trigger,
	.flat-spec-item,
	.flat-callout,
	.flat-price-card,
	.flat-action-btn,
	.flat-outline-btn {
		transition: background-color 0.45s ease, color 0.45s ease;
	}

	/* SECTION 1: BALANCED, HIGH-IMPACT HERO */
	.hero-clean-stage {
		position: relative;
		min-height: 100vh;
		min-height: 100dvh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 7.5rem 1.5rem 4.5rem;
		background: transparent;
		text-align: center;
	}

	.hero-clean-inner {
		max-width: 840px;
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
	}

	.hero-wordmark-container {
		width: 100%;
		max-width: 580px;
		height: 130px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.hero-tagline {
		font-size: clamp(2rem, 5vw, 3.4rem);
		font-weight: 900;
		letter-spacing: 0.16em;
		color: var(--color-primary);
		margin: 0;
		line-height: 1.05;
	}

	.hero-lead {
		font-size: clamp(1.05rem, 2vw, 1.25rem);
		line-height: 1.6;
		color: #ffffff;
		max-width: 660px;
		margin: 0 auto;
		font-weight: 600;
		opacity: 0.95;
	}

	.hero-pack-showcase {
		margin: 0.4rem 0 0.2rem;
		display: flex;
		justify-content: center;
	}

	.hero-pack-wrap {
		position: relative;
		max-width: 290px;
		width: 100%;
	}

	.hero-pack-img {
		width: 100%;
		max-height: 230px;
		object-fit: contain;
		border-radius: 16px;
	}

	.hero-pack-pill {
		position: absolute;
		top: -8px;
		right: -8px;
		background: var(--color-primary);
		color: var(--color-tertiary);
		font-weight: 900;
		font-size: 0.75rem;
		letter-spacing: 0.08em;
		padding: 0.35rem 0.8rem;
		border-radius: 9999px;
		transform: rotate(5deg);
	}

	.hero-badges-row {
		display: flex;
		flex-wrap: wrap;
		gap: 0.65rem;
		justify-content: center;
	}

	.hero-badge {
		font-size: 0.82rem;
		font-weight: 800;
		letter-spacing: 0.05em;
		padding: 0.45rem 1.15rem;
		border-radius: 9999px;
		background: var(--color-tertiary);
		color: var(--color-primary);
	}

	.hero-actions-row {
		display: flex;
		gap: 1.25rem;
		flex-wrap: wrap;
		justify-content: center;
		margin-top: 0.75rem;
	}

	.hero-btn-primary {
		background: var(--color-primary);
		color: var(--color-tertiary);
		font-weight: 900;
		font-size: 1.1rem;
		padding: 1.1rem 2.4rem;
		border-radius: 9999px;
		text-decoration: none;
		letter-spacing: 0.03em;
		border: none;
		transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.45s, color 0.45s;
		display: inline-block;
	}

	.hero-btn-primary:hover {
		transform: translateY(-2px) scale(1.03);
	}

	.hero-btn-secondary {
		background: var(--color-tertiary);
		color: var(--color-primary);
		font-weight: 900;
		font-size: 1.1rem;
		padding: 1.1rem 2.4rem;
		border-radius: 9999px;
		text-decoration: none;
		letter-spacing: 0.03em;
		border: none;
		transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.45s, color 0.45s;
		display: inline-block;
	}

	.hero-btn-secondary:hover {
		transform: translateY(-2px) scale(1.03);
	}

	/* SECTION 2: THE 3 STEPS WITH THRESHOLD EXPLOSION (FLAT, ZERO OUTLINES) */
	.steps-stage {
		position: relative;
		min-height: 100vh;
		background: transparent;
		padding: 6rem 1.5rem 5rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.steps-inner {
		max-width: 1140px;
		width: 100%;
		text-align: center;
	}

	.section-kicker {
		color: var(--color-primary);
		font-size: 0.95rem;
		font-weight: 900;
		letter-spacing: 0.16em;
		margin-bottom: 0.5rem;
	}

	.section-title {
		font-size: clamp(2.4rem, 5.5vw, 4.2rem);
		font-weight: 900;
		color: var(--color-primary);
		letter-spacing: -0.03em;
		margin-bottom: 1rem;
	}

	.section-sub {
		max-width: 660px;
		margin: 0 auto 2.5rem;
		font-size: 1.1rem;
		color: #ffffff;
		opacity: 0.95;
		line-height: 1.5;
	}

	.threshold-control-bar {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 1rem;
		margin-bottom: 3.5rem;
		flex-wrap: wrap;
	}

	.threshold-btn {
		font-family: inherit;
		font-weight: 900;
		font-size: 0.95rem;
		padding: 0.7rem 1.6rem;
		border-radius: 9999px;
		cursor: pointer;
		border: none;
		background: var(--color-primary);
		color: var(--color-secondary);
		letter-spacing: 0.04em;
		transition: all 0.15s ease;
	}

	.threshold-btn:hover {
		transform: scale(1.05);
	}

	.threshold-status {
		font-size: 0.88rem;
		color: var(--color-primary);
		font-weight: 700;
		letter-spacing: 0.03em;
	}

	.steps-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 2rem;
		position: relative;
	}

	.step-card {
		border-radius: 20px;
		padding: 2.75rem 2rem;
		text-align: left;
		display: flex;
		flex-direction: column;
		border: none;
		min-height: 340px;
		position: relative;
		background: var(--color-tertiary);
		color: #ffffff;
		transition:
			transform 0.65s cubic-bezier(0.16, 1, 0.3, 1),
			opacity 0.65s ease,
			background-color 0.45s ease,
			color 0.45s ease;
	}

	/* Explosive Dispersal Transforms on Threshold */
	.step-card-1.blast-tl {
		transform: translate(-45px, -40px) rotate(-6deg);
	}

	.step-card-2.blast-down {
		transform: translate(0, 50px) scale(1.04);
	}

	.step-card-3.blast-tr {
		transform: translate(45px, -40px) rotate(6deg);
	}

	.step-badge {
		font-size: 3rem;
		font-weight: 900;
		line-height: 1;
		margin-bottom: 1.25rem;
		color: var(--color-primary);
	}

	.step-label {
		font-size: 2.2rem;
		font-weight: 900;
		letter-spacing: 0.02em;
		margin-bottom: 0.75rem;
		color: var(--color-primary);
	}

	.step-text {
		font-size: 1.05rem;
		line-height: 1.5;
		flex: 1;
		color: #ffffff;
		opacity: 0.95;
	}

	.flat-rule {
		height: 6px;
		width: 44px;
		border-radius: 999px;
		margin-top: 1.5rem;
		background: var(--color-primary);
	}

	.exploded-banner {
		margin-top: 3.5rem;
		display: flex;
		justify-content: center;
	}

	.alert-box {
		display: inline-flex;
		align-items: center;
		gap: 0.75rem;
		background: var(--color-primary);
		color: var(--color-secondary);
		padding: 0.7rem 1.6rem;
		border-radius: 9999px;
		font-weight: 900;
		font-size: 0.85rem;
		letter-spacing: 0.08em;
		border: none;
	}

	/* SECTIONS 3-6: IMMERSIVE FLAVOUR SCREENS (FLAT, ZERO OUTLINES) */
	.flavour-screen {
		position: relative;
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 6rem 2rem;
		background: transparent;
	}

	.flavour-content-grid {
		max-width: 1140px;
		width: 100%;
		display: grid;
		grid-template-columns: 460px 1fr;
		gap: 4.5rem;
		align-items: center;
	}

	.flavour-media-side {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
	}

	/* 3D LIFT & FLIP INTERACTIVE CARD (FLAT SOLID SURFACES, ZERO OUTLINES) */
	.flip-stage {
		width: 100%;
		max-width: 420px;
		height: 480px;
		perspective: 1200px;
	}

	.flip-card {
		width: 100%;
		height: 100%;
		position: relative;
		transform-style: preserve-3d;
		transition: transform 0.65s cubic-bezier(0.2, 0.9, 0.3, 1.2);
	}

	.flip-card.flipped {
		transform: translateY(-16px) scale(1.04) rotateY(180deg);
	}

	.flip-face {
		position: absolute;
		inset: 0;
		backface-visibility: hidden;
		-webkit-backface-visibility: hidden;
		border-radius: 20px;
		border: none;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
		padding: 1.5rem;
		background: var(--color-tertiary);
	}

	.flip-back {
		transform: rotateY(180deg);
	}

	.flavour-pack-img {
		max-height: 100%;
		max-width: 100%;
		object-fit: contain;
	}

	/* ANIMATED LIFT & FLIP BUTTON (FLAT SOLID PILL, ZERO OUTLINES) */
	.flat-flip-trigger {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 0.65rem;
		font-family: inherit;
		font-weight: 900;
		font-size: 0.9rem;
		padding: 0.8rem 1.7rem;
		border-radius: 9999px;
		cursor: pointer;
		border: none;
		background: var(--color-tertiary);
		color: var(--color-primary);
		letter-spacing: 0.03em;
		transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.45s, color 0.45s;
		animation: flipButtonPulse 3s ease-in-out infinite;
	}

	@keyframes flipButtonPulse {
		0%, 100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-3px);
		}
	}

	.flat-flip-trigger:hover {
		animation: none;
		transform: translateY(-4px) scale(1.03);
	}

	.flat-flip-trigger:active {
		transform: translateY(2px) scale(0.97);
	}

	.flip-icon-wrap {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	.flip-icon-wrap.is-rotated {
		transform: rotate(180deg);
	}

	.flat-flip-trigger:hover .flip-icon-wrap {
		transform: rotate(180deg);
	}
	.flat-flip-trigger.is-flipped:hover .flip-icon-wrap {
		transform: rotate(360deg);
	}

	.flip-svg {
		width: 18px;
		height: 18px;
	}

	.flip-badge-pill {
		font-size: 0.68rem;
		font-weight: 900;
		padding: 0.2rem 0.55rem;
		border-radius: 999px;
		background: currentColor;
		opacity: 0.22;
		letter-spacing: 0.05em;
	}

	.flavour-copy-side {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.flavour-index {
		font-size: 0.95rem;
		font-weight: 900;
		letter-spacing: 0.16em;
		color: var(--color-tertiary);
		opacity: 0.85;
	}

	.flavour-headline {
		font-size: clamp(2.8rem, 6vw, 5rem);
		font-weight: 900;
		line-height: 0.95;
		letter-spacing: -0.03em;
		margin: 0;
		color: var(--color-tertiary);
	}

	.flavour-lead {
		font-size: 1.2rem;
		line-height: 1.5;
		font-weight: 600;
		color: var(--color-tertiary);
		opacity: 0.92;
	}

	.flat-specs-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
	}

	.flat-spec-item {
		padding: 1.15rem 1.35rem;
		border-radius: 14px;
		border: none;
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
		background: var(--color-tertiary);
	}

	.spec-kicker {
		font-size: 0.72rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		opacity: 0.85;
		color: var(--color-primary);
	}

	.spec-data {
		font-size: 1.05rem;
		font-weight: 800;
		color: #ffffff;
	}

	.flat-callout {
		padding: 1.35rem 1.6rem;
		border-radius: 14px;
		border: none;
		font-size: 0.95rem;
		font-weight: 700;
		line-height: 1.5;
		background: var(--color-tertiary);
		color: var(--color-primary);
	}

	/* SECTION 7: MIXED SHEET (FLAT SOLID) */
	.mixed-pack-stage {
		background: transparent;
		padding: 6rem 2rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.mixed-content-container {
		max-width: 1140px;
		width: 100%;
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 4rem;
		align-items: center;
	}

	.mixed-four-packs {
		width: 100%;
		max-height: 460px;
		object-fit: contain;
		border-radius: 20px;
	}

	.mixed-copy-col {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.mixed-kicker {
		color: var(--color-primary);
		font-size: 0.95rem;
		font-weight: 900;
		letter-spacing: 0.16em;
	}

	.mixed-heading {
		font-size: clamp(2.6rem, 5vw, 4rem);
		font-weight: 900;
		line-height: 1;
		color: var(--color-primary);
		letter-spacing: -0.03em;
		margin: 0;
	}

	.mixed-lead {
		font-size: 1.2rem;
		color: #ffffff;
		opacity: 0.95;
		line-height: 1.5;
	}

	.flat-price-card {
		background: var(--color-tertiary);
		border-radius: 20px;
		padding: 2.25rem;
		display: flex;
		align-items: baseline;
		gap: 2rem;
		flex-wrap: wrap;
	}

	.price-giant {
		font-size: 3.2rem;
		font-weight: 900;
		color: var(--color-primary);
		letter-spacing: -0.02em;
	}

	.price-explainer {
		font-size: 1rem;
		color: #ffffff;
		opacity: 0.95;
		line-height: 1.5;
	}

	.price-explainer strong {
		color: var(--color-primary);
	}

	.mixed-btn-row {
		display: flex;
		gap: 1.25rem;
		flex-wrap: wrap;
	}

	.flat-action-btn {
		background: var(--color-primary);
		color: var(--color-secondary);
		font-weight: 900;
		font-size: 1.05rem;
		padding: 1rem 2.2rem;
		border-radius: 9999px;
		text-decoration: none;
		letter-spacing: 0.02em;
		transition: transform 0.15s;
		display: inline-block;
	}

	.flat-action-btn:hover {
		transform: scale(1.04);
	}

	.flat-outline-btn {
		font-family: inherit;
		background: var(--color-tertiary);
		color: var(--color-primary);
		font-weight: 900;
		font-size: 1.05rem;
		padding: 1rem 2.2rem;
		border-radius: 9999px;
		border: none;
		cursor: pointer;
		letter-spacing: 0.02em;
		transition: transform 0.15s;
	}

	.flat-outline-btn:hover {
		transform: scale(1.04);
	}

	/* RESPONSIVE */
	@media (max-width: 900px) {
		.hero-clean-stage {
			padding: 6.5rem 1rem 3.5rem;
		}
		.hero-wordmark-container {
			height: 90px;
		}
		.steps-grid {
			grid-template-columns: 1fr;
			gap: 1.5rem;
		}
		.step-card-1.blast-tl,
		.step-card-2.blast-down,
		.step-card-3.blast-tr {
			transform: none;
		}
		.flavour-content-grid {
			grid-template-columns: 1fr;
			gap: 2.5rem;
		}
		.flip-stage {
			height: 380px;
		}
		.mixed-content-container {
			grid-template-columns: 1fr;
			gap: 2.5rem;
		}
	}
</style>
