<script lang="ts">
	import { onMount } from 'svelte';
	import { setSectionTheme } from '../../lib/theme.svelte';

	onMount(() => {
		setSectionTheme('mixed');
	});

	const flavours = [
		{
			id: 'butter',
			name: 'Salted Butter Spread',
			subtitle: 'Rich cultured dairy spread for toast',
			netWeight: '80 g (8 × 10 g stamps) or 2 stamps in Mixed Sheet',
			price: '$5.00 NZD ($6.25 per 100 g)',
			image: '/flavours/butter.png',
			tasteProfile:
				'Rich, clean butterfat with a measured 2.5% salt balance. Softens immediately on hot toast without tearing the crumb.',
			formula:
				'Cultured butterfat and salt (2 g salt to 78 g fat). No added oil, preserving dairy integrity standard.',
			allergens: 'Contains Milk.',
			facilityStatement: 'Produced in a facility that handles milk, gluten, and peanuts.',
			shelfLife: '12 months ambient and unopened in pantry.',
			claimsNotice:
				'Sold as a shelf-stable butter spread, not a pat of fridge butter. No artificial preservatives or flavor enhancers.'
		},
		{
			id: 'raspberry',
			name: 'Raspberry Spread',
			subtitle: 'Slow-cooked whole fruit paste',
			netWeight: '80 g (8 × 10 g stamps) or 2 stamps in Mixed Sheet',
			price: '$5.00 NZD ($6.25 per 100 g)',
			image: '/flavours/raspberry.png',
			tasteProfile:
				'Vibrant, tart raspberry fruit balanced with clean sweetness and fresh lemon brightness.',
			formula:
				'Real raspberries, caster sugar, and lemon juice cooked down to a thick paste. Made with 150 g whole fruit per 100 g finished product.',
			allergens: 'No major allergens in recipe.',
			facilityStatement: 'Produced in a facility that handles milk, gluten, and peanuts.',
			shelfLife: '12 months ambient and unopened in pantry.',
			claimsNotice:
				'No low-sugar or organic claims. Natural preservation achieved via reduction solids and sealed release film.'
		},
		{
			id: 'yeast',
			name: 'Yeast Extract Spread',
			subtitle: 'Bold savory umami paste',
			netWeight: '80 g (8 × 10 g stamps) or 2 stamps in Mixed Sheet',
			price: '$5.00 NZD ($6.25 per 100 g)',
			image: '/flavours/yeast.png',
			tasteProfile:
				'Intense, rich savory profile with roasted malt notes and a clean, sharp finish.',
			formula:
				'Yeast extract 80%, barley malt extract 15.5%, salt 2.5%, vegetable concentrate 2%. Proprietary recipe; not Marmite or Vegemite.',
			allergens: 'Contains Gluten (from barley malt).',
			facilityStatement: 'Produced in a facility that handles milk, gluten, and peanuts.',
			shelfLife: '12 months ambient and unopened in pantry.',
			claimsNotice:
				'NOT gluten-free. Contains barley malt extract. No health or vitamin treatment claims.'
		},
		{
			id: 'peanut',
			name: 'Peanut Spread',
			subtitle: '96% roasted peanut paste',
			netWeight: '80 g (8 × 10 g stamps) or 2 stamps in Mixed Sheet',
			price: '$5.00 NZD ($6.25 per 100 g)',
			image: '/flavours/peanut.png',
			tasteProfile:
				'Deep, natural roasted peanut flavour with balanced salinity and a silky melt on hot toast.',
			formula:
				'Roasted peanuts 96%, hard vegetable fat 2.3% (anti-separation stabilizer), salt 1.7%. Formulated to prevent oil separation over 12 months.',
			allergens: 'Contains Peanuts.',
			facilityStatement: 'Produced in a facility that handles milk, gluten, and peanuts.',
			shelfLife: '12 months ambient and unopened in pantry.',
			claimsNotice:
				'Made for portable toast portioning. Does not claim to be low-fat, keto, or a dietary supplement.'
		}
	];
</script>

<svelte:head>
	<title>Flavours & Range — STAMP</title>
	<meta
		name="description"
		content="Explore Stamp's four launch flavours: Salted Butter, Raspberry, Yeast extract, and Peanut. Full ingredient, allergen, and pack specs."
	/>
</svelte:head>

