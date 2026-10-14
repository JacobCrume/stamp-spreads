<script lang="ts">
	import { onMount } from 'svelte';

	let scrollY = $state(0);
	let innerHeight = $state(800);

	// Peel effect progress (0 to 1 during the first viewport of scrolling)
	let peelProgress = $derived(Math.min(1, Math.max(0, scrollY / (innerHeight * 0.8))));

	// Explosion effect progress (0 to 1 as user scrolls through the 3-step section)
	let explodeProgress = $derived(
		Math.min(1, Math.max(0, (scrollY - innerHeight * 0.8) / (innerHeight * 0.7)))
	);

	// Active pack side view toggles
	let activeSide: Record<string, 'front' | 'back'> = $state({
		butter: 'front',
		raspberry: 'front',
		yeast: 'front',
		peanut: 'front'
	});

	function toggleSide(id: string) {
		activeSide[id] = activeSide[id] === 'front' ? 'back' : 'front';
	}
</script>

<svelte:window bind:scrollY bind:innerHeight />

<svelte:head>
	<title>STAMP — Peel. Press. Toast.</title>
	<meta
		name="description"
		content="Stamp: Single-serve peel-and-press spread discs for toast. Bold breakfast innovation with no knife and no open jar."
	/>
</svelte:head>

<!-- SECTION 1: FULL-SCREEN HERO WITH INTERACTIVE SCROLL-PEEL -->
<section class="hero-wrapper">
	<div
		class="peel-surface"
		style:transform="perspective(1400px) rotateX({peelProgress * -28}deg) rotateY({peelProgress * 18}deg) translate3d({peelProgress * 40}px, -{peelProgress * 90}px, -{peelProgress * 120}px)"
		style:opacity={1 - peelProgress * 0.45}
	>
		<div class="hero-content">
			<div class="hero-kicker">NEW ZEALAND BREAKFAST INNOVATION</div>
			<h1 class="hero-brand">STAMP</h1>
			<p class="hero-tagline">PEEL. PRESS. TOAST.</p>

			<div class="hero-pack-stage">
				<div
					class="pack-floating"
					style:transform="translateY({peelProgress * -30}px) scale({1 - peelProgress * 0.1})"
				>
					<img src="/pack.png" alt="STAMP 8-Stamp Sheet" class="hero-pack-img" />
					<div class="peel-corner-hint">
						<span class="hint-text">PEEL HERE</span>
						<span class="hint-curl"></span>
					</div>
				</div>
			</div>

			<div class="hero-meta">
				<span class="meta-pill">$5.00 NZD / SHEET</span>
				<span class="meta-dot">·</span>
				<span class="meta-pill">8 × 10 g STAMPS</span>
				<span class="meta-dot">·</span>
				<span class="meta-pill">NO KNIFE · NO OPEN JAR</span>
			</div>

			<div class="scroll-indicator" style:opacity={1 - peelProgress * 2}>
				<span class="scroll-arrow">↓</span>
				<span class="scroll-label">SCROLL DOWN TO PEEL</span>
			</div>
		</div>

		<!-- Under-sheet peel release shimmer line -->
		<div
			class="peel-fold-line"
			style:opacity={peelProgress > 0.05 ? Math.min(1, peelProgress * 1.5) : 0}
			style:transform="scaleX({0.5 + peelProgress * 0.5})"
		></div>
	</div>

	<!-- Background reveal layer visible as the hero curls away -->
	<div class="hero-underlayer">
		<div class="underlayer-pattern">
			<span>STAMP</span><span>RELEASE FILM</span><span>10 g PORTIONS</span><span>HOT TOAST READY</span>
		</div>
	</div>
</section>

