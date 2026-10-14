<script lang="ts">
	interface Props {
		flavour: 'butter' | 'raspberry' | 'yeast' | 'peanut';
		class?: string;
		standalone?: boolean;
	}

	let { flavour, class: className = '', standalone = false }: Props = $props();

	const ORIGINAL_PACK_COLORS = {
		butter: {
			primary: '#ffd640',
			tertiary: '#2d1d00'
		},
		raspberry: {
			primary: '#ff467a',
			tertiary: '#2d0414'
		},
		yeast: {
			primary: '#e24bff',
			tertiary: '#18012b'
		},
		peanut: {
			primary: '#ff8c30',
			tertiary: '#2d1403'
		}
	};

	let primaryColor = $derived(standalone ? ORIGINAL_PACK_COLORS[flavour].primary : 'var(--color-primary)');
	let tertiaryColor = $derived(standalone ? ORIGINAL_PACK_COLORS[flavour].tertiary : 'var(--color-tertiary)');

	const FLAVOUR_BACK_DATA = {
		butter: {
			title: 'Salted Butter',
			ingredients: 'Cultured butterfat (milk), salt.',
			allergens: 'Contains: milk.',
			nutrition: [
				['Energy', '361 kJ', '3610 kJ'],
				['Protein', '0 g', '0 g'],
				['Fat, total', '9.8 g', '97.5 g'],
				['– saturated', '5.9 g', '58.8 g'],
				['Carbohydrate', '0 g', '0 g'],
				['– sugars', '0 g', '0 g'],
				['Dietary fibre', '0 g', '0 g'],
				['Sodium', '98 mg', '982 mg']
			]
		},
		raspberry: {
			title: 'Raspberry',
			ingredients: 'Raspberries, sugar, lemon juice. Made with 150 g raspberries per 100 g.',
			allergens: 'Contains: no declared allergens.',
			nutrition: [
				['Energy', '93 kJ', '929 kJ'],
				['Protein', '0.2 g', '1.8 g'],
				['Fat, total', '0.1 g', '1.0 g'],
				['– saturated', '0 g', '0 g'],
				['Carbohydrate', '4.6 g', '46.1 g'],
				['– sugars', '4.4 g', '44.3 g'],
				['Dietary fibre', '1.0 g', '9.8 g'],
				['Sodium', '<5 mg', '<5 mg']
			]
		},
		yeast: {
			title: 'Yeast extract',
			ingredients: 'Yeast extract (80%), barley malt extract (barley), salt, vegetable concentrate.',
			allergens: 'Contains: barley (gluten).',
			nutrition: [
				['Energy', '76 kJ', '755 kJ'],
				['Protein', '2.3 g', '23.0 g'],
				['Fat, total', '0 g', '0.4 g'],
				['– saturated', '0 g', '0.1 g'],
				['Carbohydrate', '2.0 g', '19.6 g'],
				['– sugars', '1.0 g', '10.0 g'],
				['Dietary fibre', '0.2 g', '1.9 g'],
				['Sodium', '280 mg', '2803 mg']
			]
		},
		peanut: {
			title: 'Peanut',
			ingredients: 'Peanuts (96%), vegetable fat, salt.',
			allergens: 'Contains: peanuts.',
			nutrition: [
				['Energy', '247 kJ', '2470 kJ'],
				['Protein', '2.6 g', '25.8 g'],
				['Fat, total', '4.6 g', '46.5 g'],
				['– saturated', '0.7 g', '7.3 g'],
				['Carbohydrate', '1.5 g', '15.0 g'],
				['– sugars', '0.5 g', '5.3 g'],
				['Dietary fibre', '0.7 g', '7.4 g'],
				['Sodium', '67 mg', '668 mg']
			]
		}
	};
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	viewBox="0 0 1200 1600"
	role="img"
	aria-label="{FLAVOUR_BACK_DATA[flavour].title} Stamp Pack Back"
	class="flavour-pack-svg {className}"