<div class="page-container">
	<header class="page-header">
		<div class="header-inner">
			<h1 class="page-title">The Launch Range</h1>
			<p class="page-intro">
				Four authentic flavours formulated specifically for peel-and-press toast release. Every
				sheet is 80 g, priced at <strong>$5.00 NZD</strong> ($6.25 per 100 g), and pantry-stable for
				12 months unopened.
			</p>
		</div>
	</header>

	<main class="page-body">
		<section class="mixed-pack-banner">
			<div class="banner-inner">
				<div class="banner-text">
					<span class="badge">POPULAR LAUNCH PACK</span>
					<h2 class="banner-title">The Mixed Sheet</h2>
					<p class="banner-desc">
						Can't pick one? The Mixed Sheet holds two stamps of each launch flavour (8 stamps total,
						80 g) for the same $5.00 NZD shelf price. Contains milk, gluten, and peanuts.
					</p>
				</div>
				<div class="banner-price">
					<div class="price-tag">$5.00</div>
					<div class="price-sub">80 g sheet · 8 stamps</div>
				</div>
			</div>
		</section>

		<section class="flavour-list">
			{#each flavours as item, idx}
				<article class="flavour-detail-card" id={item.id}>
					<div class="flavour-media">
						<img src={item.image} alt={item.name} class="flavour-pack-img" />
						<div class="pack-badge">80 g · 8 Stamps · $5.00</div>
					</div>

					<div class="flavour-info">
						<div class="flavour-header">
							<span class="flavour-number">0{idx + 1}</span>
							<div>
								<h2 class="flavour-name">{item.name}</h2>
								<p class="flavour-subtitle">{item.subtitle}</p>
							</div>
						</div>

						<div class="spec-grid">
							<div class="spec-block">
								<h3 class="spec-label">Taste Profile</h3>
								<p class="spec-value">{item.tasteProfile}</p>
							</div>

							<div class="spec-block">
								<h3 class="spec-label">Industrial Formulation</h3>
								<p class="spec-value">{item.formula}</p>
							</div>

							<div class="spec-block highlight-allergen">
								<h3 class="spec-label">Allergen Notice</h3>
								<p class="spec-value"><strong>{item.allergens}</strong></p>
								<p class="spec-sub">{item.facilityStatement}</p>
							</div>

							<div class="spec-block">
								<h3 class="spec-label">Pantry Life & Integrity</h3>
								<p class="spec-value">{item.shelfLife}</p>
								<p class="spec-sub">{item.claimsNotice}</p>
							</div>
						</div>
					</div>
				</article>
			{/each}
		</section>

		<section class="regulatory-section">
			<div class="regulatory-box">
				<h3 class="reg-title">Compliance & Truth in Advertising</h3>
				<p class="reg-text">
					Stamp is committed to factual, transparent food labeling. We strictly adhere to our claim
					policy:
				</p>
				<ul class="reg-list">
					<li>
						<strong>No Therapeutic Claims:</strong> Stamp is a toast spread, not medicine or a dietary
						supplement.
					</li>
					<li>
						<strong>No False 'Free-From' Badges:</strong> We do not market as gluten-free (our Yeast
						extract contains barley gluten), nor do we claim organic or low-sugar status.
					</li>
					<li>
						<strong>Honest Standards:</strong> Our Salted Butter uses the legal descriptor "spread" because
						it is an ambient cultured butterfat formulation, not chilled table butter.
					</li>
				</ul>
			</div>
		</section>
	</main>
</div>

<style>
	.page-container {
		max-width: 1120px;
		margin: 0 auto;
		padding: 7rem 1.5rem 5rem;
		background: transparent;
	}

	.page-header {
		text-align: center;
		max-width: 760px;
		margin: 0 auto 3rem;
	}

	.page-title {
		font-size: 2.8rem;
		font-weight: 900;
		color: var(--color-primary);
		margin-bottom: 1rem;
		letter-spacing: -0.02em;
	}

	.page-intro {
		font-size: 1.15rem;
		color: #ffffff;
		line-height: 1.6;
		opacity: 0.95;
	}

	.mixed-pack-banner {
		background: var(--color-tertiary);
		color: #ffffff;
		border-radius: 16px;
		padding: 2.5rem;
		margin-bottom: 3.5rem;
		border: none;
	}

	.banner-inner {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 2rem;
		flex-wrap: wrap;
	}

	.banner-text {
		flex: 1;
		min-width: 280px;
	}

	.badge {
		display: inline-block;
		background: var(--color-primary);
		color: var(--color-secondary);
		font-size: 0.75rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		padding: 0.35rem 0.75rem;
		border-radius: 9999px;
		margin-bottom: 0.75rem;
	}

	.banner-title {
		font-size: 2rem;
		font-weight: 900;
		margin-bottom: 0.5rem;
		color: var(--color-primary);
	}

	.banner-desc {
		font-size: 1rem;
		color: #ffffff;
		opacity: 0.95;
		line-height: 1.5;
	}

	.banner-price {
		background: var(--color-secondary);
		border: none;
		padding: 1.25rem 2rem;
		border-radius: 14px;
		text-align: center;
	}

	.price-tag {
		font-size: 2.2rem;
		font-weight: 900;
		color: var(--color-primary);
	}

	.price-sub {
		font-size: 0.85rem;
		color: #ffffff;
		opacity: 0.9;
	}

	.flavour-list {
		display: flex;
		flex-direction: column;
		gap: 3rem;
		margin-bottom: 4rem;
	}

	.flavour-detail-card {
		background: var(--color-tertiary);
		border: none;
		border-radius: 16px;
		overflow: hidden;
		display: grid;
		grid-template-columns: 320px 1fr;
	}

	.flavour-media {
		background: var(--color-secondary);
		border: none;
		padding: 2.5rem 1.5rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		position: relative;
	}

	.flavour-pack-img {
		max-height: 240px;
		max-width: 100%;
		object-fit: contain;
	}

	.pack-badge {
		margin-top: 1.5rem;
		background: var(--color-tertiary);
		border: none;
		color: var(--color-primary);
		font-size: 0.82rem;
		font-weight: 800;
		padding: 0.35rem 0.85rem;
		border-radius: 999px;
	}

	.flavour-info {
		padding: 2.5rem;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.flavour-header {
		display: flex;
		align-items: center;
		gap: 1.25rem;
		margin-bottom: 1.5rem;
		padding-bottom: 1rem;
		border-bottom: none;
	}

	.flavour-number {
		font-size: 2rem;
		font-weight: 900;
		color: var(--color-primary);
		line-height: 1;
	}

	.flavour-name {
		font-size: 1.8rem;
		font-weight: 900;
		color: var(--color-primary);
	}

	.flavour-subtitle {
		font-size: 0.95rem;
		color: #ffffff;
		opacity: 0.9;
		font-weight: 700;
	}

	.spec-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
	}

	.spec-block {
		background: var(--color-secondary);
		padding: 1.2rem;
		border-radius: 12px;
		border: none;
	}

	.highlight-allergen {
		background: var(--color-secondary);
	}

	.spec-label {
		font-size: 0.78rem;
		font-weight: 900;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--color-primary);
		margin-bottom: 0.4rem;
	}

	.spec-value {
		font-size: 0.92rem;
		color: #ffffff;
		line-height: 1.45;
		font-weight: 700;
	}

	.spec-sub {
		font-size: 0.82rem;
		color: var(--color-primary);
		margin-top: 0.4rem;
		line-height: 1.4;
	}

	.regulatory-box {
		background: var(--color-tertiary);
		border: none;
		border-radius: 16px;
		padding: 2rem;
	}

	.reg-title {
		font-size: 1.3rem;
		font-weight: 900;
		color: var(--color-primary);
		margin-bottom: 0.75rem;
	}

	.reg-text {
		font-size: 0.95rem;
		color: #ffffff;
		margin-bottom: 1rem;
		line-height: 1.5;
		opacity: 0.95;
	}

	.reg-list {
		list-style: disc;
		padding-left: 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
		font-size: 0.92rem;
		color: #ffffff;
		opacity: 0.95;
	}

	@media (max-width: 860px) {
		.flavour-detail-card {
			grid-template-columns: 1fr;
		}
		.spec-grid {
			grid-template-columns: 1fr;
		}
		.flavour-info {
			padding: 1.75rem;
		}
	}

	@media (max-width: 640px) {
		.page-header {
			padding: 2.5rem 1rem 2rem;
		}
		.page-title {
			font-size: 2.2rem;
		}
		.page-intro {
			font-size: 1rem;
		}
		.page-body {
			padding: 0 1rem;
		}
		.mixed-pack-banner {
			padding: 2rem 1.25rem;
		}
		.banner-inner {
			flex-direction: column;
			text-align: center;
			gap: 1.5rem;
		}
		.banner-price {
			width: 100%;
			padding: 1rem;
		}
		.flavour-media {
			padding: 1.75rem 1rem;
		}
		.flavour-pack-img {
			max-height: 180px;
		}
		.flavour-info {
			padding: 1.25rem 1rem;
		}
		.flavour-name {
			font-size: 1.5rem;
		}
		.regulatory-box {
			padding: 1.5rem 1rem;
		}
		.reg-title {
			font-size: 1.2rem;
		}
	}
</style>