<!-- SECTION 2: THE 3 STEPS WITH DYNAMIC EXPLOSION TRANSITION -->
<section id="steps" class="steps-wrapper">
	<div class="steps-container">
		<div class="section-kicker">THE 3-SECOND GESTURE</div>
		<h2 class="section-heading">HOW STAMP WORKS</h2>
		<p class="section-sub">
			Forget messy jars, butter knives, and morning sinks. Breakfast happens in three rapid steps.
		</p>

		<div class="steps-grid">
			<!-- Step 1 Card: Explodes top-left -->
			<div
				class="step-card step-1"
				style:transform="translate3d(-{explodeProgress * 280}px, -{explodeProgress * 160}px, 0) rotate(-{explodeProgress * 16}deg) scale({1 + explodeProgress * 0.15})"
				style:opacity={1 - explodeProgress * 0.85}
			>
				<div class="step-num-badge">01</div>
				<h3 class="step-title">PEEL</h3>
				<p class="step-desc">
					Peel one 10 g disc off the food-grade release film. Sits dry and ready in your fingers.
				</p>
				<div class="step-accent-bar"></div>
			</div>

			<!-- Step 2 Card: Blasts down/center -->
			<div
				class="step-card step-2"
				style:transform="translate3d(0, {explodeProgress * 220}px, 0) scale({1 + explodeProgress * 0.2})"
				style:opacity={1 - explodeProgress * 0.85}
			>
				<div class="step-num-badge">02</div>
				<h3 class="step-title">PRESS</h3>
				<p class="step-desc">
					Press the portion directly onto freshly toasted, steaming hot bread. Done in a second.
				</p>
				<div class="step-accent-bar"></div>
			</div>

			<!-- Step 3 Card: Explodes top-right -->
			<div
				class="step-card step-3"
				style:transform="translate3d({explodeProgress * 280}px, -{explodeProgress * 160}px, 0) rotate({explodeProgress * 16}deg) scale({1 + explodeProgress * 0.15})"
				style:opacity={1 - explodeProgress * 0.85}
			>
				<div class="step-num-badge">03</div>
				<h3 class="step-title">TOAST</h3>
				<p class="step-desc">
					Residual toast heat softens the disc into an even, glossy layer with zero crumb tearing.
				</p>
				<div class="step-accent-bar"></div>
			</div>
		</div>

		<!-- Explosion shockwave lines triggered on scroll -->
		<div
			class="explosion-rays"
			style:opacity={explodeProgress > 0.1 ? Math.min(0.9, explodeProgress * 1.4) : 0}
			style:transform="scale({0.8 + explodeProgress * 0.8})"
		></div>
	</div>
</section>

