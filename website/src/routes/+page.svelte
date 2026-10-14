<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import Wordmark from '../lib/Wordmark.svelte';
	import { setSectionTheme, type SectionTheme } from '../lib/theme.svelte';

	let scrollY = $state(0);
	let innerHeight = $state(800);

	// Page-flip animation for Hero: like turning a page in an e-reader (spined on left)
	// Rotates from 0deg up to -88deg over the first 500px of scroll
	let flipDegrees = $derived(Math.min(88, Math.max(0, (scrollY / 450) * 88)));

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

	let observer: IntersectionObserver | null = null;

	onMount(() => {
		// IntersectionObserver to dynamically switch header color theme based on the section below it
		const sections = [
			{ id: 'hero-section', theme: 'hero' as SectionTheme },
			{ id: 'steps-section', theme: 'steps' as SectionTheme },
			{ id: 'flavour-butter', theme: 'butter' as SectionTheme },
			{ id: 'flavour-raspberry', theme: 'raspberry' as SectionTheme },
			{ id: 'flavour-yeast', theme: 'yeast' as SectionTheme },
			{ id: 'flavour-peanut', theme: 'peanut' as SectionTheme },
			{ id: 'mixed-section', theme: 'mixed' as SectionTheme }
		];

		observer = new IntersectionObserver(
			(entries) => {
				for (const entry of entries) {
					if (entry.isIntersecting) {
						const match = sections.find((s) => s.id === entry.target.id);
						if (match) {
							setSectionTheme(match.theme);
						}
					}
				}
			},
			{
				rootMargin: '-80px 0px -60% 0px',
				threshold: 0.1
			}
		);

		for (const sec of sections) {
			const el = document.getElementById(sec.id);
			if (el) observer.observe(el);
		}
	});

	onDestroy(() => {
		if (observer) observer.disconnect();
	});

	// Trigger explosion on threshold (when scrollY crosses the middle of the steps section)
	$effect(() => {
		// Threshold: approx 1.1x viewport height
		if (scrollY > innerHeight * 0.95 && !isExploded) {
			isExploded = true;
		} else if (scrollY < innerHeight * 0.5 && isExploded) {
			isExploded = false;
		}
	});
</script>

<svelte:window bind:scrollY bind:innerHeight />

<svelte:head>
	<title>STAMP — Peel. Press. Toast.</title>
	<meta
		name="description"
		content="Stamp: Single-serve peel-and-press spread discs for toast. Bold flat breakfast innovation with no knife and no open jar."
	/>
</svelte:head>

