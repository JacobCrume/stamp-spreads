<script lang="ts">
	const flavours = [
		{
			id: 'butter',
			name: 'Salted Butter Spread',
			desc: 'Cultured butterfat and salt (2 g salt / 78 g fat). Melts into rich, golden toast without tearing the crumb.',
			allergen: 'Contains Milk',
			img: '/flavours/butter.png'
		},
		{
			id: 'raspberry',
			name: 'Raspberry Spread',
			desc: 'Cooked whole raspberries, caster sugar, and fresh lemon. Reduced down so 150 g fruit makes 100 g paste.',
			allergen: 'Made in facility handling milk & peanuts',
			img: '/flavours/raspberry.png'
		},
		{
			id: 'yeast',
			name: 'Yeast Extract Spread',
			desc: '80% yeast extract, 15.5% barley malt extract, 2.5% salt, 2% vegetable concentrate. Bold, savory umami paste.',
			allergen: 'Contains Gluten (barley)',
			img: '/flavours/yeast.png'
		},
		{
			id: 'peanut',
			name: 'Peanut Spread',
			desc: '96% roasted peanuts, 2.3% stabilizing vegetable fat, and 1.7% salt. Rich peanut flavour that never oils off in the card.',
			allergen: 'Contains Peanuts',
			img: '/flavours/peanut.png'
		}
	];
</script>

<svelte:head>
	<title>STAMP — Peel. Press. Toast.</title>
</svelte:head>

<section class="hero-section">
	<div class="hero-inner">
		<div class="hero-copy">
			<div class="kicker">NEW ZEALAND BREAKFAST INNOVATION</div>
			<h1 class="hero-title">Peel. Press. Toast.</h1>
			<p class="hero-lead">
				Stamp is a thin, single-serve disc of real spread on a food-safe release film, nested in a
				pocketable card sheet. Peel one off, press it onto hot toast, and residual heat softens it
				into an even layer.
			</p>
			<p class="hero-bullets">
				<strong>No knife. No open jar. No wash-up.</strong>
			</p>
			<div class="hero-actions">
				<a href="/flavours" class="btn btn-primary">Explore 4 Launch Flavours</a>
				<button
					type="button"
					class="btn btn-outline"
					onclick={() => {
						if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent('stamp:open-chat'));
					}}>Ask our Support Bot</button
				>
			</div>
			<div class="hero-price-badge">
				<span class="price-val">$5.00 NZD</span>
				<span class="price-detail">per 8-stamp sheet (80 g) · $6.25 / 100 g</span>
			</div>
		</div>
		<div class="hero-media">
			<img src="/pack.png" alt="STAMP Pack Sheet" class="hero-img" />
			<p class="media-caption">
				The 8-stamp card sheet: individual release film discs nested flat.
			</p>
		</div>
	</div>
</section>

<section class="how-it-works">
	<div class="section-inner">
		<div class="section-header">
			<h2 class="section-title">How Stamp Works</h2>
			<p class="section-subtitle">
				Designed for mornings away from a full kitchen: in flats, halls, offices, or out of a bag.
			</p>
		</div>

		<div class="steps-grid">
			<div class="step-card">
				<div class="step-num">1</div>
				<h3 class="step-title">Pantry Ready</h3>
				<p class="step-text">
					Store unopened sheets in your pantry for up to 12 months. No refrigeration required.
				</p>
			</div>
			<div class="step-card">
				<div class="step-num">2</div>
				<h3 class="step-title">Peel One Stamp</h3>
				<p class="step-text">
					Peel an exact 10 g disc cleanly off the food-grade release liner.
				</p>
			</div>
			<div class="step-card">
				<div class="step-num">3</div>
				<h3 class="step-title">Press onto Hot Toast</h3>
				<p class="step-text">
					Place the disc directly onto hot toast and apply gentle pressure across the film.
				</p>
			</div>
			<div class="step-card">
				<div class="step-num">4</div>
				<h3 class="step-title">Melt & Enjoy</h3>
				<p class="step-text">
					Residual toast heat softens the paste into a perfect layer within seconds. Done!
				</p>
			</div>
		</div>
	</div>
</section>

