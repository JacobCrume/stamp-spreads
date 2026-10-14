<script lang="ts">
	import { onMount } from 'svelte';
	import { setSectionTheme } from '../../lib/theme.svelte';
	import FlavourPackFront from '../../lib/FlavourPackFront.svelte';
	import FlavourPackBack from '../../lib/FlavourPackBack.svelte';

	type FlavourId = 'butter' | 'raspberry' | 'yeast' | 'peanut';

	let activeFlavour = $state<FlavourId>('butter');
	let isFlipped = $state(false);

	function selectFlavour(id: FlavourId) {
		activeFlavour = id;
		setSectionTheme(id);
	}

	function toggleFlip() {
		isFlipped = !isFlipped;
	}

	onMount(() => {
		setSectionTheme('butter');
	});

	interface FlavourSpec {
		id: FlavourId;
		num: string;
		name: string;
		shortName: string;
		formulaRatio: string;
		ingredients: string;
		allergens: string;
		shelfLife: string;
		nip: {
			energy: string;
			fat: string;
			satFat: string;
			carbs: string;
			sugars: string;
			protein: string;
			sodium: string;
		};
	}

	const SPECS: Record<FlavourId, FlavourSpec> = {
		butter: {
			id: 'butter',
			num: '01',
			name: 'Salted Butter Spread',
			shortName: 'Butter',
			formulaRatio: '78 g butterfat to 2 g salt per 80 g sheet',
			ingredients: 'Cultured butterfat (milk), salt.',
			allergens: 'Contains Milk. Facility handles milk, gluten, peanuts.',
			shelfLife: '12 months ambient and unopened in pantry',
			nip: {
				energy: '361 kJ',
				fat: '9.8 g',
				satFat: '5.9 g',
				carbs: '0 g',
				sugars: '0 g',
				protein: '0 g',
				sodium: '98 mg'
			}
		},
		raspberry: {
			id: 'raspberry',
			num: '02',
			name: 'Raspberry Spread',
			shortName: 'Raspberry',
			formulaRatio: '150 g fruit input per 100 g finished spread',
			ingredients: 'Raspberries, caster sugar, lemon juice.',
			allergens: 'No declared allergens. Facility handles milk, gluten, peanuts.',
			shelfLife: '12 months ambient and unopened in pantry',
			nip: {
				energy: '93 kJ',
				fat: '0.1 g',
				satFat: '0 g',
				carbs: '4.6 g',
				sugars: '4.4 g',
				protein: '0.2 g',
				sodium: '<5 mg'
			}
		},
		yeast: {
			id: 'yeast',
			num: '03',
			name: 'Yeast Extract Spread',
			shortName: 'Yeast',
			formulaRatio: '80% yeast extract, 15.5% barley malt extract',
			ingredients: 'Yeast extract (80%), barley malt extract (15.5%), salt (2.5%), vegetable concentrate (2%).',
			allergens: 'Contains Gluten (barley). Facility handles milk, gluten, peanuts.',
			shelfLife: '12 months ambient and unopened in pantry',
			nip: {
				energy: '76 kJ',
				fat: '0 g',
				satFat: '0 g',
				carbs: '2.0 g',
				sugars: '1.0 g',
				protein: '2.3 g',
				sodium: '280 mg'
			}
		},
		peanut: {
			id: 'peanut',
			num: '04',
			name: 'Roasted Peanut Spread',
			shortName: 'Peanut',
			formulaRatio: '96% roasted peanuts with 2.3% vegetable stabilizer',
			ingredients: 'Roasted peanuts (96%), vegetable fat (2.3%), salt (1.7%).',
			allergens: 'Contains Peanuts. Facility handles milk, gluten, peanuts.',
			shelfLife: '12 months ambient and unopened in pantry',
			nip: {
				energy: '247 kJ',
				fat: '4.6 g',
				satFat: '0.7 g',
				carbs: '1.5 g',
				sugars: '0.5 g',
				protein: '2.6 g',
				sodium: '67 mg'
			}
		}
	};

	let current = $derived(SPECS[activeFlavour]);
</script>

<svelte:head>
	<title>Specifications — STAMP</title>
	<meta
		name="description"
		content="Industrial specifications, ingredients, allergens, and nutritional information for Stamp spreads."
	/>
</svelte:head>