<!-- SECTIONS 3-6: DEDICATED FULL-SCREEN IMMERSIVE FLAVOUR WORLDS -->
<div id="flavours" class="flavour-worlds-container">
	<!-- FLAVOUR 1: SALTED BUTTER (ELECTRIC GOLD & BURNT CARAMEL) -->
	<section class="flavour-world flavour-butter">
		<div class="flavour-inner">
			<div class="flavour-visual">
				<div class="pack-flipper">
					{#if activeSide.butter === 'front'}
						<img src="/flavours/butter.png" alt="Salted Butter Stamp" class="flavour-pack" />
					{:else}
						<img src="/flavours/butter-back.png" alt="Salted Butter Back" class="flavour-pack back" />
					{/if}
				</div>
				<button class="flip-btn" onclick={() => toggleSide('butter')}>
					⇄ View {activeSide.butter === 'front' ? 'Back Ingredients' : 'Front Pack'}
				</button>
			</div>

			<div class="flavour-info">
				<div class="flavour-eyebrow">01 / LAUNCH RANGE</div>
				<h2 class="flavour-name">SALTED BUTTER</h2>
				<p class="flavour-hero-desc">
					Rich, clean cultured butterfat with a measured 2.5% salt balance. Melts instantly across hot toast without tearing fragile bread.
				</p>

				<div class="specs-pillbox">
					<div class="spec-pill">
						<span class="pill-label">FORMULA</span>
						<span class="pill-val">78 g butterfat · 2 g salt</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">ALLERGEN</span>
						<span class="pill-val">CONTAINS MILK</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">STABILITY</span>
						<span class="pill-val">12 Months Ambient</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">PRICE</span>
						<span class="pill-val">$5.00 / 8-Stamp Sheet</span>
					</div>
				</div>

				<div class="flavour-callout">
					Sold as a shelf-stable butter spread, not a pat of fridge butter. Zero added vegetable oils or artificial preservatives.
				</div>
			</div>
		</div>
	</section>

	<!-- FLAVOUR 2: RASPBERRY (VIBRANT NEON RASPBERRY & DARK WILD BERRY) -->
	<section class="flavour-world flavour-raspberry">
		<div class="flavour-inner">
			<div class="flavour-visual">
				<div class="pack-flipper">
					{#if activeSide.raspberry === 'front'}
						<img src="/flavours/raspberry.png" alt="Raspberry Stamp" class="flavour-pack" />
					{:else}
						<img src="/flavours/raspberry-back.png" alt="Raspberry Back" class="flavour-pack back" />
					{/if}
				</div>
				<button class="flip-btn" onclick={() => toggleSide('raspberry')}>
					⇄ View {activeSide.raspberry === 'front' ? 'Back Ingredients' : 'Front Pack'}
				</button>
			</div>

			<div class="flavour-info">
				<div class="flavour-eyebrow">02 / LAUNCH RANGE</div>
				<h2 class="flavour-name">SLOW-COOKED RASPBERRY</h2>
				<p class="flavour-hero-desc">
					150 g of real whole raspberries cooked down into every 100 g of thick, jewel-red spread. Brightened with fresh lemon juice.
				</p>

				<div class="specs-pillbox">
					<div class="spec-pill">
						<span class="pill-label">FRUIT RATIO</span>
						<span class="pill-val">150 g Fruit / 100 g Paste</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">ALLERGENS</span>
						<span class="pill-val">No Major Recipe Allergens</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">PRESERVATION</span>
						<span class="pill-val">Natural Fruit Solids</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">SHEET WEIGHT</span>
						<span class="pill-val">80 g Net (8 Stamps)</span>
					</div>
				</div>

				<div class="flavour-callout">
					Real raspberries, caster sugar, and lemon juice. No artificial gelling agents and no unsupported organic claims.
				</div>
			</div>
		</div>
	</section>

	<!-- FLAVOUR 3: YEAST EXTRACT (ELECTRIC VIOLET & DEEP INK PURPLE) -->
	<section class="flavour-world flavour-yeast">
		<div class="flavour-inner">
			<div class="flavour-visual">
				<div class="pack-flipper">
					{#if activeSide.yeast === 'front'}
						<img src="/flavours/yeast.png" alt="Yeast Extract Stamp" class="flavour-pack" />
					{:else}
						<img src="/flavours/yeast-back.png" alt="Yeast Extract Back" class="flavour-pack back" />
					{/if}
				</div>
				<button class="flip-btn" onclick={() => toggleSide('yeast')}>
					⇄ View {activeSide.yeast === 'front' ? 'Back Ingredients' : 'Front Pack'}
				</button>
			</div>

			<div class="flavour-info">
				<div class="flavour-eyebrow">03 / LAUNCH RANGE</div>
				<h2 class="flavour-name">YEAST EXTRACT</h2>
				<p class="flavour-hero-desc">
					Deep, roasted umami paste crafted for toast loyalists. Thick, glossy, and formulated with 80% concentrated yeast extract.
				</p>

				<div class="specs-pillbox">
					<div class="spec-pill">
						<span class="pill-label">YEAST EXTRACT</span>
						<span class="pill-val">80% Concentrated</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">MALT BLEND</span>
						<span class="pill-val">15.5% Barley Malt</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">ALLERGEN</span>
						<span class="pill-val">CONTAINS GLUTEN (BARLEY)</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">INTEGRITY</span>
						<span class="pill-val">Proprietary NZ Recipe</span>
					</div>
				</div>

				<div class="flavour-callout">
					NOT gluten-free. Contains barley malt extract. No therapeutic or medical treatment claims.
				</div>
			</div>
		</div>
	</section>

	<!-- FLAVOUR 4: ROASTED PEANUT (WARM OCHRE ORANGE & ROASTED UMBER) -->
	<section class="flavour-world flavour-peanut">
		<div class="flavour-inner">
			<div class="flavour-visual">
				<div class="pack-flipper">
					{#if activeSide.peanut === 'front'}
						<img src="/flavours/peanut.png" alt="Roasted Peanut Stamp" class="flavour-pack" />
					{:else}
						<img src="/flavours/peanut-back.png" alt="Roasted Peanut Back" class="flavour-pack back" />
					{/if}
				</div>
				<button class="flip-btn" onclick={() => toggleSide('peanut')}>
					⇄ View {activeSide.peanut === 'front' ? 'Back Ingredients' : 'Front Pack'}
				</button>
			</div>

			<div class="flavour-info">
				<div class="flavour-eyebrow">04 / LAUNCH RANGE</div>
				<h2 class="flavour-name">ROASTED PEANUT</h2>
				<p class="flavour-hero-desc">
					96% real roasted peanuts with a silky melt. Engineered with a stabilizing vegetable fat fraction so oil never separates in your bag.
				</p>

				<div class="specs-pillbox">
					<div class="spec-pill">
						<span class="pill-label">PEANUT CONTENT</span>
						<span class="pill-val">96% Roasted Peanuts</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">STABILIZER</span>
						<span class="pill-val">2.3% Anti-Oil Fraction</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">ALLERGEN</span>
						<span class="pill-val">CONTAINS PEANUTS</span>
					</div>
					<div class="spec-pill">
						<span class="pill-label">POCKETABLE</span>
						<span class="pill-val">Zero Separation</span>
					</div>
				</div>

				<div class="flavour-callout">
					Pure roasted peanuts and sea salt. Zero separated oil pooling on top; dissolves into hot toast immediately.
				</div>
			</div>
		</div>
	</section>
</div>

<!-- SECTION 7: THE MIXED SHEET & CATEGORY DISRUPTION -->
<section class="mixed-disruption-section">
	<div class="disruption-inner">
		<div class="disruption-media">
			<img src="/flavour-packs.png" alt="All 4 Stamp Flavour Packs" class="four-packs-hero" />
		</div>

		<div class="disruption-copy">
			<div class="disruption-kicker">THE HERO COMBINATION</div>
			<h2 class="disruption-title">THE MIXED SHEET</h2>
			<p class="disruption-lead">
				Two stamps of each flavour on one 8-stamp card sheet: Salted Butter, Raspberry, Yeast extract, and Roasted Peanut.
			</p>

			<div class="disruption-price-card">
				<div class="big-price">$5.00 NZD</div>
				<div class="price-context">
					<strong>$6.25 per 100 g</strong> · 80 g total net weight<br />
					Priced for portable portion convenience, avoiding messy jars and communal sink knives.
				</div>
			</div>

			<div class="disruption-actions">
				<a href="/flavours" class="bold-cta-btn">View All Nutrition & Allergen Panels →</a>
				<button
					type="button"
					class="bold-outline-btn"
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
	/* RESET & TYPOGRAPHY ENFORCEMENT - ZERO WHITE OR BLACK */
	:global(:root) {
		--stamp-purple-dark: #3b0764;
		--stamp-purple-light: #e24bff;
		--butter-dark: #4a3000;
		--butter-light: #ffd640;
		--raspberry-dark: #460820;
		--raspberry-light: #ff467a;
		--yeast-dark: #3b0764;
		--yeast-light: #e24bff;
		--peanut-dark: #4e2408;
		--peanut-light: #ff8c30;
	}

	/* SECTION 1: PEEL HERO */
	.hero-wrapper {
		position: relative;
		min-height: 100vh;
		min-height: 100dvh;
		background: #240340;
		overflow: hidden;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.peel-surface {
		width: 100%;
		min-height: 100vh;
		min-height: 100dvh;
		background: linear-gradient(135deg, #3b0764 0%, #200336 100%);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		position: relative;
		z-index: 10;
		transform-origin: top left;
		transition: transform 0.08s ease-out;
		padding: 3rem 1.5rem;
		box-shadow: 0 20px 80px rgba(18, 1, 30, 0.9);
	}

	.hero-content {
		max-width: 900px;
		width: 100%;
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.25rem;
	}

	.hero-kicker {
		font-size: 0.95rem;
		font-weight: 800;
		letter-spacing: 0.18em;
		color: #e24bff;
		text-transform: uppercase;
	}

	.hero-brand {
		font-size: clamp(5rem, 15vw, 11rem);
		font-weight: 900;
		line-height: 0.85;
		color: #e24bff;
		letter-spacing: -0.04em;
		text-shadow: 0 8px 32px rgba(226, 75, 255, 0.5);
		margin: 0;
	}

	.hero-tagline {
		font-size: clamp(1.4rem, 4vw, 2.8rem);
		font-weight: 900;
		color: #fce7ff;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}

	.hero-pack-stage {
		position: relative;
		margin: 1.5rem 0;
	}

	.pack-floating {
		position: relative;
		display: inline-block;
		filter: drop-shadow(0 24px 48px rgba(18, 1, 30, 0.8));
		transition: transform 0.1s ease-out;
	}

	.hero-pack-img {
		max-height: 380px;
		width: auto;
		max-width: 90vw;
		border-radius: 12px;
		border: 3px solid #e24bff;
	}

	.peel-corner-hint {
		position: absolute;
		top: 12px;
		right: 12px;
		background: #e24bff;
		color: #3b0764;
		font-weight: 900;
		font-size: 0.72rem;
		padding: 4px 10px;
		border-radius: 999px;
		letter-spacing: 0.08em;
		box-shadow: 0 4px 12px rgba(226, 75, 255, 0.6);
		animation: pulseHint 1.8s infinite alternate ease-in-out;
	}

	@keyframes pulseHint {
		from {
			transform: scale(0.95);
		}
		to {
			transform: scale(1.08);
		}
	}

	.hero-meta {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.75rem;
		flex-wrap: wrap;
	}

	.meta-pill {
		background: #240340;
		border: 1.5px solid #e24bff;
		color: #f4c7ff;
		padding: 0.5rem 1.25rem;
		border-radius: 9999px;
		font-size: 0.88rem;
		font-weight: 800;
		letter-spacing: 0.04em;
	}

	.meta-dot {
		color: #e24bff;
		font-weight: 900;
	}

	.scroll-indicator {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.35rem;
		margin-top: 1.5rem;
		color: #e24bff;
		font-weight: 800;
		font-size: 0.82rem;
		letter-spacing: 0.1em;
		animation: bounceArrow 1.5s infinite;
	}

	.scroll-arrow {
		font-size: 1.6rem;
		line-height: 1;
	}

	@keyframes bounceArrow {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(8px);
		}
	}

	.peel-fold-line {
		position: absolute;
		bottom: 0;
		right: 0;
		width: 100%;
		height: 8px;
		background: linear-gradient(90deg, transparent, #e24bff, #ff85ff);
		box-shadow: 0 0 24px #e24bff;
	}

	.hero-underlayer {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: #19012c;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1;
	}

	.underlayer-pattern {
		display: flex;
		gap: 2rem;
		color: rgba(226, 75, 255, 0.15);
		font-size: 3rem;
		font-weight: 900;
		white-space: nowrap;
	}

	/* SECTION 2: EXPLODING 3-STEP SECTION */
	.steps-wrapper {
		min-height: 100vh;
		min-height: 100dvh;
		background: #3b0764;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 5rem 1.5rem;
		position: relative;
		overflow: hidden;
	}

	.steps-container {
		max-width: 1200px;
		width: 100%;
		text-align: center;
		position: relative;
		z-index: 5;
	}

	.section-kicker {
		color: #e24bff;
		font-size: 0.95rem;
		font-weight: 800;
		letter-spacing: 0.16em;
		margin-bottom: 0.5rem;
	}

	.section-heading {
		font-size: clamp(2.8rem, 6vw, 4.8rem);
		font-weight: 900;
		color: #ffffff;
		letter-spacing: -0.03em;
		margin-bottom: 1rem;
	}

	.section-sub {
		max-width: 680px;
		margin: 0 auto 4rem;
		font-size: 1.15rem;
		color: #f4c7ff;
		line-height: 1.5;
	}

	.steps-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 2rem;
		position: relative;
	}

	.step-card {
		padding: 3rem 2rem;
		border-radius: 20px;
		text-align: left;
		display: flex;
		flex-direction: column;
		position: relative;
		box-shadow: 0 16px 48px rgba(18, 1, 30, 0.6);
		transition: transform 0.08s ease-out;
	}

	.step-1 {
		background: #240340;
		border: 3px solid #e24bff;
		color: #f4c7ff;
	}

	.step-2 {
		background: #4a3000;
		border: 3px solid #ffd640;
		color: #ffeeb3;
	}

	.step-3 {
		background: #460820;
		border: 3px solid #ff467a;
		color: #ffd6e3;
	}

	.step-num-badge {
		font-size: 3rem;
		font-weight: 900;
		line-height: 1;
		margin-bottom: 1.25rem;
	}

	.step-1 .step-num-badge {
		color: #e24bff;
	}
	.step-2 .step-num-badge {
		color: #ffd640;
	}
	.step-3 .step-num-badge {
		color: #ff467a;
	}

	.step-title {
		font-size: 2.2rem;
		font-weight: 900;
		letter-spacing: 0.02em;
		margin-bottom: 0.75rem;
		color: #ffffff;
	}

	.step-desc {
		font-size: 1.05rem;
		line-height: 1.5;
		flex: 1;
	}

	.step-accent-bar {
		height: 6px;
		width: 48px;
		border-radius: 999px;
		margin-top: 1.5rem;
	}

	.step-1 .step-accent-bar {
		background: #e24bff;
	}
	.step-2 .step-accent-bar {
		background: #ffd640;
	}
	.step-3 .step-accent-bar {
		background: #ff467a;
	}

	.explosion-rays {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 800px;
		height: 800px;
		background: radial-gradient(circle, rgba(226, 75, 255, 0.3) 0%, transparent 70%);
		pointer-events: none;
		z-index: 1;
	}

	/* SECTIONS 3-6: FLAVOUR WORLDS */
	.flavour-worlds-container {
		display: flex;
		flex-direction: column;
	}

	.flavour-world {
		min-height: 100vh;
		min-height: 100dvh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 5rem 2rem;
		position: relative;
	}

	.flavour-inner {
		max-width: 1200px;
		width: 100%;
		display: grid;
		grid-template-columns: 460px 1fr;
		gap: 4rem;
		align-items: center;
	}

	.flavour-visual {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
	}

	.pack-flipper {
		perspective: 1000px;
	}

	.flavour-pack {
		max-height: 480px;
		width: auto;
		max-width: 100%;
		border-radius: 16px;
		transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
	}

	.flavour-pack:hover {
		transform: scale(1.03) rotate(1deg);
	}

	.flip-btn {
		font-family: inherit;
		font-weight: 800;
		font-size: 0.88rem;
		padding: 0.6rem 1.4rem;
		border-radius: 9999px;
		cursor: pointer;
		transition: all 0.15s ease;
		letter-spacing: 0.04em;
	}

	.flavour-info {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.flavour-eyebrow {
		font-size: 0.95rem;
		font-weight: 900;
		letter-spacing: 0.16em;
	}

	.flavour-name {
		font-size: clamp(3rem, 7vw, 5.5rem);
		font-weight: 900;
		line-height: 0.95;
		letter-spacing: -0.03em;
		margin: 0;
	}

	.flavour-hero-desc {
		font-size: 1.25rem;
		line-height: 1.5;
		font-weight: 600;
	}

	.specs-pillbox {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
		margin: 0.5rem 0;
	}

	.spec-pill {
		padding: 1rem 1.25rem;
		border-radius: 12px;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.pill-label {
		font-size: 0.72rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		opacity: 0.8;
	}

	.pill-val {
		font-size: 1.05rem;
		font-weight: 800;
	}

	.flavour-callout {
		padding: 1.25rem 1.5rem;
		border-radius: 12px;
		font-size: 0.95rem;
		font-weight: 700;
		line-height: 1.5;
	}

	/* BUTTER THEME */
	.flavour-butter {
		background: #ffd640;
		color: #4a3000;
	}
	.flavour-butter .flavour-name {
		color: #4a3000;
	}
	.flavour-butter .flavour-pack {
		box-shadow: 0 20px 60px rgba(74, 48, 0, 0.45);
		border: 4px solid #4a3000;
	}
	.flavour-butter .flip-btn {
		background: #4a3000;
		color: #ffd640;
		border: 2px solid #4a3000;
	}
	.flavour-butter .flip-btn:hover {
		background: #6e4700;
	}
	.flavour-butter .spec-pill {
		background: #e8c028;
		color: #4a3000;
		border: 1.5px solid #4a3000;
	}
	.flavour-butter .flavour-callout {
		background: #f7ca22;
		border-left: 4px solid #4a3000;
	}

	/* RASPBERRY THEME */
	.flavour-raspberry {
		background: #ff467a;
		color: #460820;
	}
	.flavour-raspberry .flavour-name {
		color: #460820;
	}
	.flavour-raspberry .flavour-pack {
		box-shadow: 0 20px 60px rgba(70, 8, 32, 0.5);
		border: 4px solid #460820;
	}
	.flavour-raspberry .flip-btn {
		background: #460820;
		color: #ff467a;
		border: 2px solid #460820;
	}
	.flavour-raspberry .flip-btn:hover {
		background: #690f33;
	}
	.flavour-raspberry .spec-pill {
		background: #e83366;
		color: #ffffff;
		border: 1.5px solid #460820;
	}
	.flavour-raspberry .flavour-callout {
		background: #eb386b;
		color: #ffffff;
		border-left: 4px solid #460820;
	}

	/* YEAST THEME */
	.flavour-yeast {
		background: #e24bff;
		color: #3b0764;
	}
	.flavour-yeast .flavour-name {
		color: #3b0764;
	}
	.flavour-yeast .flavour-pack {
		box-shadow: 0 20px 60px rgba(59, 7, 100, 0.5);
		border: 4px solid #3b0764;
	}
	.flavour-yeast .flip-btn {
		background: #3b0764;
		color: #e24bff;
		border: 2px solid #3b0764;
	}
	.flavour-yeast .flip-btn:hover {
		background: #540b8f;
	}
	.flavour-yeast .spec-pill {
		background: #cb32e8;
		color: #ffffff;
		border: 1.5px solid #3b0764;
	}
	.flavour-yeast .flavour-callout {
		background: #d338f0;
		color: #ffffff;
		border-left: 4px solid #3b0764;
	}

	/* PEANUT THEME */
	.flavour-peanut {
		background: #ff8c30;
		color: #4e2408;
	}
	.flavour-peanut .flavour-name {
		color: #4e2408;
	}
	.flavour-peanut .flavour-pack {
		box-shadow: 0 20px 60px rgba(78, 36, 8, 0.5);
		border: 4px solid #4e2408;
	}
	.flavour-peanut .flip-btn {
		background: #4e2408;
		color: #ff8c30;
		border: 2px solid #4e2408;
	}
	.flavour-peanut .flip-btn:hover {
		background: #73360d;
	}
	.flavour-peanut .spec-pill {
		background: #e87820;
		color: #ffffff;
		border: 1.5px solid #4e2408;
	}
	.flavour-peanut .flavour-callout {
		background: #eb7c22;
		color: #ffffff;
		border-left: 4px solid #4e2408;
	}

	/* SECTION 7: MIXED SHEET & DISRUPTION */
	.mixed-disruption-section {
		background: #240340;
		border-top: 4px solid #e24bff;
		padding: 6rem 2rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.disruption-inner {
		max-width: 1200px;
		width: 100%;
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 4rem;
		align-items: center;
	}

	.four-packs-hero {
		width: 100%;
		max-height: 480px;
		object-fit: contain;
		border-radius: 16px;
		box-shadow: 0 24px 64px rgba(18, 1, 30, 0.85);
		border: 3px solid #e24bff;
	}

	.disruption-copy {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.disruption-kicker {
		color: #e24bff;
		font-size: 0.95rem;
		font-weight: 900;
		letter-spacing: 0.16em;
	}

	.disruption-title {
		font-size: clamp(2.8rem, 5vw, 4.2rem);
		font-weight: 900;
		line-height: 1;
		color: #ffffff;
		letter-spacing: -0.03em;
		margin: 0;
	}

	.disruption-lead {
		font-size: 1.2rem;
		line-height: 1.5;
		color: #f4c7ff;
	}

	.disruption-price-card {
		background: #3b0764;
		border: 2px solid #e24bff;
		padding: 1.75rem;
		border-radius: 14px;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.big-price {
		font-size: 3rem;
		font-weight: 900;
		color: #e24bff;
		line-height: 1;
	}

	.price-context {
		font-size: 0.95rem;
		color: #f4c7ff;
		line-height: 1.45;
	}

	.disruption-actions {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
		margin-top: 0.5rem;
	}

	.bold-cta-btn {
		background: #e24bff;
		color: #3b0764;
		font-weight: 900;
		font-size: 1rem;
		padding: 1rem 1.8rem;
		border-radius: 9999px;
		text-decoration: none;
		transition: all 0.15s ease;
		box-shadow: 0 4px 20px rgba(226, 75, 255, 0.5);
	}

	.bold-cta-btn:hover {
		background: #ff85ff;
		transform: translateY(-2px);
	}

	.bold-outline-btn {
		background: transparent;
		color: #e24bff;
		font-weight: 800;
		font-size: 1rem;
		padding: 1rem 1.8rem;
		border-radius: 9999px;
		border: 2px solid #e24bff;
		cursor: pointer;
		font-family: inherit;
		transition: all 0.15s ease;
	}

	.bold-outline-btn:hover {
		background: rgba(226, 75, 255, 0.2);
		transform: translateY(-2px);
	}

	/* RESPONSIVENESS */
	@media (max-width: 960px) {
		.steps-grid {
			grid-template-columns: 1fr;
			gap: 1.5rem;
		}

		.flavour-inner {
			grid-template-columns: 1fr;
			gap: 2.5rem;
			text-align: center;
		}

		.flavour-info {
			align-items: center;
		}

		.disruption-inner {
			grid-template-columns: 1fr;
			text-align: center;
		}

		.disruption-copy {
			align-items: center;
		}
	}

	@media (max-width: 640px) {
		.hero-pack-img {
			max-height: 280px;
		}

		.step-card {
			padding: 2rem 1.5rem;
		}

		.specs-pillbox {
			grid-template-columns: 1fr;
			width: 100%;
		}

		.disruption-actions {
			flex-direction: column;
			width: 100%;
		}

		.bold-cta-btn,
		.bold-outline-btn {
			width: 100%;
			text-align: center;
		}
	}
</style>
