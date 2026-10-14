<script lang="ts">
	import { onMount } from 'svelte';
	import { setSectionTheme, type SectionTheme } from '../../lib/theme.svelte';
	import FlavourPackFront from '../../lib/FlavourPackFront.svelte';
	import FlavourPackBack from '../../lib/FlavourPackBack.svelte';

	type FlavourId = 'butter' | 'raspberry' | 'yeast' | 'peanut';

	let activeFlavour = $state<FlavourId>('butter');
	let flipped = $state<Record<FlavourId, boolean>>({
		butter: false,
		raspberry: false,
		yeast: false,
		peanut: false
	});

	function toggleFlip(id: FlavourId) {
		flipped[id] = !flipped[id];
	}

	function selectFlavour(id: FlavourId) {
		activeFlavour = id;
		setSectionTheme(id);
	}

	onMount(() => {
		// Set initial theme to butter
		setSectionTheme('butter');
	});

	interface FlavourDetail {
		id: FlavourId;
		num: string;
		name: string;
		tagline: string;
		netWeight: string;
		price: string;
		unitCost: string;
		shelfLife: string;
		portion: string;
		tasteProfile: string;
		formula: string;
		formulaDetail: string;
		allergens: string;
		allergenBadge: string;
		facilityStatement: string;
		complianceNotice: string;
		packHighlights: string[];
		nutrition: {
			perServe: { energy: string; protein: string; fat: string; satFat: string; carbs: string; sugars: string; sodium: string };
			per100g: { energy: string; protein: string; fat: string; satFat: string; carbs: string; sugars: string; sodium: string };
		};
	}

	const FLAVOUR_DETAILS: Record<FlavourId, FlavourDetail> = {
		butter: {
			id: 'butter',
			num: '01',
			name: 'Salted Butter Spread',
			tagline: 'Cultured dairy spread formulated with 2.5% salt balance for immediate toast melt',
			netWeight: '80 g (8 × 10 g peel-and-press discs)',
			price: '$5.00 NZD',
			unitCost: '$6.25 per 100 g ($0.625 / disc)',
			shelfLife: '12 months ambient and unopened in pantry',
			portion: '10 g single-serve disc (1 toast slice)',
			tasteProfile:
				'Rich, clean cultured butterfat with a measured 2.5% sea salt finish. Softens into toast grooves within 3 seconds without tearing the crumb.',
			formula: 'Cultured butterfat and salt (78 g fat to 2 g salt per 80 g pack)',
			formulaDetail:
				'Formulated with low free-moisture to ensure ambient shelf stability over 12 months without refrigeration. Zero added vegetable oils, palm oils, or artificial preservatives.',
			allergens: 'Contains Milk.',
			allergenBadge: 'DAIRY ALLERGEN',
			facilityStatement: 'Produced in an audited facility handling milk, gluten, and peanuts.',
			complianceNotice:
				'Classified and sold legally as an ambient "butter spread", not chilled table butter. Strictly no therapeutic or false organic claims.',
			packHighlights: ['Cultured Dairy Integrity', 'Zero Knife or Jar Wash-up', 'Instant Hot Toast Melt', 'Pantry Stable for 12 Months'],
			nutrition: {
				perServe: { energy: '361 kJ', protein: '0 g', fat: '9.8 g', satFat: '5.9 g', carbs: '0 g', sugars: '0 g', sodium: '98 mg' },
				per100g: { energy: '3610 kJ', protein: '0 g', fat: '97.5 g', satFat: '58.8 g', carbs: '0 g', sugars: '0 g', sodium: '982 mg' }
			}
		},
		raspberry: {
			id: 'raspberry',
			num: '02',
			name: 'Slow-Cooked Raspberry',
			tagline: 'Concentrated whole-fruit paste cooked down with 150 g raspberries per 100 g',
			netWeight: '80 g (8 × 10 g peel-and-press discs)',
			price: '$5.00 NZD',
			unitCost: '$6.25 per 100 g ($0.625 / disc)',
			shelfLife: '12 months ambient and unopened in pantry',
			portion: '10 g single-serve disc (1 toast slice)',
			tasteProfile:
				'Vibrant, ruby-red whole fruit with a sharp, refreshing berry punch balanced by clean sugar and fresh lemon brightness.',
			formula: 'Whole raspberries, caster sugar, and lemon juice (150 g fruit input / 100 g output)',
			formulaDetail:
				'Natural fruit pectin and slow steam jacket reduction achieve thick disc firmness without artificial gelling agents or synthetic colors.',
			allergens: 'No major declared food allergens in recipe.',
			allergenBadge: 'NO RECIPE ALLERGENS',
			facilityStatement: 'Produced in an audited facility handling milk, gluten, and peanuts.',
			complianceNotice:
				'Traditional fruit spread formula. Contains natural fruit sugars and caster sugar; no low-sugar, dietetic, or organic certification claims made.',
			packHighlights: ['150 g Real Fruit per 100 g', 'No Added Gelatine or Gums', 'Bright Lemon Balanced', 'Pantry Stable for 12 Months'],
			nutrition: {
				perServe: { energy: '93 kJ', protein: '0.2 g', fat: '0.1 g', satFat: '0 g', carbs: '4.6 g', sugars: '4.4 g', sodium: '<5 mg' },
				per100g: { energy: '929 kJ', protein: '1.8 g', fat: '1.0 g', satFat: '0 g', carbs: '46.1 g', sugars: '44.3 g', sodium: '<5 mg' }
			}
		},
		yeast: {
			id: 'yeast',
			num: '03',
			name: 'Yeast Extract Spread',
			tagline: 'Deep savory umami spread with roasted barley malt and a sharp, clean finish',
			netWeight: '80 g (8 × 10 g peel-and-press discs)',
			price: '$5.00 NZD',
			unitCost: '$6.25 per 100 g ($0.625 / disc)',
			shelfLife: '12 months ambient and unopened in pantry',
			portion: '10 g single-serve disc (1 toast slice)',
			tasteProfile:
				'Bold, salty, roasted umami explosion with deep toasted malt undertones and a lingering savory finish. Perfectly portioned so you never overspread.',
			formula: 'Yeast extract 80%, barley malt extract 15.5%, salt 2.5%, vegetable concentrate 2%',
			formulaDetail:
				'Proprietary New Zealand savory paste recipe. Controlled sodium and high-density solids yield effortless release from backing film onto steaming buttered toast.',
			allergens: 'Contains Gluten (from barley malt).',
			allergenBadge: 'CONTAINS GLUTEN',
			facilityStatement: 'Produced in an audited facility handling milk, gluten, and peanuts.',
			complianceNotice:
				'NOT gluten-free. Contains barley malt extract. Strictly zero health, medicinal, or vitamin curative claims.',
			packHighlights: ['Proprietary NZ Recipe', 'Precise 10 g Toast Portion', 'Deep Roasted Umami', 'Pantry Stable for 12 Months'],
			nutrition: {
				perServe: { energy: '76 kJ', protein: '2.3 g', fat: '0 g', satFat: '0 g', carbs: '2.0 g', sugars: '1.0 g', sodium: '280 mg' },
				per100g: { energy: '755 kJ', protein: '23.0 g', fat: '0.4 g', satFat: '0.1 g', carbs: '19.6 g', sugars: '10.0 g', sodium: '2803 mg' }
			}
		},
		peanut: {
			id: 'peanut',
			num: '04',
			name: 'Roasted Peanut Spread',
			tagline: '96% high-roast peanuts with natural vegetable fat to eliminate oil separation',
			netWeight: '80 g (8 × 10 g peel-and-press discs)',
			price: '$5.00 NZD',
			unitCost: '$6.25 per 100 g ($0.625 / disc)',
			shelfLife: '12 months ambient and unopened in pantry',
			portion: '10 g single-serve disc (1 toast slice)',
			tasteProfile:
				'Deep roasted aroma, full-bodied nutty savoriness, and a velvety smooth melt that glides across warm toast without clumping.',
			formula: 'Roasted peanuts 96%, hard vegetable fat 2.3%, sea salt 1.7%',
			formulaDetail:
				'The 2.3% vegetable fat structure prevents oil separation across 12 months at room temperature, eliminating sticky separation common in traditional peanut butter jars.',
			allergens: 'Contains Peanuts.',
			allergenBadge: 'PEANUT ALLERGEN',
			facilityStatement: 'Produced in an audited facility handling milk, gluten, and peanuts.',
			complianceNotice:
				'Formulated as an ambient portable portion spread. Does not claim to be low-fat, keto-certified, or a protein supplement.',
			packHighlights: ['96% Fresh Roasted Peanuts', 'Zero Oil Separation', 'Smooth Hot Toast Melt', 'Pantry Stable for 12 Months'],
			nutrition: {
				perServe: { energy: '247 kJ', protein: '2.6 g', fat: '4.6 g', satFat: '0.7 g', carbs: '1.5 g', sugars: '0.5 g', sodium: '67 mg' },
				per100g: { energy: '2470 kJ', protein: '25.8 g', fat: '46.5 g', satFat: '7.3 g', carbs: '15.0 g', sugars: '5.3 g', sodium: '668 mg' }
			}
		}
	};

	let current = $derived(FLAVOUR_DETAILS[activeFlavour]);
