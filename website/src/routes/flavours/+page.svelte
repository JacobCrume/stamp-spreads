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
		headline: string;
		ingredients: string;
		allergens: string;
		shelfLife: string;
		nip: {
			energy: string;
			protein: string;
			fat: string;
			satFat: string;
			carbs: string;
			sugars: string;
			sodium: string;
		};
	}

	const SPECS: Record<FlavourId, FlavourSpec> = {
		butter: {
			id: 'butter',
			num: '01',
			name: 'Salted Butter',
			shortName: 'Butter',
			headline: 'Cultured butterfat (78 g) and sea salt (2 g). Low moisture formulation for 12-month ambient stability.',
			ingredients: 'Cultured butterfat (milk), salt.',
			allergens: 'Contains Milk. Produced in a facility handling milk, gluten, and peanuts.',
			shelfLife: '12 months ambient and unopened in pantry.',
			nip: {
				energy: '361 kJ',
				protein: '0 g',
				fat: '9.8 g',
				satFat: '5.9 g',
				carbs: '0 g',
				sugars: '0 g',
				sodium: '98 mg'
			}
		},
		raspberry: {
			id: 'raspberry',
			num: '02',
			name: 'Raspberry',
			shortName: 'Raspberry',
			headline: 'Slow steam reduction made with 150 g whole raspberries per 100 g finished spread.',
			ingredients: 'Raspberries, caster sugar, lemon juice.',
			allergens: 'No declared allergens. Produced in a facility handling milk, gluten, and peanuts.',
			shelfLife: '12 months ambient and unopened in pantry.',
			nip: {
				energy: '93 kJ',
				protein: '0.2 g',
				fat: '0.1 g',
				satFat: '0 g',
				carbs: '4.6 g',
				sugars: '4.4 g',
				sodium: '<5 mg'
			}
		},
		yeast: {
			id: 'yeast',
			num: '03',
			name: 'Yeast Extract',
			shortName: 'Yeast',
			headline: 'Proprietary New Zealand savory recipe. 80% yeast extract with roasted barley malt.',
			ingredients: 'Yeast extract (80%), barley malt extract (15.5%), salt (2.5%), vegetable concentrate (2%).',
			allergens: 'Contains Gluten (barley). Produced in a facility handling milk, gluten, and peanuts.',
			shelfLife: '12 months ambient and unopened in pantry.',
			nip: {
				energy: '76 kJ',
				protein: '2.3 g',
				fat: '0 g',
				satFat: '0 g',
				carbs: '2.0 g',
				sugars: '1.0 g',
				sodium: '280 mg'
			}
		},
		peanut: {
			id: 'peanut',
			num: '04',
			name: 'Roasted Peanut',
			shortName: 'Peanut',
			headline: '96% high-roast peanuts with 2.3% vegetable fat to permanently eliminate oil separation.',
			ingredients: 'Peanuts (96%), vegetable fat (2.3%), salt (1.7%).',
			allergens: 'Contains Peanuts. Produced in a facility handling milk, gluten, and peanuts.',
			shelfLife: '12 months ambient and unopened in pantry.',
			nip: {
				energy: '247 kJ',
				protein: '2.6 g',
				fat: '4.6 g',
				satFat: '0.7 g',
				carbs: '1.5 g',
				sugars: '0.5 g',
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

<div class="specs-clean-page">
	<!-- MINIMAL CLEAN HEADER -->
	<header class="specs-top">
		<div class="specs-top-inner">
			<h1 class="specs-title">SPECIFICATIONS</h1>
			<p class="specs-meta">
				80 g sheet · 8 × 10 g discs · $5.00 NZD ($6.25 / 100 g) · 12-month ambient shelf life
			</p>

			<!-- 4-TAB SELECTOR -->
			<nav class="specs-tabs" aria-label="Select Flavour">
				{#each (['butter', 'raspberry', 'yeast', 'peanut'] as const) as fid}
					<button
						type="button"
						class="tab-btn"
						class:active={activeFlavour === fid}
						onclick={() => selectFlavour(fid)}
					>
						<span class="tab-dot" class:active={activeFlavour === fid}></span>
						<span>{SPECS[fid].shortName}</span>
					</button>
				{/each}
			</nav>
		</div>
	</header>

	<!-- FOCUSED SPEC CONTENT -->
	<main class="specs-content-wrap">
		<div class="specs-grid">
			<!-- LEFT: PACK VIEW (FRONT & BACK WITH QUICK TOGGLE) -->
			<div class="pack-col">
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

				<button
					type="button"
					class="flip-pill-btn"
					onclick={toggleFlip}
					aria-label={isFlipped ? 'View pack front' : 'View pack back and nutrition panel'}
				>
					<svg class="flip-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
						<path d="M21 2v6h-6"></path>
						<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
						<path d="M3 22v-6h6"></path>
						<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
					</svg>
					<span>{isFlipped ? 'Show Pack Front' : 'Show NIP & Back'}</span>
				</button>
			</div>

			<!-- RIGHT: CONCISE TECHNICAL DATA -->
			<div class="data-col">
				<div class="flavour-heading-block">
					<span class="flavour-num">{current.num}</span>
					<h2 class="flavour-name">{current.name}</h2>
					<p class="flavour-summary">{current.headline}</p>
				</div>

				<!-- SPECS LIST -->
				<div class="tech-specs-card">
					<div class="spec-row">
						<span class="spec-term">Ingredients</span>
						<span class="spec-desc">{current.ingredients}</span>
					</div>

					<div class="spec-row">
						<span class="spec-term">Allergen Notice</span>
						<span class="spec-desc"><strong>{current.allergens}</strong></span>
					</div>

					<div class="spec-row">
						<span class="spec-term">Shelf Stability</span>
						<span class="spec-desc">{current.shelfLife}</span>
					</div>
				</div>

				<!-- NUTRITION PER 10G SERVE -->
				<div class="nip-summary-card">
					<div class="nip-card-header">
						<span class="nip-label">Nutrition per 10 g Disc</span>
						<span class="nip-sub">1 serving</span>
					</div>

					<div class="nip-inline-grid">
						<div class="nip-cell">
							<span class="nip-val">{current.nip.energy}</span>
							<span class="nip-key">Energy</span>
						</div>
						<div class="nip-cell">
							<span class="nip-val">{current.nip.fat}</span>
							<span class="nip-key">Fat (tot)</span>
						</div>
						<div class="nip-cell">
							<span class="nip-val">{current.nip.satFat}</span>
							<span class="nip-key">Sat Fat</span>
						</div>
						<div class="nip-cell">
							<span class="nip-val">{current.nip.carbs}</span>
							<span class="nip-key">Carbs</span>
						</div>
						<div class="nip-cell">
							<span class="nip-val">{current.nip.sugars}</span>
							<span class="nip-key">Sugars</span>
						</div>
						<div class="nip-cell">
							<span class="nip-val">{current.nip.protein}</span>
							<span class="nip-key">Protein</span>
						</div>
						<div class="nip-cell">
							<span class="nip-val">{current.nip.sodium}</span>
							<span class="nip-key">Sodium</span>
						</div>
					</div>
				</div>

				<!-- MINIMAL COMPLIANCE & MIXED PACK LINE -->
				<div class="specs-foot-note">
					<p>
						Also available in the <strong>Mixed Sheet</strong> (2× Butter, 2× Raspberry, 2× Yeast, 2× Peanut) for $5.00 NZD. Contains milk, gluten, and peanuts. All Stamp products comply with the NZ Food Standards Code; no therapeutic or medicinal claims made.
					</p>
				</div>
			</div>
		</div>
	</main>
</div>

<style>
	.specs-clean-page {
		min-height: 100vh;
		background: transparent;
		color: #ffffff;
		padding-top: 5.5rem;
		padding-bottom: 3rem;
		font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}

	/* TOP SECTION */
	.specs-top {
		padding: 2.5rem 1.5rem 2rem;
		text-align: center;
	}

	.specs-top-inner {
		max-width: 800px;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.specs-title {
		font-size: clamp(2.4rem, 5vw, 3.6rem);
		font-weight: 900;
		color: var(--color-primary);
		letter-spacing: -0.03em;
		margin: 0 0 0.5rem;
		line-height: 1;
	}

	.specs-meta {
		font-size: 0.95rem;
		font-weight: 700;
		color: #ffffff;
		opacity: 0.85;
		margin: 0 0 1.75rem;
	}

	/* 4 TABS */
	.specs-tabs {
		display: inline-flex;
		gap: 0.4rem;
		padding: 0.35rem;
		background: var(--color-tertiary);
		border-radius: 9999px;
		transition: background-color 0.45s ease;
	}

	.tab-btn {
		background: transparent;
		border: none;
		border-radius: 9999px;
		padding: 0.55rem 1.3rem;
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		font-family: inherit;
		font-size: 0.9rem;
		font-weight: 800;
		color: #ffffff;
		transition: background-color 0.2s, transform 0.15s, color 0.2s;
	}

	.tab-btn:hover {
		transform: scale(1.03);
	}

	.tab-btn.active {
		background: var(--color-primary);
		color: var(--color-tertiary);
	}

	.tab-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--color-primary);
	}

	.tab-btn.active .tab-dot {
		background: var(--color-tertiary);
	}

	/* MAIN CONTENT */
	.specs-content-wrap {
		max-width: 1040px;
		margin: 0 auto;
		padding: 1.5rem 1.5rem 3rem;
	}

	.specs-grid {
		display: grid;
		grid-template-columns: 360px 1fr;
		gap: 3.5rem;
		align-items: flex-start;
	}

	/* PACK COLUMN */
	.pack-col {
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

	.flip-pill-btn {
		background: var(--color-tertiary);
		color: var(--color-primary);
		border: none;
		border-radius: 9999px;
		padding: 0.6rem 1.25rem;
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		gap: 0.6rem;
		font-family: inherit;
		font-size: 0.85rem;
		font-weight: 800;
		box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
		transition: transform 0.15s, background-color 0.45s ease, color 0.45s ease;
	}

	.flip-pill-btn:hover {
		transform: scale(1.05);
	}

	.flip-icon {
		width: 18px;
		height: 18px;
	}

	/* DATA COLUMN */
	.data-col {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.flavour-heading-block {
		border-bottom: 2px solid var(--color-primary);
		padding-bottom: 1.2rem;
		transition: border-color 0.45s ease;
	}

	.flavour-num {
		font-size: 0.85rem;
		font-weight: 900;
		letter-spacing: 0.14em;
		color: var(--color-primary);
	}

	.flavour-name {
		font-size: clamp(2rem, 4vw, 2.8rem);
		font-weight: 900;
		color: var(--color-primary);
		letter-spacing: -0.03em;
		margin: 0.2rem 0 0.5rem;
		line-height: 1;
	}

	.flavour-summary {
		font-size: 1.05rem;
		color: #ffffff;
		line-height: 1.5;
		margin: 0;
		opacity: 0.95;
	}

	/* TECH SPECS CARD */
	.tech-specs-card {
		background: var(--color-tertiary);
		border-radius: 20px;
		padding: 1.5rem 1.75rem;
		display: flex;
		flex-direction: column;
		gap: 1.15rem;
		transition: background-color 0.45s ease;
	}

	.spec-row {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.spec-term {
		font-size: 0.72rem;
		font-weight: 900;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--color-primary);
		opacity: 0.9;
	}

	.spec-desc {
		font-size: 0.95rem;
		color: #ffffff;
		line-height: 1.45;
	}

	/* NUTRITION INLINE CARD */
	.nip-summary-card {
		background: var(--color-tertiary);
		border-radius: 20px;
		padding: 1.4rem 1.75rem;
		display: flex;
		flex-direction: column;
		gap: 0.9rem;
		transition: background-color 0.45s ease;
	}

	.nip-card-header {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
	}

	.nip-label {
		font-size: 0.78rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--color-primary);
	}

	.nip-sub {
		font-size: 0.75rem;
		font-weight: 700;
		color: #ffffff;
		opacity: 0.75;
	}

	.nip-inline-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(68px, 1fr));
		gap: 0.5rem;
	}

	.nip-cell {
		background: rgba(0, 0, 0, 0.22);
		border-radius: 12px;
		padding: 0.75rem 0.5rem;
		text-align: center;
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
	}

	.nip-val {
		font-size: 0.95rem;
		font-weight: 900;
		color: #ffffff;
	}

	.nip-key {
		font-size: 0.68rem;
		font-weight: 800;
		text-transform: uppercase;
		color: var(--color-primary);
		letter-spacing: 0.04em;
	}

	/* FOOT NOTE */
	.specs-foot-note {
		padding: 0.5rem 0.25rem;
		font-size: 0.85rem;
		line-height: 1.5;
		color: #ffffff;
		opacity: 0.75;
	}

	.specs-foot-note strong {
		color: var(--color-primary);
	}

	/* RESPONSIVE */
	@media (max-width: 860px) {
		.specs-grid {
			grid-template-columns: 1fr;
			gap: 2.5rem;
		}

		.pack-col {
			margin: 0 auto;
		}

		.nip-inline-grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	@media (max-width: 600px) {
		.specs-top {
			padding: 1.5rem 1rem;
		}

		.specs-tabs {
			width: 100%;
			justify-content: center;
		}

		.tab-btn {
			padding: 0.45rem 0.85rem;
			font-size: 0.82rem;
		}

		.pack-stage {
			max-width: 280px;
			height: 373px;
		}

		.nip-inline-grid {
			grid-template-columns: repeat(3, 1fr);
		}
	}
</style>