<div class="specs-page">
	<div class="specs-container">
		<!-- HEADER WITH CLEAN FLUID SELECTOR -->
		<header class="specs-header">
			<div class="header-titles">
				<h1 class="title">SPECIFICATIONS</h1>
				<p class="subtitle">
					80 g sheet · 8 × 10 g discs · $5.00 NZD · 12-month ambient shelf life
				</p>
			</div>

			<!-- CLEAN FLUID TAB BAR WITHOUT RANDOM DOTS -->
			<nav class="flavour-tabs" aria-label="Select Flavour">
				{#each (['butter', 'raspberry', 'yeast', 'peanut'] as const) as fid}
					<button
						type="button"
						class="tab-btn"
						class:active={activeFlavour === fid}
						onclick={() => selectFlavour(fid)}
					>
						{SPECS[fid].shortName}
					</button>
				{/each}
			</nav>
		</header>

		<!-- CRISP 2-COLUMN GRID ALIGNED TO STRICT BASELINE -->
		<div class="specs-main-grid">
			<!-- LEFT COLUMN: PACK VIEWER WITH ROUND ICON FLIP BUTTON -->
			<div class="pack-panel">
				<div class="pack-stage">
					<div class="pack-card" class:flipped={isFlipped}>
						<div class="pack-face front">
							<FlavourPackFront flavour={activeFlavour} />
						</div>
						<div class="pack-face back">
							<FlavourPackBack flavour={activeFlavour} />
						</div>
					</div>
				</div>

				<!-- Simple Round Icon Flip Button (Matches Main Page) -->
				<button
					type="button"
					class="round-flip-btn"
					class:is-flipped={isFlipped}
					onclick={toggleFlip}
					aria-label={isFlipped ? 'Flip to pack front' : 'Flip to pack back (nutrition & ingredients)'}
					title={isFlipped ? 'Flip to front' : 'Flip to back ingredients'}
				>
					<svg class="flip-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<path d="M21 2v6h-6"></path>
						<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
						<path d="M3 22v-6h6"></path>
						<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
					</svg>
				</button>
			</div>

			<!-- RIGHT COLUMN: ALIGNED TECHNICAL SPECIFICATION GRID -->
			<div class="data-panel">
				<!-- FLAVOUR IDENTITY -->
				<div class="data-identity">
					<div class="identity-top">
						<span class="flavour-index">0{current.num.slice(-1)} / 04</span>
					</div>
					<h2 class="flavour-title">{current.name}</h2>
					<p class="formula-line">{current.formulaRatio}</p>
				</div>

				<!-- TECHNICAL PARAMETERS GRID -->
				<div class="tech-grid">
					<div class="grid-card">
						<span class="card-label">Ingredients</span>
						<p class="card-val">{current.ingredients}</p>
					</div>

					<div class="grid-card">
						<span class="card-label">Allergens</span>
						<p class="card-val"><strong>{current.allergens}</strong></p>
					</div>

					<div class="grid-card">
						<span class="card-label">Stability</span>
						<p class="card-val">{current.shelfLife}</p>
					</div>

					<div class="grid-card">
						<span class="card-label">Standard</span>
						<p class="card-val">FSANZ compliant. No therapeutic or false organic claims.</p>
					</div>
				</div>

				<!-- NIP GRID (7-CELL BALANCED ROW) -->
				<div class="nip-grid-panel">
					<div class="nip-header">
						<span class="nip-heading">NIP — Per 10 g Disc</span>
						<span class="nip-metric">1 Toast Serve</span>
					</div>

					<div class="nip-row">
						<div class="nip-item">
							<span class="nip-val">{current.nip.energy}</span>
							<span class="nip-tag">Energy</span>
						</div>
						<div class="nip-item">
							<span class="nip-val">{current.nip.fat}</span>
							<span class="nip-tag">Fat</span>
						</div>
						<div class="nip-item">
							<span class="nip-val">{current.nip.satFat}</span>
							<span class="nip-tag">Sat Fat</span>
						</div>
						<div class="nip-item">
							<span class="nip-val">{current.nip.carbs}</span>
							<span class="nip-tag">Carbs</span>
						</div>
						<div class="nip-item">
							<span class="nip-val">{current.nip.sugars}</span>
							<span class="nip-tag">Sugars</span>
						</div>
						<div class="nip-item">
							<span class="nip-val">{current.nip.protein}</span>
							<span class="nip-tag">Protein</span>
						</div>
						<div class="nip-item">
							<span class="nip-val">{current.nip.sodium}</span>
							<span class="nip-tag">Sodium</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	.specs-page {
		min-height: calc(100vh - 120px);
		background: transparent;
		color: #ffffff;
		padding-top: 7rem;
		padding-bottom: 4rem;
		display: flex;
		flex-direction: column;
		justify-content: center;
		font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}

	.specs-container {
		max-width: 1060px;
		width: 100%;
		margin: 0 auto;
		padding: 0 1.5rem;
	}

	/* HEADER */
	.specs-header {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		margin-bottom: 2.75rem;
		gap: 1.25rem;
	}

	.title {
		font-size: clamp(2.4rem, 5vw, 3.4rem);
		font-weight: 900;
		color: var(--color-primary);
		letter-spacing: -0.03em;
		line-height: 1;
		margin: 0 0 0.45rem;
	}

	.subtitle {
		font-size: 0.95rem;
		font-weight: 700;
		color: #ffffff;
		opacity: 0.85;
		margin: 0;
	}

	/* TABS WITHOUT RANDOM DOTS */
	.flavour-tabs {
		display: inline-flex;
		padding: 0.35rem;
		background: var(--color-tertiary);
		border-radius: 9999px;
		gap: 0.25rem;
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
		transition: background-color 0.45s ease;
	}

	.tab-btn {
		background: transparent;
		border: none;
		border-radius: 9999px;
		padding: 0.6rem 1.6rem;
		cursor: pointer;
		font-family: inherit;
		font-size: 0.92rem;
		font-weight: 800;
		color: #ffffff;
		transition: background-color 0.2s ease, color 0.2s ease, transform 0.15s ease;
	}

	.tab-btn:hover {
		transform: scale(1.02);
	}

	.tab-btn.active {
		background: var(--color-primary);
		color: var(--color-tertiary);
		box-shadow: 0 3px 12px rgba(0, 0, 0, 0.25);
	}

	/* 2-COLUMN MAIN GRID */
	.specs-main-grid {
		display: grid;
		grid-template-columns: 360px 1fr;
		gap: 3.5rem;
		align-items: center;
	}

	/* PACK PANEL */
	.pack-panel {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.25rem;
	}

	.pack-stage {
		width: 100%;
		max-width: 340px;
		height: 453px;
		perspective: 1200px;
	}

	.pack-card {
		width: 100%;
		height: 100%;
		position: relative;
		transform-style: preserve-3d;
		transition: transform 0.65s cubic-bezier(0.2, 0.9, 0.3, 1.2);
	}

	.pack-card.flipped {
		transform: translateY(-8px) rotateY(180deg);
	}

	.pack-face {
		position: absolute;
		inset: 0;
		backface-visibility: hidden;
		-webkit-backface-visibility: hidden;
		border-radius: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		filter: drop-shadow(0 16px 36px rgba(0, 0, 0, 0.3));
	}

	.pack-face.back {
		transform: rotateY(180deg);
	}

	/* SIMPLE ROUND ICON FLIP BUTTON */
	.round-flip-btn {
		width: 54px;
		height: 54px;
		border-radius: 50%;
		border: none;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		background: var(--color-tertiary);
		color: var(--color-primary);
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
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
		width: 25px;
		height: 25px;
		transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	.round-flip-btn.is-flipped .flip-svg {
		transform: rotate(180deg);
	}

	/* DATA PANEL */
	.data-panel {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	/* IDENTITY HEADER */
	.data-identity {
		border-bottom: 2px solid var(--color-primary);
		padding-bottom: 1.15rem;
		transition: border-color 0.45s ease;
	}

	.identity-top {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 0.3rem;
	}

	.flavour-index {
		font-size: 0.82rem;
		font-weight: 900;
		letter-spacing: 0.14em;
		color: var(--color-primary);
	}

	.flavour-title {
		font-size: clamp(2rem, 3.8vw, 2.7rem);
		font-weight: 900;
		color: var(--color-primary);
		letter-spacing: -0.03em;
		margin: 0.15rem 0 0.4rem;
		line-height: 1;
	}

	.formula-line {
		font-size: 1rem;
		font-weight: 600;
		color: #ffffff;
		opacity: 0.95;
		margin: 0;
	}

	/* 4-CELL TECHNICAL GRID */
	.tech-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
	}

	.grid-card {
		background: var(--color-tertiary);
		border-radius: 16px;
		padding: 1.2rem 1.4rem;
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
		transition: background-color 0.45s ease;
	}

	.card-label {
		font-size: 0.72rem;
		font-weight: 900;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--color-primary);
		opacity: 0.9;
	}

	.card-val {
		font-size: 0.92rem;
		font-weight: 600;
		color: #ffffff;
		line-height: 1.45;
		margin: 0;
	}

	/* NIP PANEL */
	.nip-grid-panel {
		background: var(--color-tertiary);
		border-radius: 16px;
		padding: 1.25rem 1.4rem;
		display: flex;
		flex-direction: column;
		gap: 0.85rem;
		transition: background-color 0.45s ease;
	}

	.nip-header {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
	}

	.nip-heading {
		font-size: 0.75rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--color-primary);
	}

	.nip-metric {
		font-size: 0.72rem;
		font-weight: 700;
		color: #ffffff;
		opacity: 0.75;
	}

	.nip-row {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		gap: 0.5rem;
	}

	.nip-item {
		background: rgba(0, 0, 0, 0.22);
		border-radius: 10px;
		padding: 0.65rem 0.35rem;
		text-align: center;
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
	}

	.nip-val {
		font-size: 0.88rem;
		font-weight: 900;
		color: #ffffff;
		line-height: 1.1;
	}

	.nip-tag {
		font-size: 0.64rem;
		font-weight: 800;
		text-transform: uppercase;
		color: var(--color-primary);
		letter-spacing: 0.03em;
	}

	/* RESPONSIVE LAYOUT */
	@media (max-width: 860px) {
		.specs-main-grid {
			grid-template-columns: 1fr;
			gap: 2.5rem;
		}

		.pack-panel {
			margin: 0 auto;
		}

		.nip-row {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	@media (max-width: 600px) {
		.specs-header {
			margin-bottom: 2rem;
			gap: 1rem;
		}

		.flavour-tabs {
			width: 100%;
			justify-content: center;
		}

		.tab-btn {
			padding: 0.5rem 1rem;
			font-size: 0.82rem;
		}

		.pack-stage {
			max-width: 280px;
			height: 373px;
		}

		.tech-grid {
			grid-template-columns: 1fr;
		}

		.nip-row {
			grid-template-columns: repeat(3, 1fr);
		}
	}
</style>