</script>

<svelte:head>
	<title>Flavours & Range Specifications — STAMP</title>
	<meta
		name="description"
		content="Complete product specifications for Stamp's four launch flavours: Salted Butter, Slow-Cooked Raspberry, Yeast Extract, and Roasted Peanut."
	/>
</svelte:head>

<div class="specs-page-root">
	<!-- HERO INTRO -->
	<header class="specs-hero">
		<div class="hero-inner">
			<div class="hero-kicker">FOUR FORMULAS · ZERO KNIFE · ZERO JARS</div>
			<h1 class="hero-title">THE RANGE & SPECS</h1>
			<p class="hero-lead">
				Engineered for direct thermal contact with hot toast. Every 80 g sheet delivers eight 10 g peel-and-press portions for <strong class="price-highlight">$5.00 NZD</strong> ($6.25 / 100 g), ambient pantry-stable for 12 months.
			</p>

			<!-- INTERACTIVE FLAVOUR PILL SELECTOR -->
			<nav class="flavour-selector-pills" aria-label="Select Flavour">
				{#each (['butter', 'raspberry', 'yeast', 'peanut'] as const) as fid}
					<button
						type="button"
						class="flavour-pill-btn"
						class:active={activeFlavour === fid}
						onclick={() => selectFlavour(fid)}
					>
						<span class="pill-dot" class:active={activeFlavour === fid}></span>
						<span class="pill-text">{FLAVOUR_DETAILS[fid].name.replace(' Spread', '')}</span>
					</button>
				{/each}
			</nav>
		</div>
	</header>

	<!-- MAIN INTERACTIVE SHOWCASE FOR CURRENT FLAVOUR -->
	<section class="flavour-showcase-stage" id="showcase">
		<div class="showcase-inner">
			<!-- LEFT: 3D CARD DISPLAY WITH FLIP BUTTON -->
			<div class="showcase-card-col">
				<div class="flip-stage">
					<div class="flip-card {flipped[activeFlavour] ? 'flipped' : ''}">
						<!-- Front of Pack -->
						<div class="flip-face flip-front">
							<FlavourPackFront flavour={activeFlavour} />
						</div>
						<!-- Back of Pack with full Nutritional Information Panel -->
						<div class="flip-face flip-back">
							<FlavourPackBack flavour={activeFlavour} />
						</div>
					</div>
				</div>

				<!-- Interactive Flip Action Button -->
				<button
					type="button"
					class="round-flip-btn"
					class:is-flipped={flipped[activeFlavour]}
					onclick={() => toggleFlip(activeFlavour)}
					aria-label={flipped[activeFlavour] ? 'Flip to pack front' : 'Flip to pack back (nutrition & ingredients)'}
					title={flipped[activeFlavour] ? 'Flip to front' : 'Flip to back ingredients panel'}
				>
					<svg class="flip-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<path d="M21 2v6h-6"></path>
						<path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
						<path d="M3 22v-6h6"></path>
						<path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
					</svg>
				</button>
				<span class="flip-hint-text">
					{flipped[activeFlavour] ? 'Showing Back Panel (NIP & Ingredients)' : 'Click to inspect Back Panel & NIP'}
				</span>
			</div>

			<!-- RIGHT: COMPREHENSIVE INDUSTRIAL SPECS -->
			<div class="showcase-details-col">
				<div class="flavour-header-row">
					<span class="flavour-kicker">{current.num} / FOUR LAUNCH FLAVOURS</span>
					<span class="allergen-pill">{current.allergenBadge}</span>
				</div>

				<h2 class="flavour-title">{current.name}</h2>
				<p class="flavour-tagline">{current.tagline}</p>

				<!-- QUICK HIGHLIGHT PILLS -->
				<div class="highlights-row">
					{#each current.packHighlights as h}
						<span class="highlight-chip">{h}</span>
					{/each}
				</div>

				<!-- 4-CELL SPEC GRID -->
				<div class="spec-matrix-grid">
					<div class="matrix-card">
						<span class="matrix-label">TASTE PROFILE</span>
						<p class="matrix-val">{current.tasteProfile}</p>
					</div>

					<div class="matrix-card">
						<span class="matrix-label">FORMULATION</span>
						<p class="matrix-val">{current.formula}</p>
						<span class="matrix-sub">{current.formulaDetail}</span>
					</div>

					<div class="matrix-card">
						<span class="matrix-label">PACK & PORTION</span>
						<p class="matrix-val">{current.netWeight}</p>
						<span class="matrix-sub">{current.unitCost} · Ambient for 12 months</span>
					</div>

					<div class="matrix-card">
						<span class="matrix-label">ALLERGENS & FACILITY</span>
						<p class="matrix-val"><strong>{current.allergens}</strong></p>
						<span class="matrix-sub">{current.facilityStatement}</span>
					</div>
				</div>

				<!-- NUTRITION TABLE ACCORDION/CARD -->
				<div class="nutrition-card">
					<div class="nutrition-title-row">
						<span class="nutrition-heading">NUTRITION INFORMATION PANEL (NIP)</span>
						<span class="nutrition-meta">Servings Per Sheet: 8 · Serving Size: 10 g</span>
					</div>

					<div class="nutrition-table-wrap">
						<table class="nip-table">
							<thead>
								<tr>
									<th class="col-nutrient">Nutrient</th>
									<th class="col-serve">Avg Qty per 10 g Serve</th>
									<th class="col-100g">Avg Qty per 100 g</th>
								</tr>
							</thead>
							<tbody>
								<tr>
									<td>Energy</td>
									<td>{current.nutrition.perServe.energy}</td>
									<td>{current.nutrition.per100g.energy}</td>
								</tr>
								<tr>
									<td>Protein</td>
									<td>{current.nutrition.perServe.protein}</td>
									<td>{current.nutrition.per100g.protein}</td>
								</tr>
								<tr>
									<td>Fat, total</td>
									<td>{current.nutrition.perServe.fat}</td>
									<td>{current.nutrition.per100g.fat}</td>
								</tr>
								<tr class="indent">
									<td>– saturated</td>
									<td>{current.nutrition.perServe.satFat}</td>
									<td>{current.nutrition.per100g.satFat}</td>
								</tr>
								<tr>
									<td>Carbohydrate</td>
									<td>{current.nutrition.perServe.carbs}</td>
									<td>{current.nutrition.per100g.carbs}</td>
								</tr>
								<tr class="indent">
									<td>– sugars</td>
									<td>{current.nutrition.perServe.sugars}</td>
									<td>{current.nutrition.per100g.sugars}</td>
								</tr>
								<tr>
									<td>Sodium</td>
									<td>{current.nutrition.perServe.sodium}</td>
									<td>{current.nutrition.per100g.sodium}</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>

				<!-- COMPLIANCE & INTEGRITY CALLOUT -->
				<div class="integrity-callout">
					<div class="integrity-icon">ℹ</div>
					<div class="integrity-text">
						<strong>Product Integrity Notice:</strong> {current.complianceNotice}
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- SECTION: THE POPULAR MIXED SHEET VARIANT -->
	<section class="mixed-sheet-showcase">
		<div class="mixed-sheet-inner">
			<div class="mixed-text-side">
				<span class="mixed-badge">POPULAR LAUNCH SELECTION</span>
				<h2 class="mixed-title">The Mixed Sheet</h2>
				<p class="mixed-lead">
					Can't choose between sweet and savory? The Mixed Sheet delivers two 10 g discs of each launch flavour on a single 80 g release sheet for the exact same <strong>$5.00 NZD</strong> shelf price.
				</p>

				<div class="mixed-flavours-strip">
					<div class="mini-strip-item">
						<span class="strip-dot" style:background="#ffd640"></span>
						<strong>2× Salted Butter</strong>
					</div>
					<div class="mini-strip-item">
						<span class="strip-dot" style:background="#ff467a"></span>
						<strong>2× Raspberry</strong>
					</div>
					<div class="mini-strip-item">
						<span class="strip-dot" style:background="#e24bff"></span>
						<strong>2× Yeast Extract</strong>
					</div>
					<div class="mini-strip-item">
						<span class="strip-dot" style:background="#ff8c30"></span>
						<strong>2× Peanut</strong>
					</div>
				</div>

				<div class="mixed-notice">
					<strong>Allergen Warning:</strong> Because all four varieties are packaged on the same sheet, the Mixed Sheet contains <strong>Milk, Gluten (barley), and Peanuts</strong>.
				</div>
			</div>

			<div class="mixed-price-side">
				<div class="price-bubble">
					<span class="price-val">$5.00</span>
					<span class="price-unit">NZD / Sheet</span>
					<div class="price-divider"></div>
					<span class="price-stats">8 Stamps · 80 g Total</span>
					<span class="price-sub">$6.25 per 100 g</span>
				</div>
			</div>
		</div>
	</section>

	<!-- SECTION: COMMERCIAL & REGULATORY COMPLIANCE -->
	<section class="compliance-section">
		<div class="compliance-inner">
			<div class="compliance-header">
				<div class="compliance-kicker">FAIR TRADING & FOOD SAFETY</div>
				<h3 class="compliance-title">Transparent Food Labeling Standard</h3>
				<p class="compliance-sub">
					Stamp strictly observes New Zealand Food Standards Code and fair commercial marketing regulations across all print and digital touchpoints.
				</p>
			</div>

			<div class="compliance-grid">
				<div class="compliance-card">
					<h4 class="card-heading">Zero Therapeutic Claims</h4>
					<p class="card-text">
						Stamp is a convenient breakfast food spread, not medicine or a health treatment. We make no therapeutic or curative claims regarding vitamins, vitality, or medical health.
					</p>
				</div>

				<div class="compliance-card">
					<h4 class="card-heading">Accurate Allergen Declarations</h4>
					<p class="card-text">
						We do not claim 'gluten-free' status because our Yeast Extract contains barley malt gluten. Every pack clearly prints bold allergen statements and audited facility declarations.
					</p>
				</div>

				<div class="compliance-card">
					<h4 class="card-heading">Honest Standard of Identity</h4>
					<p class="card-text">
						Salted Butter uses the descriptor "spread" because it is a shelf-stable cultured dairy formulation designed for ambient pantry storage, not a refrigerated table butter pat.
					</p>
				</div>
			</div>
		</div>
	</section>
</div>

<style>
	/* SPECS PAGE ROOT */
	.specs-page-root {
		width: 100%;
		min-height: 100vh;
		background: transparent;
		color: #ffffff;
		padding-top: 5.5rem;
		padding-bottom: 2rem;
		font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}

	/* HERO */
	.specs-hero {
		padding: 3rem 1.5rem 2.5rem;
		text-align: center;
	}

	.hero-inner {
		max-width: 860px;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.hero-kicker {
		font-size: 0.85rem;
		font-weight: 900;
		letter-spacing: 0.16em;
		color: var(--color-primary);
		margin-bottom: 0.5rem;
	}

	.hero-title {
		font-size: clamp(2.6rem, 5.5vw, 4.2rem);
		font-weight: 900;
		color: var(--color-primary);
		letter-spacing: -0.03em;
		line-height: 1;
		margin-bottom: 1.25rem;
	}

	.hero-lead {
		font-size: 1.15rem;
		line-height: 1.6;
		color: #ffffff;
		opacity: 0.95;
		max-width: 700px;
		margin-bottom: 2.25rem;
	}

	.price-highlight {
		color: var(--color-primary);
	}

	/* INTERACTIVE PILL SELECTOR */
	.flavour-selector-pills {
		display: flex;
		gap: 0.75rem;
		flex-wrap: wrap;
		justify-content: center;
		padding: 0.4rem;
		background: var(--color-tertiary);
		border-radius: 9999px;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
		transition: background-color 0.45s ease;
	}

	.flavour-pill-btn {
		background: transparent;
		border: none;
		border-radius: 9999px;
		padding: 0.65rem 1.4rem;
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		gap: 0.6rem;
		font-family: inherit;
		font-size: 0.95rem;
		font-weight: 800;
		color: #ffffff;
		transition: background-color 0.2s ease, transform 0.15s ease, color 0.2s ease;
	}

	.flavour-pill-btn:hover {
		transform: scale(1.04);
		background: rgba(255, 255, 255, 0.08);
	}

	.flavour-pill-btn.active {
		background: var(--color-primary);
		color: var(--color-tertiary);
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
	}

	.pill-dot {
		width: 10px;
		height: 10px;
		border-radius: 50%;
		background: var(--color-primary);
		transition: background-color 0.2s ease;
	}

	.flavour-pill-btn.active .pill-dot {
		background: var(--color-tertiary);
	}

	/* SHOWCASE STAGE */
	.flavour-showcase-stage {
		padding: 3rem 1.5rem 4.5rem;
		display: flex;
		justify-content: center;
	}

	.showcase-inner {
		max-width: 1140px;
		width: 100%;
		display: grid;
		grid-template-columns: 440px 1fr;
		gap: 4rem;
		align-items: flex-start;
	}

	/* 3D CARD DISPLAY */
	.showcase-card-col {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.25rem;
		position: sticky;
		top: 100px;
	}

	.flip-stage {
		width: 100%;
		max-width: 400px;
		height: 533px;
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
		transform: translateY(-10px) rotateY(180deg);
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
		filter: drop-shadow(0 20px 48px rgba(0, 0, 0, 0.35));
	}

	.flip-back {
		transform: rotateY(180deg);
	}

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
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
		transition:
			transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1),
			background-color 0.45s ease,
			color 0.45s ease;
	}

	.round-flip-btn:hover {
		transform: scale(1.12);
	}

	.round-flip-btn .flip-svg {
		width: 25px;
		height: 25px;
		transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	.round-flip-btn.is-flipped .flip-svg {
		transform: rotate(180deg);
	}

	.flip-hint-text {
		font-size: 0.85rem;
		font-weight: 700;
		color: var(--color-primary);
		opacity: 0.9;
	}

	/* RIGHT COLUMN: SPECS & NIP */
	.showcase-details-col {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.flavour-header-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		flex-wrap: wrap;
	}

	.flavour-kicker {
		font-size: 0.88rem;
		font-weight: 900;
		letter-spacing: 0.16em;
		color: var(--color-primary);
	}

	.allergen-pill {
		font-size: 0.72rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		padding: 0.35rem 0.85rem;
		border-radius: 9999px;
		background: var(--color-primary);
		color: var(--color-tertiary);
		transition: background-color 0.45s ease, color 0.45s ease;
	}

	.flavour-title {
		font-size: clamp(2.4rem, 4.5vw, 3.6rem);
		font-weight: 900;
		line-height: 1;
		color: var(--color-primary);
		letter-spacing: -0.03em;
		margin: 0;
	}

	.flavour-tagline {
		font-size: 1.15rem;
		line-height: 1.5;
		color: #ffffff;
		opacity: 0.95;
		font-weight: 600;
		margin: 0;
	}

	/* HIGHLIGHT CHIPS */
	.highlights-row {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
	}

	.highlight-chip {
		font-size: 0.82rem;
		font-weight: 800;
		background: rgba(255, 255, 255, 0.08);
		color: #ffffff;
		padding: 0.4rem 0.9rem;
		border-radius: 9999px;
	}

	/* 4-CARD MATRIX GRID */
	.spec-matrix-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1.15rem;
	}

	.matrix-card {
		background: var(--color-tertiary);
		border-radius: 18px;
		padding: 1.4rem 1.6rem;
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
		transition: background-color 0.45s ease;
	}

	.matrix-label {
		font-size: 0.75rem;
		font-weight: 900;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--color-primary);
		opacity: 0.9;
	}

	.matrix-val {
		font-size: 0.98rem;
		font-weight: 700;
		color: #ffffff;
		line-height: 1.5;
		margin: 0;
	}

	.matrix-sub {
		font-size: 0.82rem;
		color: var(--color-primary);
		line-height: 1.4;
		opacity: 0.95;
	}

	/* NUTRITION INFORMATION PANEL */
	.nutrition-card {
		background: var(--color-tertiary);
		border-radius: 18px;
		padding: 1.5rem 1.8rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		transition: background-color 0.45s ease;
	}

	.nutrition-title-row {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		flex-wrap: wrap;
		gap: 0.5rem;
		border-bottom: 2px solid var(--color-primary);
		padding-bottom: 0.6rem;
	}

	.nutrition-heading {
		font-size: 0.88rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		color: var(--color-primary);
	}

	.nutrition-meta {
		font-size: 0.78rem;
		font-weight: 700;
		color: #ffffff;
		opacity: 0.8;
	}

	.nutrition-table-wrap {
		overflow-x: auto;
	}

	.nip-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.88rem;
		text-align: left;
	}

	.nip-table th {
		font-size: 0.78rem;
		font-weight: 900;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--color-primary);
		padding: 0.4rem 0.6rem;
		border-bottom: 1px solid rgba(255, 255, 255, 0.12);
	}

	.nip-table td {
		padding: 0.45rem 0.6rem;
		border-bottom: 1px solid rgba(255, 255, 255, 0.06);
		color: #ffffff;
		font-weight: 600;
	}

	.nip-table tr.indent td:first-child {
		padding-left: 1.4rem;
		opacity: 0.85;
	}

	.col-nutrient {
		width: 44%;
	}
	.col-serve {
		width: 28%;
		text-align: right;
	}
	.col-100g {
		width: 28%;
		text-align: right;
	}

	.nip-table td:nth-child(2),
	.nip-table td:nth-child(3),
	.nip-table th:nth-child(2),
	.nip-table th:nth-child(3) {
		text-align: right;
	}

	/* INTEGRITY CALLOUT */
	.integrity-callout {
		display: flex;
		gap: 1rem;
		align-items: flex-start;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 14px;
		padding: 1.15rem 1.4rem;
	}

	.integrity-icon {
		font-size: 1.2rem;
		color: var(--color-primary);
		line-height: 1;
	}

	.integrity-text {
		font-size: 0.88rem;
		line-height: 1.5;
		color: #ffffff;
		opacity: 0.95;
	}

	/* MIXED SHEET SHOWCASE */
	.mixed-sheet-showcase {
		padding: 3.5rem 1.5rem 4rem;
		display: flex;
		justify-content: center;
	}

	.mixed-sheet-inner {
		max-width: 1140px;
		width: 100%;
		background: var(--color-tertiary);
		border-radius: 24px;
		padding: 3.5rem;
		display: grid;
		grid-template-columns: 1fr 300px;
		gap: 3.5rem;
		align-items: center;
		box-shadow: 0 16px 48px rgba(0, 0, 0, 0.35);
		transition: background-color 0.45s ease;
	}

	.mixed-badge {
		display: inline-block;
		background: var(--color-primary);
		color: var(--color-tertiary);
		font-size: 0.75rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		padding: 0.4rem 0.95rem;
		border-radius: 9999px;
		margin-bottom: 0.9rem;
		transition: background-color 0.45s ease, color 0.45s ease;
	}

	.mixed-title {
		font-size: clamp(2.2rem, 4vw, 3.2rem);
		font-weight: 900;
		color: var(--color-primary);
		letter-spacing: -0.03em;
		line-height: 1;
		margin: 0 0 1rem;
	}

	.mixed-lead {
		font-size: 1.1rem;
		line-height: 1.6;
		color: #ffffff;
		opacity: 0.95;
		margin: 0 0 1.75rem;
	}

	.mixed-flavours-strip {
		display: flex;
		gap: 1.25rem;
		flex-wrap: wrap;
		margin-bottom: 1.75rem;
	}

	.mini-strip-item {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		background: rgba(255, 255, 255, 0.08);
		padding: 0.5rem 1rem;
		border-radius: 9999px;
		font-size: 0.9rem;
	}

	.strip-dot {
		width: 10px;
		height: 10px;
		border-radius: 50%;
	}

	.mixed-notice {
		font-size: 0.88rem;
		line-height: 1.5;
		color: #ffffff;
		opacity: 0.85;
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		padding-top: 1rem;
	}

	.mixed-price-side {
		display: flex;
		justify-content: center;
	}

	.price-bubble {
		background: rgba(0, 0, 0, 0.28);
		border-radius: 20px;
		padding: 2.25rem 2rem;
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		max-width: 280px;
	}

	.price-val {
		font-size: 3.5rem;
		font-weight: 900;
		color: var(--color-primary);
		line-height: 1;
		letter-spacing: -0.04em;
	}

	.price-unit {
		font-size: 0.95rem;
		font-weight: 900;
		color: #ffffff;
		margin-top: 0.25rem;
		letter-spacing: 0.04em;
	}

	.price-divider {
		width: 40px;
		height: 4px;
		border-radius: 999px;
		background: var(--color-primary);
		margin: 1.25rem 0;
	}

	.price-stats {
		font-size: 0.95rem;
		font-weight: 800;
		color: #ffffff;
		margin-bottom: 0.25rem;
	}

	.price-sub {
		font-size: 0.82rem;
		font-weight: 700;
		color: var(--color-primary);
	}

	/* COMPLIANCE & INTEGRITY SECTION */
	.compliance-section {
		padding: 3rem 1.5rem 4rem;
		display: flex;
		justify-content: center;
	}

	.compliance-inner {
		max-width: 1140px;
		width: 100%;
		background: var(--color-tertiary);
		border-radius: 24px;
		padding: 3.5rem;
		transition: background-color 0.45s ease;
	}

	.compliance-header {
		text-align: center;
		max-width: 720px;
		margin: 0 auto 2.75rem;
	}

	.compliance-kicker {
		font-size: 0.85rem;
		font-weight: 900;
		letter-spacing: 0.16em;
		color: var(--color-primary);
		margin-bottom: 0.5rem;
	}

	.compliance-title {
		font-size: clamp(2rem, 3.8vw, 2.8rem);
		font-weight: 900;
		color: var(--color-primary);
		letter-spacing: -0.03em;
		margin-bottom: 0.75rem;
	}

	.compliance-sub {
		font-size: 1.05rem;
		color: #ffffff;
		opacity: 0.9;
		line-height: 1.5;
	}

	.compliance-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1.75rem;
	}

	.compliance-card {
		background: rgba(0, 0, 0, 0.24);
		border-radius: 18px;
		padding: 2rem 1.75rem;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.card-heading {
		font-size: 1.15rem;
		font-weight: 900;
		color: var(--color-primary);
		margin: 0;
	}

	.card-text {
		font-size: 0.92rem;
		color: #ffffff;
		opacity: 0.9;
		line-height: 1.55;
		margin: 0;
	}

	/* RESPONSIVE LAYOUT */
	@media (max-width: 960px) {
		.showcase-inner {
			grid-template-columns: 1fr;
			gap: 3rem;
		}

		.showcase-card-col {
			position: static;
		}

		.flip-stage {
			max-width: 360px;
			height: 480px;
		}

		.mixed-sheet-inner {
			grid-template-columns: 1fr;
			gap: 2.5rem;
			padding: 2.5rem;
		}

		.compliance-grid {
			grid-template-columns: 1fr;
			gap: 1.25rem;
		}
	}

	@media (max-width: 640px) {
		.specs-hero {
			padding: 2rem 1rem 1.75rem;
		}

		.hero-title {
			font-size: 2.4rem;
		}

		.flavour-selector-pills {
			border-radius: 20px;
			gap: 0.4rem;
		}

		.flavour-pill-btn {
			padding: 0.5rem 0.9rem;
			font-size: 0.85rem;
		}

		.flavour-showcase-stage {
			padding: 1.5rem 1rem 3rem;
		}

		.flip-stage {
			max-width: 300px;
			height: 400px;
		}

		.spec-matrix-grid {
			grid-template-columns: 1fr;
		}

		.nutrition-card {
			padding: 1.25rem 1rem;
		}

		.mixed-sheet-inner {
			padding: 1.75rem 1.25rem;
		}

		.price-bubble {
			padding: 1.75rem 1.25rem;
		}

		.compliance-inner {
			padding: 2rem 1.25rem;
		}
	}
</style>
