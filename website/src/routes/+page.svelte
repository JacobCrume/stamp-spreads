<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import Wordmark from '../lib/Wordmark.svelte';
	import FlavourPackFront from '../lib/FlavourPackFront.svelte';
	import FlavourPackBack from '../lib/FlavourPackBack.svelte';
	import { colorScheme, setSectionTheme, type SectionTheme } from '../lib/theme.svelte';

	let scrollY = $state(0);
	let innerHeight = $state(800);
	let innerWidth = $state(1200);

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
				{ id: 'steps', theme: 'steps' },
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
<section id="steps" class="steps-stage">
	<div class="steps-inner">
		<div class="section-kicker">THE 3-SECOND ROUTINE</div>
		<h2 class="section-title">HOW STAMP WORKS</h2>
		<p class="section-sub">
			Forget sticky jars, table knives, and office sinks. Breakfast happens in three rapid moves.
		</p>

		<div class="steps-grid">
			<!-- Step 1 -->
			<div class="step-card">
				<div class="step-badge">01</div>
				<h3 class="step-label">PEEL</h3>
				<p class="step-text">
					Peel one 10 g disc off the food-grade release film. Sits clean and dry in your fingers.
				</p>
				<div class="flat-rule"></div>
			</div>

			<!-- Step 2 -->
			<div class="step-card">
				<div class="step-badge">02</div>
				<h3 class="step-label">PRESS</h3>
				<p class="step-text">
					Press the disc directly onto fresh hot toast. No table knife required.
				</p>
				<div class="flat-rule"></div>
			</div>

			<!-- Step 3 -->
			<div class="step-card">
				<div class="step-badge">03</div>
				<h3 class="step-label">SPREAD</h3>
				<p class="step-text">
					Thermal contact melts the disc into toast grooves within 3 seconds. Enjoy clean breakfast.
				</p>
				<div class="flat-rule"></div>
			</div>
		</div>
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
							<FlavourPackFront flavour="butter" />
						</div>
						<div class="flip-face flip-back">
							<FlavourPackBack flavour="butter" />
						</div>
					</div>
				</div>

				<!-- Simple Round Icon Flip Button -->
				<button
					type="button"
					class="round-flip-btn"
					class:is-flipped={flipped.butter}
					onclick={() => toggleFlip('butter')}
					aria-label={flipped.butter ? 'Flip to front of Salted Butter pack' : 'Flip to back of Salted Butter pack (nutrition & ingredients)'}
					title={flipped.butter ? 'Flip to front' : 'Flip to back ingredients'}
				>
					<svg class="flip-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<path d="M21 2v6h-6"></path>
						<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
						<path d="M3 22v-6h6"></path>
						<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
					</svg>
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
							<FlavourPackFront flavour="raspberry" />
						</div>
						<div class="flip-face flip-back">
							<FlavourPackBack flavour="raspberry" />
						</div>
					</div>
				</div>

				<!-- Simple Round Icon Flip Button -->
				<button
					type="button"
					class="round-flip-btn"
					class:is-flipped={flipped.raspberry}
					onclick={() => toggleFlip('raspberry')}
					aria-label={flipped.raspberry ? 'Flip to front of Raspberry pack' : 'Flip to back of Raspberry pack (nutrition & ingredients)'}
					title={flipped.raspberry ? 'Flip to front' : 'Flip to back ingredients'}
				>
					<svg class="flip-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<path d="M21 2v6h-6"></path>
						<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
						<path d="M3 22v-6h6"></path>
						<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
					</svg>
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
							<FlavourPackFront flavour="yeast" />
						</div>
						<div class="flip-face flip-back">
							<FlavourPackBack flavour="yeast" />
						</div>
					</div>
				</div>

				<!-- Simple Round Icon Flip Button -->
				<button
					type="button"
					class="round-flip-btn"
					class:is-flipped={flipped.yeast}
					onclick={() => toggleFlip('yeast')}
					aria-label={flipped.yeast ? 'Flip to front of Yeast Extract pack' : 'Flip to back of Yeast Extract pack (nutrition & ingredients)'}
					title={flipped.yeast ? 'Flip to front' : 'Flip to back ingredients'}
				>
					<svg class="flip-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<path d="M21 2v6h-6"></path>
						<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
						<path d="M3 22v-6h6"></path>
 						<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
					</svg>
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
							<FlavourPackFront flavour="peanut" />
						</div>
						<div class="flip-face flip-back">
							<FlavourPackBack flavour="peanut" />
						</div>
					</div>
				</div>

				<!-- Simple Round Icon Flip Button -->
				<button
					type="button"
					class="round-flip-btn"
					class:is-flipped={flipped.peanut}
					onclick={() => toggleFlip('peanut')}
					aria-label={flipped.peanut ? 'Flip to front of Roasted Peanut pack' : 'Flip to back of Roasted Peanut pack (nutrition & ingredients)'}
					title={flipped.peanut ? 'Flip to front' : 'Flip to back ingredients'}
				>
					<svg class="flip-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<path d="M21 2v6h-6"></path>
						<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
						<path d="M3 22v-6h6"></path>
						<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
					</svg>
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
			<div class="mixed-packs-grid">
				<div class="mixed-pack-item"><FlavourPackFront flavour="butter" standalone={true} /></div>
				<div class="mixed-pack-item"><FlavourPackFront flavour="raspberry" standalone={true} /></div>
				<div class="mixed-pack-item"><FlavourPackFront flavour="yeast" standalone={true} /></div>
				<div class="mixed-pack-item"><FlavourPackFront flavour="peanut" standalone={true} /></div>
			</div>
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
	.flip-face,
	.round-flip-btn,
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
			background-color 0.45s ease,
			color 0.45s ease;
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
		height: 560px;
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
		transform: translateY(-12px) rotateY(180deg);
	}

	.flip-face {
		position: absolute;
		inset: 0;
		backface-visibility: hidden;
		-webkit-backface-visibility: hidden;
		border-radius: 48px;
		border: none;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0;
		background: transparent;
		filter: drop-shadow(0 20px 48px rgba(0, 0, 0, 0.22));
	}

	.flip-back {
		transform: rotateY(180deg);
	}

	/* SIMPLE ROUND ICON FLIP BUTTON */
	.round-flip-btn {
		width: 56px;
		height: 56px;
		border-radius: 50%;
		border: none;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		background: var(--color-tertiary);
		color: var(--color-primary);
		transition:
			transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1),
			background-color 0.45s ease,
			color 0.45s ease;
	}

	.round-flip-btn:hover {
		transform: scale(1.12);
	}

	.round-flip-btn:active {
		transform: scale(0.92);
	}

	.round-flip-btn .flip-svg {
		width: 26px;
		height: 26px;
		transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	.round-flip-btn.is-flipped .flip-svg {
		transform: rotate(180deg);
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
		color: var(--color-primary);
		opacity: 0.85;
	}

	.flavour-headline {
		font-size: clamp(2.8rem, 6vw, 5rem);
		font-weight: 900;
		line-height: 0.95;
		letter-spacing: -0.03em;
		margin: 0;
		color: var(--color-primary);
	}

	.flavour-lead {
		font-size: 1.2rem;
		line-height: 1.5;
		font-weight: 600;
		color: #ffffff;
		opacity: 0.95;
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

	.mixed-packs-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1.25rem;
		max-width: 480px;
		width: 100%;
		margin: 0 auto;
	}

	.mixed-pack-item {
		filter: drop-shadow(0 16px 32px rgba(0, 0, 0, 0.28));
		border-radius: 24px;
		transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	.mixed-pack-item:hover {
		transform: translateY(-6px) scale(1.03);
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
