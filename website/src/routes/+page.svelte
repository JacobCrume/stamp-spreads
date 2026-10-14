<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import Wordmark from '../lib/Wordmark.svelte';
	import { setSectionTheme, type SectionTheme } from '../lib/theme.svelte';

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

	// Peel.js integration for Hero section
	let peelEl: HTMLElement | null = $state(null);
	let peelTrackEl: HTMLElement | null = $state(null);
	let peelInstance: any = null;
	let peelProgress = $state(0.04);
	let manualPeelOverride = $state(false);

	function toggleManualPeel() {
		manualPeelOverride = true;
		if (peelProgress < 0.5) {
			peelProgress = 1.0;
		} else {
			peelProgress = 0.04;
		}
		if (peelInstance) {
			peelInstance.setTimeAlongPath(peelProgress);
		}
	}

	onMount(async () => {
		// 1. Initialize Peel.js
		try {
			const { Peel, PeelCorners } = await import('peel.js');
			if (peelEl) {
				peelInstance = new Peel(peelEl, {
					corner: PeelCorners.BOTTOM_RIGHT,
					topShadow: false,
					backShadow: false,
					bottomShadow: false,
					backReflection: false,
					fadeThreshold: 0.96
				});

				const updatePeelDimensions = () => {
					if (!peelEl || !peelInstance) return;
					const w = peelEl.offsetWidth || window.innerWidth;
					const h = peelEl.offsetHeight || window.innerHeight;
					// Diagonal peel path from bottom-right (w, h) to past top-left (-w*0.35, -h*0.35)
					peelInstance.setPeelPath(w, h, -w * 0.35, -h * 0.35);
					peelInstance.setTimeAlongPath(peelProgress);
				};

				updatePeelDimensions();

				// Enable mouse & touch drag on peel sheet
				peelInstance.handle('drag', (_evt: any, x: number, y: number) => {
					manualPeelOverride = true;
					peelInstance.setPeelPosition(x, y);
				});

				window.addEventListener('resize', updatePeelDimensions);
			}
		} catch (err) {
			console.error('Peel.js setup notice:', err);
		}

		// 2. Active section observer to fade stationary background smoothly between brand colors
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
			// clean up any listeners if needed
		}
	});

	// Peel along path with scroll progress
	$effect(() => {
		if (!peelInstance || manualPeelOverride) return;
		if (peelTrackEl) {
			const rect = peelTrackEl.getBoundingClientRect();
			const scrollDistance = rect.height - innerHeight;
			if (scrollDistance > 0) {
				const progress = Math.max(0, Math.min(1, -rect.top / scrollDistance));
				// Map scrollProgress: 0 -> 0.04 (starter tease), 1.0 -> 1.0 (fully peeled open)
				peelProgress = 0.04 + progress * 0.96;
				peelInstance.setTimeAlongPath(peelProgress);
			}
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

<!-- SECTION 1: FULL-SCREEN HERO WITH PEEL.JS INTERACTION -->
<section id="hero-section" class="hero-peel-track" bind:this={peelTrackEl}>
	<div class="hero-peel-sticky">
		<div class="peel hero-peel-box" bind:this={peelEl}>
			<!-- BOTTOM LAYER: Underneath surface revealed when peeled -->
			<div class="peel-bottom hero-peel-bottom">
				<div class="hero-bottom-content">
					<div class="under-eyebrow">REVEALED BENEATH THE FOIL</div>
					<h2 class="under-headline">HOT SOURDOUGH + 10 g STAMP DISC</h2>
					<p class="under-note">
						No knives. No sticky butter dishes. No messy jars. 
						Peel the seal, press the solid disc onto hot toast, and watch it melt evenly in 3 seconds.
					</p>
					<div class="under-spec-badges">
						<span class="under-badge">MELT THRESHOLD: 32°C - 38°C</span>
						<span class="under-badge">8 DISCS PER SHEET</span>
						<span class="under-badge">100% RECYCLABLE FILM</span>
					</div>
					<div class="under-actions">
						<a href="#steps-section" class="flat-btn-ghost">View The 3-Step Gesture ↓</a>
						<button type="button" class="flat-btn-reset-peel" onclick={toggleManualPeel}>
							{peelProgress > 0.5 ? '↩ Re-Seal Disc' : 'Peel Open Stamp ↗'}
						</button>
					</div>
				</div>
			</div>

			<!-- BACK LAYER: Underside of the peeled foil sheet that curls over -->
			<div class="peel-back hero-peel-back">
				<div class="foil-pattern">
					<div class="foil-stamp-text">STAMP • 10G SPREAD DISC • NZ FOODTECH INNOVATION • PEEL &amp; PRESS • </div>
					<div class="foil-stamp-text">STAMP • 10G SPREAD DISC • NZ FOODTECH INNOVATION • PEEL &amp; PRESS • </div>
					<div class="foil-stamp-text">STAMP • 10G SPREAD DISC • NZ FOODTECH INNOVATION • PEEL &amp; PRESS • </div>
					<div class="foil-stamp-text">STAMP • 10G SPREAD DISC • NZ FOODTECH INNOVATION • PEEL &amp; PRESS • </div>
				</div>
			</div>

			<!-- TOP LAYER: Front hero cover sheet -->
			<div class="peel-top hero-peel-top">
				<div class="hero-top-kicker">NEW ZEALAND BREAKFAST INNOVATION</div>

				<!-- Actual Drawn STAMP Vector Wordmark -->
				<div class="hero-wordmark-container">
					<Wordmark color="#e24bff" />
				</div>

				<p class="hero-tagline">PEEL. PRESS. TOAST.</p>

				<div class="hero-pack-box">
					<img src="/pack.png" alt="STAMP 8-Stamp Sheet" class="hero-flat-pack" />
					<div class="flat-peel-tag">PEEL ME</div>
				</div>

				<div class="hero-meta-row">
					<span class="meta-tag">$5.00 NZD / SHEET</span>
					<span class="meta-tag">8 × 10 g DISCS</span>
					<span class="meta-tag">PANTRY STABLE 12 MO.</span>
				</div>

				<!-- Animated corner peel indicator with click-to-peel toggle -->
				<button type="button" class="hero-peel-indicator" onclick={toggleManualPeel}>
					<span class="peel-arrow">↘</span>
					<span class="peel-label">SCROLL OR CLICK CORNER TO PEEL</span>
				</button>
			</div>
		</div>
	</div>
</section>

<!-- SECTION 2: THE 3 STEPS WITH THRESHOLD EXPLOSION -->
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
				class="threshold-btn {isExploded ? 'active' : ''}"
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

<!-- SECTIONS 3-6: DEDICATED FULL-SCREEN IMMERSIVE FLAVOUR WORLDS -->
<div id="flavours" class="flavour-worlds-list">
	<!-- FLAVOUR 1: SALTED BUTTER (ELECTRIC GOLD & ROASTED CARAMEL) -->
	<section id="flavour-butter" class="flavour-screen butter-screen">
		<div class="flavour-content-grid">
			<div class="flavour-media-side">
				<!-- 3D Lift & Flip Card -->
				<div class="flip-stage">
					<div class="flip-card {flipped.butter ? 'flipped' : ''}">
						<div class="flip-face flip-front butter-face">
							<img src="/flavours/butter.png" alt="Salted Butter Stamp Pack" class="flavour-pack-img" />
						</div>
						<div class="flip-face flip-back butter-face">
							<img src="/flavours/butter-back.png" alt="Salted Butter Nutritional Panel" class="flavour-pack-img" />
						</div>
					</div>
				</div>

				<!-- Animated Lift & Flip Button -->
				<button
					type="button"
					class="flat-flip-trigger butter-btn"
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
					<div class="flat-spec-item butter-spec">
						<span class="spec-kicker">FORMULA</span>
						<span class="spec-data">78 g butterfat · 2 g salt</span>
					</div>
					<div class="flat-spec-item butter-spec">
						<span class="spec-kicker">ALLERGEN</span>
						<span class="spec-data">CONTAINS MILK</span>
					</div>
					<div class="flat-spec-item butter-spec">
						<span class="spec-kicker">STABILITY</span>
						<span class="spec-data">12 Months Ambient</span>
					</div>
					<div class="flat-spec-item butter-spec">
						<span class="spec-kicker">PORTION</span>
						<span class="spec-data">10 g Discs · 8 per Sheet</span>
					</div>
				</div>

				<div class="flat-callout butter-callout">
					Sold as a shelf-stable butter spread, not a pat of fridge butter. Zero added vegetable oils or artificial preservatives.
				</div>
			</div>
		</div>
	</section>

	<!-- FLAVOUR 2: RASPBERRY (VIBRANT NEON RASPBERRY & DARK WILD BERRY) -->
	<section id="flavour-raspberry" class="flavour-screen raspberry-screen">
		<div class="flavour-content-grid">
			<div class="flavour-media-side">
				<!-- 3D Lift & Flip Card -->
				<div class="flip-stage">
					<div class="flip-card {flipped.raspberry ? 'flipped' : ''}">
						<div class="flip-face flip-front raspberry-face">
							<img src="/flavours/raspberry.png" alt="Raspberry Stamp Pack" class="flavour-pack-img" />
						</div>
						<div class="flip-face flip-back raspberry-face">
							<img src="/flavours/raspberry-back.png" alt="Raspberry Nutritional Panel" class="flavour-pack-img" />
						</div>
					</div>
				</div>

				<!-- Animated Lift & Flip Button -->
				<button
					type="button"
					class="flat-flip-trigger raspberry-btn"
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
					<div class="flat-spec-item raspberry-spec">
						<span class="spec-kicker">FRUIT PROPORTION</span>
						<span class="spec-data">150 g fruit / 100 g spread</span>
					</div>
					<div class="flat-spec-item raspberry-spec">
						<span class="spec-kicker">ALLERGENS</span>
						<span class="spec-data">No Major Recipe Allergens</span>
					</div>
					<div class="flat-spec-item raspberry-spec">
						<span class="spec-kicker">PRESERVATION</span>
						<span class="spec-data">Natural Fruit Solids</span>
					</div>
					<div class="flat-spec-item raspberry-spec">
						<span class="spec-kicker">PORTION</span>
						<span class="spec-data">10 g Discs · 8 per Sheet</span>
					</div>
				</div>

				<div class="flat-callout raspberry-callout">
					Whole raspberries, caster sugar, and lemon juice. No artificial gelling agents and no unsupported organic claims.
				</div>
			</div>
		</div>
	</section>

	<!-- FLAVOUR 3: YEAST EXTRACT (ELECTRIC VIOLET & DEEP INK PURPLE) -->
	<section id="flavour-yeast" class="flavour-screen yeast-screen">
		<div class="flavour-content-grid">
			<div class="flavour-media-side">
				<!-- 3D Lift & Flip Card -->
				<div class="flip-stage">
					<div class="flip-card {flipped.yeast ? 'flipped' : ''}">
						<div class="flip-face flip-front yeast-face">
							<img src="/flavours/yeast.png" alt="Yeast Extract Stamp Pack" class="flavour-pack-img" />
						</div>
						<div class="flip-face flip-back yeast-face">
							<img src="/flavours/yeast-back.png" alt="Yeast Extract Nutritional Panel" class="flavour-pack-img" />
						</div>
					</div>
				</div>

				<!-- Animated Lift & Flip Button -->
				<button
					type="button"
					class="flat-flip-trigger yeast-btn"
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
					<div class="flat-spec-item yeast-spec">
						<span class="spec-kicker">YEAST EXTRACT</span>
						<span class="spec-data">80% Concentrated</span>
					</div>
					<div class="flat-spec-item yeast-spec">
						<span class="spec-kicker">MALT EXTRACT</span>
						<span class="spec-data">15.5% Barley Malt</span>
					</div>
					<div class="flat-spec-item yeast-spec">
						<span class="spec-kicker">ALLERGEN</span>
						<span class="spec-data">CONTAINS GLUTEN (BARLEY)</span>
					</div>
					<div class="flat-spec-item yeast-spec">
						<span class="spec-kicker">PORTION</span>
						<span class="spec-data">10 g Discs · 8 per Sheet</span>
					</div>
				</div>

				<div class="flat-callout yeast-callout">
					NOT gluten-free. Contains barley malt extract. No therapeutic or medical treatment claims.
				</div>
			</div>
		</div>
	</section>

	<!-- FLAVOUR 4: ROASTED PEANUT (WARM OCHRE ORANGE & ROASTED UMBER) -->
	<section id="flavour-peanut" class="flavour-screen peanut-screen">
		<div class="flavour-content-grid">
			<div class="flavour-media-side">
				<!-- 3D Lift & Flip Card -->
				<div class="flip-stage">
					<div class="flip-card {flipped.peanut ? 'flipped' : ''}">
						<div class="flip-face flip-front peanut-face">
							<img src="/flavours/peanut.png" alt="Roasted Peanut Stamp Pack" class="flavour-pack-img" />
						</div>
						<div class="flip-face flip-back peanut-face">
							<img src="/flavours/peanut-back.png" alt="Roasted Peanut Nutritional Panel" class="flavour-pack-img" />
						</div>
					</div>
				</div>

				<!-- Animated Lift & Flip Button -->
				<button
					type="button"
					class="flat-flip-trigger peanut-btn"
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
					<div class="flat-spec-item peanut-spec">
						<span class="spec-kicker">PEANUT CONTENT</span>
						<span class="spec-data">96% Roasted Peanuts</span>
					</div>
					<div class="flat-spec-item peanut-spec">
						<span class="spec-kicker">STABILIZER</span>
						<span class="spec-data">2.3% Anti-Oil Fraction</span>
					</div>
					<div class="flat-spec-item peanut-spec">
						<span class="spec-kicker">ALLERGEN</span>
						<span class="spec-data">CONTAINS PEANUTS</span>
					</div>
					<div class="flat-spec-item peanut-spec">
						<span class="spec-kicker">PORTION</span>
						<span class="spec-data">10 g Discs · 8 per Sheet</span>
					</div>
				</div>

				<div class="flat-callout peanut-callout">
					96% peanuts, vegetable fat, and sea salt. Zero separated oil pooling; melts across toast instantly.
				</div>
			</div>
		</div>
	</section>
</div>

<!-- SECTION 7: THE MIXED SHEET & CATEGORY DISRUPTION -->
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
	/* PEEL.JS SYSTEM CONTAINER & LAYERS */
	.peel {
		position: relative;
		opacity: 0;
	}
	:global(.peel-ready) {
		opacity: 1 !important;
	}
	:global(.peel-svg-clip-element) {
		position: absolute;
		top: -10000px;
		left: -10000px;
		width: 1px;
		height: 1px;
		opacity: 0;
		pointer-events: none;
	}
	:global(.peel-layer) {
		position: absolute;
		z-index: 1;
		width: 100%;
		height: 100%;
		top: 0;
		right: 0;
		bottom: 0;
		left: 0;
		user-select: none;
		transform-origin: top left;
	}

	/* SECTION 1: HERO PEEL TRACK (STATIONARY VIEWPORT CANVAS) */
	.hero-peel-track {
		position: relative;
		height: 190vh; /* provides scroll length for peel */
		background: transparent;
	}

	.hero-peel-sticky {
		position: sticky;
		top: 0;
		height: 100vh;
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
		padding: 76px 1.5rem 1.5rem;
	}

	.hero-peel-box {
		width: 100%;
		max-width: 1140px;
		height: calc(100vh - 100px);
		max-height: 860px;
		border-radius: 20px;
		border: 3px solid #e24bff;
		background: #240340;
		overflow: hidden;
	}

	/* BOTTOM LAYER (UNDER PEEL): HOT SOURDOUGH & GESTURE REVEAL */
	.hero-peel-bottom {
		background: #240340;
		border-radius: 17px;
		padding: 3rem 2.5rem;
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
	}

	.hero-bottom-content {
		max-width: 680px;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
	}

	.under-eyebrow {
		color: #e24bff;
		font-weight: 800;
		letter-spacing: 0.16em;
		font-size: 0.95rem;
	}

	.under-headline {
		color: #e24bff;
		font-size: clamp(2.2rem, 5vw, 3.8rem);
		font-weight: 900;
		letter-spacing: -0.02em;
		line-height: 1.05;
		margin: 0;
	}

	.under-note {
		color: #f4c7ff;
		font-size: 1.15rem;
		line-height: 1.55;
	}

	.under-spec-badges {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
		justify-content: center;
	}

	.under-badge {
		font-size: 0.8rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		padding: 0.45rem 1rem;
		border-radius: 9999px;
		border: 2px solid #e24bff;
		color: #e24bff;
		background: #3b0764;
	}

	.under-actions {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
		justify-content: center;
		margin-top: 0.5rem;
	}

	.flat-btn-ghost {
		font-size: 1rem;
		font-weight: 900;
		padding: 0.85rem 1.8rem;
		border-radius: 9999px;
		text-decoration: none;
		border: 2px solid #e24bff;
		color: #240340;
		background: #e24bff;
		letter-spacing: 0.02em;
		transition: transform 0.15s;
	}

	.flat-btn-ghost:hover {
		transform: scale(1.04);
	}

	.flat-btn-reset-peel {
		font-family: inherit;
		font-size: 1rem;
		font-weight: 900;
		padding: 0.85rem 1.8rem;
		border-radius: 9999px;
		border: 2px solid #ffd640;
		color: #4a3000;
		background: #ffd640;
		cursor: pointer;
		letter-spacing: 0.02em;
		transition: transform 0.15s;
	}

	.flat-btn-reset-peel:hover {
		transform: scale(1.04);
	}

	/* BACK LAYER: UNDERSIDE OF FOIL SHEET */
	.hero-peel-back {
		background: #e24bff;
		border: 3px solid #ffd640;
		border-radius: 17px;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}

	.foil-pattern {
		transform: rotate(-35deg);
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		opacity: 0.45;
		user-select: none;
		pointer-events: none;
	}

	.foil-stamp-text {
		font-size: 1.6rem;
		font-weight: 900;
		letter-spacing: 0.12em;
		white-space: nowrap;
		color: #3b0764;
	}

	/* TOP LAYER: FRONT HERO COVER */
	.hero-peel-top {
		background: #240340;
		border-radius: 17px;
		padding: 2.2rem 2rem 1.75rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
		text-align: center;
		cursor: grab;
	}

	.hero-peel-top:active {
		cursor: grabbing;
	}

	.hero-top-kicker {
		font-size: 0.85rem;
		font-weight: 900;
		letter-spacing: 0.18em;
		color: #e24bff;
	}

	.hero-wordmark-container {
		width: 100%;
		max-width: 480px;
		height: 95px;
		display: flex;
		align-items: center;
		justify-content: center;
		margin: 0.25rem 0;
	}

	.hero-tagline {
		font-size: clamp(1.2rem, 3vw, 1.85rem);
		font-weight: 900;
		letter-spacing: 0.22em;
		color: #f4c7ff;
		margin-bottom: 0.5rem;
	}

	.hero-pack-box {
		position: relative;
		width: 100%;
		max-width: 320px;
		margin: 0 auto;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.hero-flat-pack {
		width: 100%;
		max-height: 250px;
		object-fit: contain;
		border-radius: 14px;
		border: 3px solid #e24bff;
	}

	.flat-peel-tag {
		position: absolute;
		top: -12px;
		right: -12px;
		background: #ffd640;
		color: #4a3000;
		font-weight: 900;
		font-size: 0.75rem;
		letter-spacing: 0.08em;
		padding: 0.35rem 0.75rem;
		border-radius: 9999px;
		border: 2px solid #4a3000;
		transform: rotate(8deg);
	}

	.hero-meta-row {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
		justify-content: center;
		margin: 0.5rem 0;
	}

	.meta-tag {
		font-size: 0.8rem;
		font-weight: 800;
		letter-spacing: 0.05em;
		padding: 0.35rem 0.85rem;
		border-radius: 9999px;
		background: #3b0764;
		border: 2px solid #e24bff;
		color: #e24bff;
	}

	.hero-peel-indicator {
		display: inline-flex;
		align-items: center;
		gap: 0.6rem;
		background: #3b0764;
		border: 2px solid #ffd640;
		color: #ffd640;
		padding: 0.45rem 1.1rem;
		border-radius: 9999px;
		font-family: inherit;
		font-size: 0.82rem;
		font-weight: 900;
		cursor: pointer;
		letter-spacing: 0.05em;
		transition: transform 0.15s, background-color 0.15s;
		animation: peelIndicatorWiggle 2.5s infinite ease-in-out;
	}

	@keyframes peelIndicatorWiggle {
		0%, 100% {
			transform: translateX(0);
		}
		50% {
			transform: translateX(4px);
		}
	}

	.hero-peel-indicator:hover {
		transform: scale(1.05);
		background: #4a3000;
	}

	.peel-arrow {
		font-size: 1.1rem;
		color: #ffd640;
	}

	/* SECTION 2: THE 3 STEPS WITH THRESHOLD EXPLOSION */
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
		color: #e24bff;
		font-size: 0.95rem;
		font-weight: 800;
		letter-spacing: 0.16em;
		margin-bottom: 0.5rem;
	}

	.section-title {
		font-size: clamp(2.4rem, 5.5vw, 4.2rem);
		font-weight: 900;
		color: #e24bff;
		letter-spacing: -0.03em;
		margin-bottom: 1rem;
	}

	.section-sub {
		max-width: 660px;
		margin: 0 auto 2.5rem;
		font-size: 1.1rem;
		color: #f4c7ff;
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
		padding: 0.65rem 1.5rem;
		border-radius: 9999px;
		cursor: pointer;
		border: 2px solid #e24bff;
		background: #e24bff;
		color: #240340;
		letter-spacing: 0.04em;
		transition: all 0.15s ease;
	}

	.threshold-btn:hover {
		transform: scale(1.05);
	}

	.threshold-btn.active {
		background: #ffd640;
		border-color: #ffd640;
		color: #4a3000;
	}

	.threshold-status {
		font-size: 0.88rem;
		color: #f4c7ff;
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
		border-radius: 18px;
		padding: 2.75rem 2rem;
		text-align: left;
		display: flex;
		flex-direction: column;
		border: 3px solid;
		min-height: 340px;
		position: relative;
		transition:
			transform 0.65s cubic-bezier(0.16, 1, 0.3, 1),
			opacity 0.65s ease;
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

	.step-card-1 {
		background: #3b0764;
		border-color: #e24bff;
		color: #f4c7ff;
	}

	.step-card-2 {
		background: #4a3000;
		border-color: #ffd640;
		color: #ffeaa0;
	}

	.step-card-3 {
		background: #460820;
		border-color: #ff467a;
		color: #ffc0d2;
	}

	.step-badge {
		font-size: 3rem;
		font-weight: 900;
		line-height: 1;
		margin-bottom: 1.25rem;
	}

	.step-card-1 .step-badge {
		color: #e24bff;
	}
	.step-card-2 .step-badge {
		color: #ffd640;
	}
	.step-card-3 .step-badge {
		color: #ff467a;
	}

	.step-label {
		font-size: 2.2rem;
		font-weight: 900;
		letter-spacing: 0.02em;
		margin-bottom: 0.75rem;
	}

	.step-card-1 .step-label {
		color: #e24bff;
	}
	.step-card-2 .step-label {
		color: #ffd640;
	}
	.step-card-3 .step-label {
		color: #ff467a;
	}

	.step-text {
		font-size: 1.05rem;
		line-height: 1.5;
		flex: 1;
	}

	.flat-rule {
		height: 6px;
		width: 44px;
		border-radius: 999px;
		margin-top: 1.5rem;
	}

	.step-card-1 .flat-rule {
		background: #e24bff;
	}
	.step-card-2 .flat-rule {
		background: #ffd640;
	}
	.step-card-3 .flat-rule {
		background: #ff467a;
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
		background: #ffd640;
		color: #4a3000;
		padding: 0.65rem 1.4rem;
		border-radius: 9999px;
		font-weight: 900;
		font-size: 0.85rem;
		letter-spacing: 0.08em;
		border: 2px solid #4a3000;
	}

	/* SECTIONS 3-6: IMMERSIVE FLAVOUR SCREENS */
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

	/* 3D LIFT & FLIP INTERACTIVE CARD */
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
		border-radius: 16px;
		border: 3px solid;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
		padding: 1rem;
	}

	.flip-back {
		transform: rotateY(180deg);
	}

	.flavour-pack-img {
		max-height: 100%;
		max-width: 100%;
		object-fit: contain;
	}

	/* ANIMATED LIFT & FLIP BUTTON */
	.flat-flip-trigger {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 0.65rem;
		font-family: inherit;
		font-weight: 900;
		font-size: 0.88rem;
		padding: 0.75rem 1.6rem;
		border-radius: 9999px;
		cursor: pointer;
		border: 2px solid;
		letter-spacing: 0.03em;
		transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.2s, color 0.2s;
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
	}

	.flavour-headline {
		font-size: clamp(2.8rem, 6vw, 5rem);
		font-weight: 900;
		line-height: 0.95;
		letter-spacing: -0.03em;
		margin: 0;
	}

	.flavour-lead {
		font-size: 1.2rem;
		line-height: 1.5;
		font-weight: 600;
	}

	.flat-specs-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
	}

	.flat-spec-item {
		padding: 1rem 1.25rem;
		border-radius: 12px;
		border: 2px solid;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.spec-kicker {
		font-size: 0.72rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		opacity: 0.85;
		color: inherit;
	}

	.spec-data {
		font-size: 1.05rem;
		font-weight: 800;
		color: inherit;
	}

	.flat-callout {
		padding: 1.25rem 1.5rem;
		border-radius: 12px;
		font-size: 0.95rem;
		font-weight: 700;
		line-height: 1.5;
	}

	/* BUTTER THEME (FLAT) */
	.butter-screen {
		color: #4a3000;
	}
	.butter-face {
		background: #4a3000;
		border-color: #4a3000;
	}
	.butter-btn {
		background: #4a3000;
		color: #ffd640;
		border-color: #4a3000;
	}
	.butter-spec {
		background: #e8c028;
		border-color: #4a3000;
		color: #4a3000;
	}
	.butter-callout {
		background: #f7ca22;
		color: #4a3000;
		border-left: 4px solid #4a3000;
	}

	/* RASPBERRY THEME (FLAT - ZERO WHITE) */
	.raspberry-screen {
		color: #460820;
	}
	.raspberry-face {
		background: #460820;
		border-color: #460820;
	}
	.raspberry-btn {
		background: #460820;
		color: #ff467a;
		border-color: #460820;
	}
	.raspberry-spec {
		background: #e83366;
		border-color: #460820;
		color: #460820;
	}
	.raspberry-callout {
		background: #e83366;
		color: #460820;
		border-left: 4px solid #460820;
	}

	/* YEAST THEME (FLAT - ZERO WHITE) */
	.yeast-screen {
		color: #3b0764;
	}
	.yeast-face {
		background: #3b0764;
		border-color: #3b0764;
	}
	.yeast-btn {
		background: #3b0764;
		color: #e24bff;
		border-color: #3b0764;
	}
	.yeast-spec {
		background: #cb32e8;
		border-color: #3b0764;
		color: #3b0764;
	}
	.yeast-callout {
		background: #cb32e8;
		color: #3b0764;
		border-left: 4px solid #3b0764;
	}

	/* PEANUT THEME (FLAT - ZERO WHITE) */
	.peanut-screen {
		color: #4e2408;
	}
	.peanut-face {
		background: #4e2408;
		border-color: #4e2408;
	}
	.peanut-btn {
		background: #4e2408;
		color: #ff8c30;
		border-color: #4e2408;
	}
	.peanut-spec {
		background: #e87820;
		border-color: #4e2408;
		color: #4e2408;
	}
	.peanut-callout {
		background: #e87820;
		color: #4e2408;
		border-left: 4px solid #4e2408;
	}

	/* SECTION 7: MIXED SHEET */
	.mixed-pack-stage {
		background: transparent;
		border-top: 4px solid #e24bff;
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
		border-radius: 16px;
		border: 3px solid #e24bff;
	}

	.mixed-copy-col {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.mixed-kicker {
		color: #e24bff;
		font-size: 0.95rem;
		font-weight: 900;
		letter-spacing: 0.16em;
	}

	.mixed-heading {
		font-size: clamp(2.6rem, 5vw, 4rem);
		font-weight: 900;
		line-height: 1;
		color: #e24bff;
		letter-spacing: -0.03em;
		margin: 0;
	}

	.mixed-lead {
		font-size: 1.2rem;
		color: #f4c7ff;
		line-height: 1.5;
	}

	.flat-price-card {
		background: #3b0764;
		border: 3px solid #e24bff;
		border-radius: 16px;
		padding: 2rem;
		display: flex;
		align-items: baseline;
		gap: 2rem;
		flex-wrap: wrap;
	}

	.price-giant {
		font-size: 3.2rem;
		font-weight: 900;
		color: #ffd640;
		letter-spacing: -0.02em;
	}

	.price-explainer {
		font-size: 1rem;
		color: #f4c7ff;
		line-height: 1.5;
	}

	.price-explainer strong {
		color: #ffd640;
	}

	.mixed-btn-row {
		display: flex;
		gap: 1.25rem;
		flex-wrap: wrap;
	}

	.flat-action-btn {
		background: #e24bff;
		color: #240340;
		font-weight: 900;
		font-size: 1.05rem;
		padding: 0.95rem 2rem;
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
		background: transparent;
		color: #e24bff;
		font-weight: 800;
		font-size: 1.05rem;
		padding: 0.95rem 2rem;
		border-radius: 9999px;
		border: 2px solid #e24bff;
		cursor: pointer;
		letter-spacing: 0.02em;
		transition: transform 0.15s;
	}

	.flat-outline-btn:hover {
		transform: scale(1.04);
	}

	/* RESPONSIVE */
	@media (max-width: 900px) {
		.hero-peel-sticky {
			padding: 70px 1rem 1rem;
		}
		.hero-peel-box {
			height: calc(100vh - 80px);
		}
		.hero-peel-top {
			padding: 1.75rem 1.25rem;
		}
		.hero-wordmark-container {
			height: 70px;
		}
		.hero-flat-pack {
			max-height: 180px;
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