>
	<!-- Pack Card Base (Flat Solid Surface, Dynamic Tertiary Brand Color) -->
	<rect
		width="1200"
		height="1600"
		rx="48"
		fill={tertiaryColor}
		class="pack-card-base"
	/>

	<!-- STAMP Wordmark at Top of Back Panel -->
	<g transform="translate(360, 48) scale(0.33)" fill={primaryColor} class="pack-svg-mark">
		<!-- S -->
		<g transform="translate(0.0 0)">
			<path
				d="M 48.3 0 H 201.7 A 48.3 48.3 0 0 1 201.7 96.6 H 122.1 A 12.1 12.1 0 0 0 122.1 120.7 H 201.7 A 48.3 48.3 0 0 1 250.0 169.0 V 289.7 A 48.3 48.3 0 0 1 201.7 338.0 H 48.3 A 48.3 48.3 0 0 1 48.3 241.4 H 127.9 A 12.1 12.1 0 0 0 127.9 217.3 H 48.3 A 48.3 48.3 0 0 1 0 169.0 V 48.3 A 48.3 48.3 0 0 1 48.3 0 Z"
				fill-rule="evenodd"
			/>
		</g>
		<!-- T -->
		<g transform="translate(268.0 0)">
			<path
				d="M 39.0 0 H 211.0 A 39.0 39.0 0 0 1 211.0 78.0 H 180.0 V 283.0 A 55.0 55.0 0 0 1 70.0 283.0 V 78.0 H 39.0 A 39.0 39.0 0 0 1 39.0 0 Z"
				fill-rule="evenodd"
			/>
		</g>
		<!-- A -->
		<g transform="translate(536.0 0)">
			<path
				d="M 0 120.0 A 120.0 120.0 0 0 1 240.0 120.0 L 240.0 283.0 A 55.0 55.0 0 0 1 130.0 283.0 L 130.0 224.0 A 10.0 10.0 0 0 0 110.0 224.0 L 110.0 283.0 A 55.0 55.0 0 0 1 0 283.0 Z M 110.0 88.0 A 10.0 10.0 0 0 1 130.0 88.0 L 130.0 166.0 A 10.0 10.0 0 0 1 110.0 166.0 Z"
				fill-rule="evenodd"
			/>
		</g>
		<!-- M (first arch) -->
		<g transform="translate(794.0 0)">
			<path
				d="M 0 120.0 A 120.0 120.0 0 0 1 240.0 120.0 L 240.0 283.0 A 55.0 55.0 0 0 1 130.0 283.0 L 130.0 74 A 10.0 10.0 0 0 0 110.0 74 L 110.0 283.0 A 55.0 55.0 0 0 1 0 283.0 Z"
				fill-rule="evenodd"
			/>
		</g>
		<!-- M (second arch) -->
		<g transform="translate(924.0 0)">
			<path
				d="M 0 120.0 A 120.0 120.0 0 0 1 240.0 120.0 L 240.0 283.0 A 55.0 55.0 0 0 1 130.0 283.0 L 130.0 74 A 10.0 10.0 0 0 0 110.0 74 L 110.0 283.0 A 55.0 55.0 0 0 1 0 283.0 Z"
				fill-rule="evenodd"
			/>
		</g>
		<!-- P -->
		<g transform="translate(1182.0 0)">
			<path
				d="M 0 64 A 64 64 0 0 1 64 0 H 184 A 64 64 0 0 1 248 64 V 148 A 28 28 0 0 1 220 176 H 110 V 283.0 A 55.0 55.0 0 0 1 0 283.0 Z M 110.0 60.0 A 14.0 14.0 0 0 1 138.0 60.0 L 138.0 116.0 A 14.0 14.0 0 0 1 110.0 116.0 Z"
				fill-rule="evenodd"
			/>
		</g>
	</g>

	<text
		x="600"
		y="215"
		text-anchor="middle"
		font-family="'Manrope', sans-serif"
		font-weight="900"
		font-size="44"
		fill={primaryColor}
		class="pack-svg-text"
	>
		{FLAVOUR_BACK_DATA[flavour].title} spread
	</text>

	<!-- Mini Vector Icon -->
	<g
		transform="translate(450, 240) scale(0.46)"
		stroke={primaryColor}
		stroke-width="14"
		stroke-linecap="round"
		stroke-linejoin="round"
		fill="none"
		class="pack-svg-stroke"
	>
		{#if flavour === 'butter'}
			<line x1="88" y1="292" x2="552" y2="292" />
			<path d="M168 292 V152 A28 28 0 0 1 196 124 H416 A28 28 0 0 1 444 152 V292" />
			<line x1="270" y1="124" x2="270" y2="214" />
			<line x1="372" y1="124" x2="372" y2="214" />
		{:else if flavour === 'raspberry'}
			<circle cx="320" cy="164" r="20" />
			<circle cx="286" cy="208" r="26" />
			<circle cx="354" cy="208" r="26" />
			<circle cx="258" cy="258" r="28" />
			<circle cx="320" cy="264" r="28" />
			<circle cx="382" cy="258" r="28" />
			<line x1="88" y1="292" x2="552" y2="292" />
		{:else if flavour === 'yeast'}
			<line x1="230" y1="48" x2="230" y2="292" />
			<ellipse cx="204" cy="134" rx="20" ry="12" transform="rotate(38 204 134)" />
			<ellipse cx="256" cy="162" rx="19" ry="12" transform="rotate(-38 256 162)" />
			<ellipse cx="204" cy="190" rx="18" ry="12" transform="rotate(38 204 190)" />
			<line x1="410" y1="48" x2="410" y2="292" />
			<ellipse cx="384" cy="134" rx="20" ry="12" transform="rotate(38 384 134)" />
			<ellipse cx="436" cy="162" rx="19" ry="12" transform="rotate(-38 436 162)" />
			<ellipse cx="384" cy="190" rx="18" ry="12" transform="rotate(38 384 190)" />
			<line x1="88" y1="292" x2="552" y2="292" />
		{:else if flavour === 'peanut'}
			<g transform="translate(220 236) scale(0.95)">
				<path d="M-96 6 C-96 -30 -58 -42 -28 -26 C-12 -16 -2 -16 14 -24 C52 -44 104 -22 104 12 C104 40 62 48 26 34 C10 26 0 26 -14 34 C-50 48 -96 36 -96 6 Z" />
			</g>
			<g transform="translate(455 248) scale(0.65)">
				<path d="M-96 6 C-96 -30 -58 -42 -28 -26 C-12 -16 -2 -16 14 -24 C52 -44 104 -22 104 12 C104 40 62 48 26 34 C10 26 0 26 -14 34 C-50 48 -96 36 -96 6 Z" />
			</g>
			<line x1="88" y1="292" x2="552" y2="292" />
		{/if}
	</g>

	<!-- INGREDIENTS SECTION -->
	<text
		x="90"
		y="430"
		font-family="'Manrope', sans-serif"
		font-weight="900"
		font-size="28"
		letter-spacing="0.1em"
		fill={primaryColor}
		class="pack-svg-text"
	>
		INGREDIENTS
	</text>

	<text
		x="90"
		y="475"
		font-family="'Manrope', sans-serif"
		font-weight="600"
		font-size="26"
		fill="#ffffff"
	>
		{FLAVOUR_BACK_DATA[flavour].ingredients}
	</text>

	<text
		x="90"
		y="520"
		font-family="'Manrope', sans-serif"
		font-weight="800"
		font-size="26"
		fill={primaryColor}
		class="pack-svg-text"
	>
		{FLAVOUR_BACK_DATA[flavour].allergens}
	</text>

	<text
		x="90"
		y="565"
		font-family="'Manrope', sans-serif"
		font-weight="600"
		font-size="24"
		fill="#ffffff"
		opacity="0.8"
	>
		Made in a facility that handles milk, gluten, and peanuts.
	</text>

	<!-- NUTRITION INFORMATION SECTION -->
	<text
		x="90"
		y="645"
		font-family="'Manrope', sans-serif"
		font-weight="900"
		font-size="28"
		letter-spacing="0.1em"
		fill={primaryColor}
		class="pack-svg-text"
	>
		NUTRITION INFORMATION
	</text>

	<text
		x="90"
		y="690"
		font-family="'Manrope', sans-serif"
		font-weight="600"
		font-size="24"
		fill="#ffffff"
		opacity="0.9"
	>
		Servings per package: 8   |   Serving size: 10 g (1 stamp)
	</text>

	<!-- Table Rule Top -->
	<line x1="90" y1="720" x2="1110" y2="720" stroke={primaryColor} stroke-width="3" opacity="0.4" class="pack-svg-stroke" />

	<!-- Table Column Headers -->
	<text x="90" y="755" font-family="'Manrope', sans-serif" font-weight="900" font-size="22" fill={primaryColor} class="pack-svg-text">Average Quantity</text>
	<text x="750" y="755" text-anchor="end" font-family="'Manrope', sans-serif" font-weight="900" font-size="22" fill={primaryColor} class="pack-svg-text">Per Serving (10 g)</text>
	<text x="1110" y="755" text-anchor="end" font-family="'Manrope', sans-serif" font-weight="900" font-size="22" fill={primaryColor} class="pack-svg-text">Per 100 g</text>

	<line x1="90" y1="775" x2="1110" y2="775" stroke={primaryColor} stroke-width="3" class="pack-svg-stroke" />

	<!-- Nutrition Rows -->
	{#each FLAVOUR_BACK_DATA[flavour].nutrition as row, idx}
		{@const yPos = 825 + idx * 64}
		<text x="90" y={yPos} font-family="'Manrope', sans-serif" font-weight={row[0].startsWith('–') ? '600' : '800'} font-size="24" fill="#ffffff" dx={row[0].startsWith('–') ? '24' : '0'}>
			{row[0]}
		</text>
		<text x="750" y={yPos} text-anchor="end" font-family="'Manrope', sans-serif" font-weight="700" font-size="24" fill="#ffffff">
			{row[1]}
		</text>
		<text x="1110" y={yPos} text-anchor="end" font-family="'Manrope', sans-serif" font-weight="700" font-size="24" fill="#ffffff">
			{row[2]}
		</text>
		{#if idx < FLAVOUR_BACK_DATA[flavour].nutrition.length - 1}
			<line x1="90" y1={yPos + 22} x2="1110" y2={yPos + 22} stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5" />
		{/if}
	{/each}

	<line x1="90" y1="1350" x2="1110" y2="1350" stroke={primaryColor} stroke-width="3" opacity="0.4" class="pack-svg-stroke" />

	<!-- Regulatory Microcopy -->
	<text x="600" y="1400" text-anchor="middle" font-family="'Manrope', sans-serif" font-weight="600" font-size="22" fill="#ffffff" opacity="0.8">
		Storage: Ambient pantry stable. Sits dry at room temperature.
	</text>

	<!-- Bottom Brand Footer Bar -->
	<path
		d="M 0 1460 H 1200 V 1552 A 48 48 0 0 1 1152 1600 H 48 A 48 48 0 0 1 0 1552 Z"
		fill={primaryColor}
		class="pack-peel-bar"
	/>

	<text
		x="600"
		y="1542"
		text-anchor="middle"
		font-family="'Manrope', sans-serif"
		font-weight="900"
		font-size="34"
		letter-spacing="0.08em"
		fill={tertiaryColor}
		class="pack-peel-text"
	>
		MADE IN NEW ZEALAND · NO KNIFE REQUIRED
	</text>
</svg>

<style>
	.flavour-pack-svg {
		width: 100%;
		height: 100%;
		display: block;
	}

	.pack-card-base,
	.pack-svg-mark,
	.pack-svg-text,
	.pack-svg-stroke,
	.pack-peel-bar,
	.pack-peel-text {
		transition: fill 0.45s ease, stroke 0.45s ease;
	}
</style>