<section class="flavours-preview">
	<div class="section-inner">
		<div class="section-header">
			<h2 class="section-title">Four Real Flavours</h2>
			<p class="section-subtitle">
				Available in single-flavour 8-stamp sheets and a mixed sheet with two of each.
			</p>
		</div>

		<div class="flavours-grid">
			{#each flavours as f}
				<div class="flavour-card">
					<div class="card-img-wrap">
						<img src={f.img} alt={f.name} class="flavour-thumb" />
					</div>
					<div class="card-body">
						<h3 class="card-title">{f.name}</h3>
						<p class="card-desc">{f.desc}</p>
						<div class="allergen-tag">{f.allergen}</div>
					</div>
				</div>
			{/each}
		</div>

		<div class="view-all-wrap">
			<a href="/flavours" class="btn btn-secondary">View Full Nutritional & Ingredient Specs →</a>
		</div>
	</div>
</section>

<section class="market-section">
	<div class="section-inner">
		<div class="market-card">
			<div class="market-copy">
				<h2 class="market-heading">Category Opportunity</h2>
				<p class="market-text">
					Analysis of New Zealand breakfast retail sales shows spreads revenue expanding from $275m
					NZD in 2022 to $341m NZD in 2025 (24% growth), with premium spreads leading category
					expansion. Yet across 154 existing spread names, not a single brand offers a portioned,
					peel-and-press format.
				</p>
				<p class="market-text">
					Stamp fills that gap at <strong>$5.00 NZD</strong> ($6.25 per 100 g), offering portable single-serve
					convenience without the clutter or waste of traditional jars.
				</p>
			</div>
			<div class="ad-visual">
				<img src="/ad.png" alt="STAMP Campaign Ad" class="ad-img" />
			</div>
		</div>
	</div>
</section>

<style>
	.hero-section {
		background: linear-gradient(135deg, #ffffff 0%, #f7eaff 100%);
		padding: 4rem 1.5rem;
		border-bottom: 1px solid #ebd4ff;
	}

	.hero-inner {
		max-width: 1120px;
		margin: 0 auto;
		display: grid;
		grid-template-columns: 1.15fr 0.85fr;
		gap: 3.5rem;
		align-items: center;
	}

	.kicker {
		font-size: 0.82rem;
		font-weight: 800;
		letter-spacing: 0.08em;
		color: #3b0764;
		margin-bottom: 0.75rem;
	}

	.hero-title {
		font-size: 3.4rem;
		line-height: 1.08;
		font-weight: 800;
		color: #3b0764;
		margin-bottom: 1.25rem;
		letter-spacing: -0.03em;
	}

	.hero-lead {
		font-size: 1.2rem;
		line-height: 1.55;
		color: #2e1c40;
		margin-bottom: 1rem;
	}

	.hero-bullets {
		font-size: 1.05rem;
		color: #3b0764;
		margin-bottom: 1.75rem;
	}

	.hero-actions {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		margin-bottom: 2rem;
	}

	.btn {
		display: inline-block;
		padding: 0.8rem 1.6rem;
		font-weight: 700;
		font-size: 0.98rem;
		border-radius: 8px;
		text-decoration: none;
		transition: all 0.15s ease;
		cursor: pointer;
	}

	.btn-primary {
		background-color: #3b0764;
		color: #ffffff;
		border: 2px solid #3b0764;
	}

	.btn-primary:hover {
		background-color: #550a8a;
		border-color: #550a8a;
		transform: translateY(-1px);
	}

	.btn-outline {
		background-color: transparent;
		color: #3b0764;
		border: 2px solid #3b0764;
	}

	.btn-outline:hover {
		background-color: #3b0764;
		color: #ffffff;
	}

	.btn-secondary {
		background-color: #e24bff;
		color: #3b0764;
		border: 2px solid #e24bff;
	}

	.btn-secondary:hover {
		background-color: #d122f5;
		color: #ffffff;
	}

	.hero-price-badge {
		display: inline-flex;
		align-items: center;
		gap: 0.75rem;
		background-color: #ffffff;
		padding: 0.6rem 1.2rem;
		border-radius: 999px;
		border: 1px solid #d4a6f7;
		box-shadow: 0 2px 8px rgba(59, 7, 100, 0.06);
	}

	.price-val {
		font-size: 1.25rem;
		font-weight: 800;
		color: #3b0764;
	}

	.price-detail {
		font-size: 0.85rem;
		color: #634380;
		font-weight: 600;
	}

	.hero-media {
		text-align: center;
	}

	.hero-img {
		max-width: 100%;
		height: auto;
		border-radius: 12px;
		box-shadow: 0 12px 32px rgba(59, 7, 100, 0.18);
		border: 3px solid #3b0764;
	}

	.media-caption {
		font-size: 0.85rem;
		color: #634380;
		margin-top: 0.75rem;
		font-weight: 500;
	}

	.section-inner {
		max-width: 1120px;
		margin: 0 auto;
		padding: 4.5rem 1.5rem;
	}

	.section-header {
		text-align: center;
		max-width: 680px;
		margin: 0 auto 3rem;
	}

	.section-title {
		font-size: 2.2rem;
		font-weight: 800;
		color: #3b0764;
		margin-bottom: 0.75rem;
		letter-spacing: -0.02em;
	}

	.section-subtitle {
		font-size: 1.05rem;
		color: #553b6e;
	}

	.steps-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 1.5rem;
	}

	.step-card {
		background: #ffffff;
		border: 1px solid #ebd4ff;
		padding: 2rem 1.5rem;
		border-radius: 10px;
		position: relative;
		transition: transform 0.15s ease;
	}

	.step-card:hover {
		transform: translateY(-2px);
		box-shadow: 0 6px 16px rgba(59, 7, 100, 0.08);
	}

	.step-num {
		width: 38px;
		height: 38px;
		background: #e24bff;
		color: #3b0764;
		font-weight: 800;
		font-size: 1.2rem;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 1rem;
	}

	.step-title {
		font-size: 1.2rem;
		font-weight: 700;
		color: #3b0764;
		margin-bottom: 0.5rem;
	}

	.step-text {
		font-size: 0.92rem;
		color: #4a3560;
		line-height: 1.5;
	}

	.flavours-preview {
		background: #fbf7ff;
		border-top: 1px solid #ebd4ff;
		border-bottom: 1px solid #ebd4ff;
	}

	.flavours-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: 1.75rem;
	}

	.flavour-card {
		background: #ffffff;
		border-radius: 10px;
		border: 1px solid #ecd8ff;
		overflow: hidden;
		display: flex;
		flex-direction: column;
		box-shadow: 0 4px 12px rgba(59, 7, 100, 0.04);
	}

	.card-img-wrap {
		background: #3b0764;
		padding: 1.5rem 1rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.flavour-thumb {
		max-height: 170px;
		max-width: 100%;
		object-fit: contain;
	}

	.card-body {
		padding: 1.25rem;
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	.card-title {
		font-size: 1.15rem;
		font-weight: 800;
		color: #3b0764;
		margin-bottom: 0.5rem;
	}

	.card-desc {
		font-size: 0.88rem;
		color: #4a3560;
		line-height: 1.45;
		margin-bottom: 1rem;
		flex: 1;
	}

	.allergen-tag {
		font-size: 0.78rem;
		font-weight: 700;
		color: #3b0764;
		background: #f1dcff;
		padding: 0.35rem 0.6rem;
		border-radius: 4px;
		align-self: flex-start;
	}

	.view-all-wrap {
		text-align: center;
		margin-top: 3rem;
	}

	.market-card {
		background: #ffffff;
		border: 2px solid #3b0764;
		border-radius: 12px;
		padding: 3rem;
		display: grid;
		grid-template-columns: 1.2fr 0.8fr;
		gap: 2.5rem;
		align-items: center;
	}

	.market-heading {
		font-size: 2rem;
		font-weight: 800;
		color: #3b0764;
		margin-bottom: 1rem;
	}

	.market-text {
		font-size: 1.05rem;
		line-height: 1.6;
		color: #301f40;
		margin-bottom: 1rem;
	}

	.ad-visual {
		text-align: center;
	}

	.ad-img {
		max-width: 100%;
		max-height: 320px;
		border-radius: 8px;
		border: 2px solid #3b0764;
	}

	@media (max-width: 768px) {
		.hero-inner {
			grid-template-columns: 1fr;
			text-align: center;
			gap: 2rem;
		}
		.hero-title {
			font-size: 2.6rem;
		}
		.hero-actions {
			justify-content: center;
		}
		.market-card {
			grid-template-columns: 1fr;
			padding: 2rem 1.5rem;
		}
	}

	@media (max-width: 640px) {
		.hero-section {
			padding: 2.5rem 1rem 3rem;
		}
		.hero-title {
			font-size: 2.2rem;
			letter-spacing: -0.02em;
		}
		.hero-lead {
			font-size: 1.05rem;
		}
		.hero-actions {
			flex-direction: column;
			gap: 0.75rem;
			width: 100%;
		}
		.hero-actions :global(.btn) {
			width: 100%;
			justify-content: center;
			text-align: center;
		}
		.hero-price-badge {
			justify-content: center;
			flex-wrap: wrap;
			text-align: center;
		}
		.hero-img {
			max-height: 280px;
		}
		.how-it-works,
		.flavours-preview,
		.market-section {
			padding: 3rem 1rem;
		}
		.section-header {
			margin-bottom: 2rem;
		}
		.section-title {
			font-size: 1.8rem;
		}
		.step-card {
			padding: 1.5rem 1.25rem;
		}
		.market-card {
			padding: 1.75rem 1.25rem;
		}
		.market-heading {
			font-size: 1.6rem;
		}
	}
</style>