<!-- SECTION 1: FULL-SCREEN HERO WITH E-READER PAGE FLIP ANIMATION -->
<section id="hero-section" class="hero-stage">
	<!-- Underlying reveal surface visible as page flips -->
	<div class="hero-under-book">
		<div class="under-spine"></div>
		<div class="under-content">
			<div class="under-eyebrow">NEXT SECTION READY</div>
			<div class="under-headline">THE 3-SECOND GESTURE</div>
			<p class="under-note">
				Peel one 10 g disc. Press onto steaming toast. No knife, no open jar.
			</p>
			<a href="#steps-section" class="flat-btn-ghost">View The 3 Steps ↓</a>
		</div>
	</div>

	<!-- Page sheet that flips open from right to left like an e-reader page -->
	<div
		class="ereader-page"
		style:transform="perspective(2400px) rotateY(-{flipDegrees}deg)"
		style:opacity={flipDegrees > 82 ? Math.max(0, (88 - flipDegrees) / 6) : 1}
	>
		<div class="ereader-page-inner">
			<div class="hero-top-kicker">NEW ZEALAND BREAKFAST INNOVATION</div>

			<!-- Actual Drawn STAMP Vector Wordmark (Toundra construction) -->
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

			<div class="page-flip-indicator" style:opacity={1 - flipDegrees / 50}>
				<span class="flip-icon">📖</span>
				<span class="flip-text">SCROLL TO TURN PAGE</span>
			</div>
		</div>

		<!-- Page edge binding shadow-free border -->
		<div class="page-edge-binding"></div>
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
					Press the portion directly onto hot, steaming bread. The disc adheres immediately.
				</p>
				<div class="flat-rule"></div>
			</div>

			<!-- Step 3: Explodes Top-Right on threshold -->
			<div class="step-card step-card-3 {isExploded ? 'blast-tr' : ''}">
				<div class="step-badge">03</div>
				<h3 class="step-label">TOAST</h3>
				<p class="step-text">
					Residual toast heat softens it into an even spread in seconds without tearing bread crumb.
				</p>
				<div class="flat-rule"></div>
			</div>
		</div>

		{#if isExploded}
			<div class="explosion-alert">
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

				<button
					type="button"
					class="flat-flip-trigger butter-btn"
					onclick={() => toggleFlip('butter')}
				>
					⇄ {flipped.butter ? 'Show Front Pack' : 'Lift & Flip: View Back Ingredients'}
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

				<button
					type="button"
					class="flat-flip-trigger raspberry-btn"
					onclick={() => toggleFlip('raspberry')}
				>
					⇄ {flipped.raspberry ? 'Show Front Pack' : 'Lift & Flip: View Back Ingredients'}
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

				<button
					type="button"
					class="flat-flip-trigger yeast-btn"
					onclick={() => toggleFlip('yeast')}
				>
					⇄ {flipped.yeast ? 'Show Front Pack' : 'Lift & Flip: View Back Ingredients'}
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

				<button
					type="button"
					class="flat-flip-trigger peanut-btn"
					onclick={() => toggleFlip('peanut')}
				>
					⇄ {flipped.peanut ? 'Show Front Pack' : 'Lift & Flip: View Back Ingredients'}
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
				<a href="/flavours" class="flat-action-btn">View All Nutrition & Specs →</a>
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
	/* SECTION 1: E-READER HERO */
	.hero-stage {
		position: relative;
		min-height: 100vh;
		min-height: 100dvh;
		background: #19012c;
		overflow: hidden;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.hero-under-book {
		position: absolute;
		inset: 0;
		background: #240340;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1;
		padding: 4rem 2rem;
		text-align: center;
	}

	.under-content {
		max-width: 600px;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.25rem;
	}

	.under-eyebrow {
		color: #e24bff;
		font-weight: 800;
		letter-spacing: 0.16em;
		font-size: 0.9rem;
	}

	.under-headline {
		color: #ffffff;
		font-size: clamp(2.5rem, 5vw, 4rem);
		font-weight: 900;
		letter-spacing: -0.02em;
	}

	.under-note {
		color: #f4c7ff;
		font-size: 1.15rem;
		line-height: 1.5;
	}

	.flat-btn-ghost {
		background: #e24bff;
		color: #240340;
		padding: 0.8rem 1.8rem;
		border-radius: 9999px;
		text-decoration: none;
		font-weight: 900;
		font-size: 0.95rem;
		border: 2px solid #e24bff;
		transition: all 0.15s;
	}

	.flat-btn-ghost:hover {
		background: transparent;
		color: #e24bff;
	}

	/* E-READER PAGE THAT FLIPS ON SCROLL */
	.ereader-page {
		width: 100%;
		min-height: 100vh;
		min-height: 100dvh;
		background: #3b0764;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		position: relative;
		z-index: 10;
		transform-origin: left center;
		transition: transform 0.08s ease-out;
		padding: 5rem 1.5rem 3rem;
		border-right: 4px solid #e24bff;
	}

	.ereader-page-inner {
		max-width: 860px;
		width: 100%;
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.25rem;
	}

	.hero-top-kicker {
		font-size: 0.92rem;
		font-weight: 800;
		letter-spacing: 0.18em;
		color: #e24bff;
		text-transform: uppercase;
	}

	.hero-wordmark-container {
		width: clamp(280px, 60vw, 560px);
		margin: 0.5rem 0;
	}

	.hero-tagline {
		font-size: clamp(1.4rem, 4vw, 2.6rem);
		font-weight: 900;
		color: #f4c7ff;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}

	.hero-pack-box {
		position: relative;
		margin: 1.25rem 0;
	}

	.hero-flat-pack {
		max-height: 340px;
		width: auto;
		max-width: 88vw;
		border-radius: 14px;
		border: 3px solid #e24bff;
	}

	.flat-peel-tag {
		position: absolute;
		top: 10px;
		right: 10px;
		background: #e24bff;
		color: #3b0764;
		font-weight: 900;
		font-size: 0.72rem;
		padding: 4px 10px;
		border-radius: 999px;
		letter-spacing: 0.08em;
		border: 1.5px solid #3b0764;
	}

	.hero-meta-row {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.6rem;
		flex-wrap: wrap;
	}

	.meta-tag {
		background: #240340;
		border: 2px solid #e24bff;
		color: #f4c7ff;
		padding: 0.45rem 1.15rem;
		border-radius: 9999px;
		font-size: 0.84rem;
		font-weight: 800;
		letter-spacing: 0.04em;
	}

	.page-flip-indicator {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.35rem;
		margin-top: 1.5rem;
		color: #e24bff;
		font-weight: 800;
		font-size: 0.8rem;
		letter-spacing: 0.1em;
	}

	.flip-icon {
		font-size: 1.5rem;
	}

	/* SECTION 2: 3 STEPS WITH THRESHOLD EXPLOSION */
	.steps-stage {
		min-height: 100vh;
		min-height: 100dvh;
		background: #3b0764;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 6rem 1.5rem;
		position: relative;
		overflow: hidden;
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
		font-size: clamp(2.6rem, 5.5vw, 4.4rem);
		font-weight: 900;
		color: #ffffff;
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
		background: #e24bff;
		color: #3b0764;
		border: 2px solid #e24bff;
		padding: 0.6rem 1.4rem;
		border-radius: 9999px;
		font-weight: 900;
		font-size: 0.92rem;
		cursor: pointer;
		transition: all 0.15s;
		font-family: inherit;
	}

	.threshold-btn.active {
		background: #240340;
		color: #e24bff;
		border-color: #e24bff;
	}

	.threshold-status {
		font-size: 0.85rem;
		font-weight: 700;
		color: #f4c7ff;
	}

	.steps-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 2rem;
		position: relative;
		perspective: 1200px;
	}

	.step-card {
		padding: 2.75rem 2rem;
		border-radius: 18px;
		text-align: left;
		display: flex;
		flex-direction: column;
		position: relative;
		transition:
			transform 0.65s cubic-bezier(0.2, 0.9, 0.2, 1),
			opacity 0.5s ease;
	}

	.step-card-1 {
		background: #240340;
		border: 3px solid #e24bff;
		color: #f4c7ff;
	}

	.step-card-2 {
		background: #4a3000;
		border: 3px solid #ffd640;
		color: #ffeeb3;
	}

	.step-card-3 {
		background: #460820;
		border: 3px solid #ff467a;
		color: #ffd6e3;
	}

	.step-card-1.blast-tl {
		transform: translate3d(-320px, -180px, 0) rotate(-20deg) scale(0.9);
		opacity: 0.1;
		pointer-events: none;
	}

	.step-card-2.blast-down {
		transform: translate3d(0, 260px, 0) scale(1.15);
		opacity: 0.1;
		pointer-events: none;
	}

	.step-card-3.blast-tr {
		transform: translate3d(320px, -180px, 0) rotate(20deg) scale(0.9);
		opacity: 0.1;
		pointer-events: none;
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
		color: #ffffff;
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

	.explosion-alert {
		margin-top: 3rem;
		display: flex;
		justify-content: center;
		animation: fadeIn 0.3s ease;
	}

	.alert-box {
		background: #240340;
		border: 2px solid #e24bff;
		color: #e24bff;
		padding: 0.85rem 1.8rem;
		border-radius: 999px;
		font-weight: 800;
		font-size: 0.9rem;
		display: flex;
		align-items: center;
		gap: 0.75rem;
		letter-spacing: 0.04em;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: scale(0.95);
		}
		to {
			opacity: 1;
			transform: scale(1);
		}
	}

	/* SECTIONS 3-6: DEDICATED FLAVOUR WORLDS */
	.flavour-worlds-list {
		display: flex;
		flex-direction: column;
	}

	.flavour-screen {
		min-height: 100vh;
		min-height: 100dvh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 6rem 2rem;
		position: relative;
	}

	.flavour-content-grid {
		max-width: 1140px;
		width: 100%;
		display: grid;
		grid-template-columns: 400px 1fr;
		gap: 4.5rem;
		align-items: center;
	}

	.flavour-media-side {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
	}

	/* 3D LIFT & FLIP ANIMATION STAGE */
	.flip-stage {
		perspective: 1200px;
		width: 290px;
		height: 410px;
	}

	.flip-card {
		position: relative;
		width: 100%;
		height: 100%;
		transition: transform 0.65s cubic-bezier(0.34, 1.56, 0.64, 1);
		transform-style: preserve-3d;
	}

	.flip-card.flipped {
		transform: translateY(-18px) scale(1.05) rotateY(180deg);
	}

	.flip-face {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
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

	.flat-flip-trigger {
		font-family: inherit;
		font-weight: 900;
		font-size: 0.88rem;
		padding: 0.65rem 1.4rem;
		border-radius: 9999px;
		cursor: pointer;
		border: 2px solid;
		transition: transform 0.15s;
		letter-spacing: 0.03em;
	}

	.flat-flip-trigger:hover {
		transform: translateY(-2px);
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
	}

	.spec-data {
		font-size: 1.05rem;
		font-weight: 800;
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
		background: #ffd640;
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
		border-left: 4px solid #4a3000;
	}

	/* RASPBERRY THEME (FLAT) */
	.raspberry-screen {
		background: #ff467a;
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
		color: #ffffff;
	}
	.raspberry-callout {
		background: #eb386b;
		color: #ffffff;
		border-left: 4px solid #460820;
	}

	/* YEAST THEME (FLAT) */
	.yeast-screen {
		background: #e24bff;
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
		color: #ffffff;
	}
	.yeast-callout {
		background: #d338f0;
		color: #ffffff;
		border-left: 4px solid #3b0764;
	}

	/* PEANUT THEME (FLAT) */
	.peanut-screen {
		background: #ff8c30;
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
		color: #ffffff;
	}
	.peanut-callout {
		background: #eb7c22;
		color: #ffffff;
		border-left: 4px solid #4e2408;
	}

	/* SECTION 7: MIXED SHEET */
	.mixed-pack-stage {
		background: #240340;
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
		color: #ffffff;
		letter-spacing: -0.03em;
		margin: 0;
	}

	.mixed-lead {
		font-size: 1.2rem;
		line-height: 1.5;
		color: #f4c7ff;
	}

	.flat-price-card {
		background: #3b0764;
		border: 2px solid #e24bff;
		padding: 1.75rem;
		border-radius: 14px;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.price-giant {
		font-size: 3rem;
		font-weight: 900;
		color: #e24bff;
		line-height: 1;
	}

	.price-explainer {
		font-size: 0.95rem;
		color: #f4c7ff;
		line-height: 1.45;
	}

	.mixed-btn-row {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
		margin-top: 0.5rem;
	}

	.flat-action-btn {
		background: #e24bff;
		color: #3b0764;
		font-weight: 900;
		font-size: 1rem;
		padding: 1rem 1.8rem;
		border-radius: 9999px;
		text-decoration: none;
		border: 2px solid #e24bff;
		transition: all 0.15s ease;
	}

	.flat-action-btn:hover {
		background: transparent;
		color: #e24bff;
	}

	.flat-outline-btn {
		background: transparent;
		color: #e24bff;
		font-weight: 900;
		font-size: 1rem;
		padding: 1rem 1.8rem;
		border-radius: 9999px;
		border: 2px solid #e24bff;
		cursor: pointer;
		font-family: inherit;
		transition: all 0.15s ease;
	}

	.flat-outline-btn:hover {
		background: #e24bff;
		color: #3b0764;
	}

	/* RESPONSIVE */
	@media (max-width: 960px) {
		.steps-grid {
			grid-template-columns: 1fr;
			gap: 1.5rem;
		}

		.step-card-1.blast-tl,
		.step-card-2.blast-down,
		.step-card-3.blast-tr {
			transform: scale(0.9);
			opacity: 0.15;
		}

		.flavour-content-grid {
			grid-template-columns: 1fr;
			gap: 2.5rem;
			text-align: center;
		}

		.flavour-copy-side {
			align-items: center;
		}

		.mixed-content-container {
			grid-template-columns: 1fr;
			text-align: center;
		}

		.mixed-copy-col {
			align-items: center;
		}
	}

	@media (max-width: 640px) {
		.hero-flat-pack {
			max-height: 260px;
		}

		.step-card {
			padding: 2rem 1.5rem;
		}

		.flat-specs-grid {
			grid-template-columns: 1fr;
			width: 100%;
		}

		.mixed-btn-row {
			flex-direction: column;
			width: 100%;
		}

		.flat-action-btn,
		.flat-outline-btn {
			width: 100%;
			text-align: center;
		}
	}
</style>
