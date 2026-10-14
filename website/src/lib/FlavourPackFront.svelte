<script lang="ts">
	interface Props {
		flavour: 'butter' | 'raspberry' | 'yeast' | 'peanut';
		class?: string;
	}

	let { flavour, class: className = '' }: Props = $props();

	const FLAVOUR_DATA = {
		butter: {
			title: 'SALTED BUTTER',
			sub: 'spread',
			meta: '80 g · 8 STAMPS · 12 MONTHS',
			iconY: 480
		},
		raspberry: {
			title: 'RASPBERRY',
			sub: 'spread',
			meta: '80 g · 8 STAMPS · 12 MONTHS',
			iconY: 480
		},
		yeast: {
			title: 'YEAST EXTRACT',
			sub: 'spread',
			meta: '80 g · 8 STAMPS · 12 MONTHS',
			iconY: 480
		},
		peanut: {
			title: 'ROASTED PEANUT',
			sub: 'spread',
			meta: '80 g · 8 STAMPS · 12 MONTHS',
			iconY: 480
		}
	};
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	viewBox="0 0 1200 1600"
	role="img"
	aria-label="{FLAVOUR_DATA[flavour].title} Stamp Pack Front"
	class="flavour-pack-svg {className}"
>
	<!-- Pack Card Base (Flat Solid Surface, Dynamic Tertiary Brand Color) -->
	<rect
		width="1200"
		height="1600"
		rx="48"
		fill="var(--color-tertiary)"
		class="pack-card-base"
	/>

	<!-- STAMP Wordmark at Top of Card -->
	<g transform="translate(200, 110) scale(0.55)" fill="var(--color-primary)" class="pack-svg-mark">
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

	<!-- Pack Metadata -->
	<text
		x="600"
		y="380"
		text-anchor="middle"
		font-family="'Manrope', sans-serif"
		font-weight="700"
		font-size="28"
		letter-spacing="0.14em"
		fill="var(--color-primary)"
		class="pack-svg-text"
	>
		{FLAVOUR_DATA[flavour].meta}
	</text>

	<!-- Vector Line Icon Centered -->
	<g
		transform="translate(280, 470)"
		stroke="var(--color-primary)"
		stroke-width="14"
		stroke-linecap="round"
		stroke-linejoin="round"
		fill="none"
		class="pack-svg-stroke"
	>
		{#if flavour === 'butter'}
			<!-- Butter Block -->
			<line x1="88" y1="292" x2="552" y2="292" />
			<path d="M168 292 V152 A28 28 0 0 1 196 124 H416 A28 28 0 0 1 444 152 V292" />
			<line x1="270" y1="124" x2="270" y2="214" />
			<line x1="372" y1="124" x2="372" y2="214" />
			<path d="M112 108 l16 -26 l16 26 l-16 26 z" />
			<path d="M492 86 l14 -22 l14 22 l-14 22 z" />
			<path d="M534 140 l11 -18 l11 18 l-11 18 z" />
		{:else if flavour === 'raspberry'}
			<!-- Raspberry drupelet pyramid -->
			<circle cx="320" cy="164" r="20" />
			<circle cx="286" cy="208" r="26" />
			<circle cx="354" cy="208" r="26" />
			<circle cx="258" cy="258" r="28" />
			<circle cx="320" cy="264" r="28" />
			<circle cx="382" cy="258" r="28" />
			<path d="M314 150 C292 118 248 112 240 140 C268 128 292 134 316 154" />
			<line x1="312" y1="150" x2="252" y2="126" />
			<line x1="88" y1="292" x2="552" y2="292" />
		{:else if flavour === 'yeast'}
			<!-- Two Barley Ears -->
			<line x1="230" y1="48" x2="230" y2="292" />
			<ellipse cx="204" cy="78" rx="22" ry="12" transform="rotate(38 204 78)" />
			<ellipse cx="256" cy="106" rx="21" ry="12" transform="rotate(-38 256 106)" />
			<ellipse cx="204" cy="134" rx="20" ry="12" transform="rotate(38 204 134)" />
			<ellipse cx="256" cy="162" rx="19" ry="12" transform="rotate(-38 256 162)" />
			<ellipse cx="204" cy="190" rx="18" ry="12" transform="rotate(38 204 190)" />
			<ellipse cx="256" cy="218" rx="17" ry="12" transform="rotate(-38 256 218)" />
			<ellipse cx="204" cy="246" rx="16" ry="12" transform="rotate(38 204 246)" />
			<path d="M224 58 l-20 -24 M236 58 l20 -24" />
			<line x1="410" y1="48" x2="410" y2="292" />
			<ellipse cx="384" cy="78" rx="22" ry="12" transform="rotate(38 384 78)" />
			<ellipse cx="436" cy="106" rx="21" ry="12" transform="rotate(-38 436 106)" />
			<ellipse cx="384" cy="134" rx="20" ry="12" transform="rotate(38 384 134)" />
			<ellipse cx="436" cy="162" rx="19" ry="12" transform="rotate(-38 436 162)" />
			<ellipse cx="384" cy="190" rx="18" ry="12" transform="rotate(38 384 190)" />
			<ellipse cx="436" cy="218" rx="17" ry="12" transform="rotate(-38 436 218)" />
			<ellipse cx="384" cy="246" rx="16" ry="12" transform="rotate(38 384 246)" />
			<path d="M404 58 l-20 -24 M416 58 l20 -24" />
			<line x1="88" y1="292" x2="552" y2="292" />
		{:else if flavour === 'peanut'}
			<!-- Peanut Shells -->
			<g transform="translate(220 236) scale(1.05)">
				<path d="M-96 6 C-96 -30 -58 -42 -28 -26 C-12 -16 -2 -16 14 -24 C52 -44 104 -22 104 12 C104 40 62 48 26 34 C10 26 0 26 -14 34 C-50 48 -96 36 -96 6 Z" />
				<path d="M-6 -22 C2 -6 4 10 0 30" />
			</g>
			<g transform="translate(455 248) scale(0.72)">
				<path d="M-96 6 C-96 -30 -58 -42 -28 -26 C-12 -16 -2 -16 14 -24 C52 -44 104 -22 104 12 C104 40 62 48 26 34 C10 26 0 26 -14 34 C-50 48 -96 36 -96 6 Z" />
				<path d="M-6 -22 C2 -6 4 10 0 30" />
			</g>
			<line x1="88" y1="292" x2="552" y2="292" />
		{/if}
	</g>

	<!-- Flavour Name Title -->
	<text
		x="600"
		y="930"
		text-anchor="middle"
		font-family="'Manrope', sans-serif"
		font-weight="900"
		font-size="76"
		letter-spacing="-0.02em"
		fill="var(--color-primary)"
		class="pack-svg-text"
	>
		{FLAVOUR_DATA[flavour].title}
	</text>

	<!-- "spread" subtitle -->
	<text
		x="600"
		y="995"
		text-anchor="middle"
		font-family="'Manrope', sans-serif"
		font-weight="600"
		font-size="42"
		letter-spacing="0.04em"
		fill="var(--color-primary)"
		opacity="0.85"
		class="pack-svg-text"
	>
		spread
	</text>

	<!-- Bottom Peel Bar with Curved Bottom Corners -->
	<path
		d="M 0 1420 H 1200 V 1552 A 48 48 0 0 1 1152 1600 H 48 A 48 48 0 0 1 0 1552 Z"
		fill="var(--color-primary)"
		class="pack-peel-bar"
	/>

	<text
		x="600"
		y="1525"
		text-anchor="middle"
		font-family="'Manrope', sans-serif"
		font-weight="900"
		font-size="48"
		letter-spacing="0.08em"
		fill="var(--color-tertiary)"
		class="pack-peel-text"
	>
		PEEL. PRESS. TOAST.
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
