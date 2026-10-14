<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		primaryColor: string;
	}

	let { primaryColor }: Props = $props();

	let visible = $state(false);
	let isHovered = $state(false);
	let isPressed = $state(false);
	let hoverText = $state('');

	// Target element bounds for morphing
	let morphRect = $state<{
		x: number;
		y: number;
		width: number;
		height: number;
		radius: number;
	} | null>(null);

	// Mouse coords
	let mouseX = 0;
	let mouseY = 0;

	// Animated follower positions
	let dotX = $state(-100);
	let dotY = $state(-100);
	let blobX = $state(-100);
	let blobY = $state(-100);
	let blobWidth = $state(40);
	let blobHeight = $state(40);
	let blobRadius = $state(999);

	let hasPointer = $state(false);

	onMount(() => {
		// Only enable custom cursor if fine pointer (mouse/trackpad), not touch screens
		if (typeof window === 'undefined') return;
		const media = window.matchMedia('(pointer: fine)');
		if (!media.matches) return;

		hasPointer = true;
		document.documentElement.classList.add('custom-cursor-active');

		const onMouseMove = (e: MouseEvent) => {
			mouseX = e.clientX;
			mouseY = e.clientY;
			if (!visible) {
				visible = true;
				dotX = mouseX;
				dotY = mouseY;
				blobX = mouseX;
				blobY = mouseY;
			}
		};

		const onMouseDown = () => {
			isPressed = true;
		};

		const onMouseUp = () => {
			isPressed = false;
		};

		const onMouseLeave = () => {
			visible = false;
		};

		const onMouseEnter = () => {
			visible = true;
		};

		// Check hovered element
		const onMouseOver = (e: MouseEvent) => {
			const target = e.target as HTMLElement | null;
			if (!target) return;

			// Look for clickable / interactive elements: button, a, input, select, textarea, [role=button], .round-flip-btn
			const interactive = target.closest(
				'a, button, [role="button"], input, select, textarea, .round-flip-btn, .flip-card, .flat-flip-trigger'
			) as HTMLElement | null;

			if (interactive) {
				isHovered = true;
				const r = interactive.getBoundingClientRect();
				const computed = window.getComputedStyle(interactive);
				const br = parseFloat(computed.borderRadius) || 16;

				morphRect = {
					x: r.left,
					y: r.top,
					width: r.width,
					height: r.height,
					radius: Math.min(br, r.height / 2)
				};

				// Custom label if defined (e.g. data-cursor="Flip")
				hoverText = interactive.getAttribute('data-cursor') || '';
			} else {
				isHovered = false;
				morphRect = null;
				hoverText = '';
			}
		};

		window.addEventListener('mousemove', onMouseMove, { passive: true });
		window.addEventListener('mousedown', onMouseDown);
		window.addEventListener('mouseup', onMouseUp);
		document.addEventListener('mouseover', onMouseOver, { passive: true });
		document.documentElement.addEventListener('mouseleave', onMouseLeave);
		document.documentElement.addEventListener('mouseenter', onMouseEnter);

		let animId: number;
		const tick = () => {
			// Dot directly tracks mouse
			dotX += (mouseX - dotX) * 0.45;
			dotY += (mouseY - dotY) * 0.45;

			if (morphRect && isHovered) {
				// Morph and magnetically wrap around the interactive element
				const targetWidth = morphRect.width + 12;
				const targetHeight = morphRect.height + 12;
				const targetCenterX = morphRect.x + morphRect.width / 2;
				const targetCenterY = morphRect.y + morphRect.height / 2;

				blobX += (targetCenterX - blobX) * 0.22;
				blobY += (targetCenterY - blobY) * 0.22;
				blobWidth += (targetWidth - blobWidth) * 0.22;
				blobHeight += (targetHeight - blobHeight) * 0.22;
				blobRadius += (morphRect.radius + 6 - blobRadius) * 0.22;
			} else {
				// Default floating goo circle trailing with organic spring
				const baseSize = isPressed ? 28 : 38;
				blobX += (mouseX - blobX) * 0.18;
				blobY += (mouseY - blobY) * 0.18;
				blobWidth += (baseSize - blobWidth) * 0.2;
				blobHeight += (baseSize - blobHeight) * 0.2;
				blobRadius += (999 - blobRadius) * 0.2;
			}

			animId = requestAnimationFrame(tick);
		};

		animId = requestAnimationFrame(tick);

		return () => {
			cancelAnimationFrame(animId);
			document.documentElement.classList.remove('custom-cursor-active');
			window.removeEventListener('mousemove', onMouseMove);
			window.removeEventListener('mousedown', onMouseDown);
			window.removeEventListener('mouseup', onMouseUp);
			document.removeEventListener('mouseover', onMouseOver);
			document.documentElement.removeEventListener('mouseleave', onMouseLeave);
			document.documentElement.removeEventListener('mouseenter', onMouseEnter);
		};
	});
</script>

{#if hasPointer}
	<!-- Gooey/Morphing Custom Cursor Container -->
	<div
		class="morph-cursor-container"
		class:is-visible={visible}
		class:is-hovered={isHovered}
		class:is-pressed={isPressed}
		aria-hidden="true"
	>
		<!-- SVG Gooey Filter -->
		<svg class="cursor-goo-filter" xmlns="http://www.w3.org/2000/svg" version="1.1">
			<defs>
				<filter id="goo">
					<feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur" />
					<feColorMatrix
						in="blur"
						mode="matrix"
						values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 20 -8"
						result="goo"
					/>
					<feComposite in="SourceGraphic" in2="goo" operator="atop" />
				</filter>
			</defs>
		</svg>

		<!-- Outer Gooey Morphing Pill/Blob -->
		<div
			class="cursor-blob"
			style="
				transform: translate3d({blobX - blobWidth / 2}px, {blobY - blobHeight / 2}px, 0);
				width: {blobWidth}px;
				height: {blobHeight}px;
				border-radius: {blobRadius}px;
				background-color: {primaryColor};
			"
		>
			{#if hoverText}
				<span class="cursor-label">{hoverText}</span>
			{/if}
		</div>

		<!-- Precise Inner Dot -->
		<div
			class="cursor-dot"
			style="
				transform: translate3d({dotX - 4}px, {dotY - 4}px, 0);
				background-color: {primaryColor};
			"
		></div>
	</div>
{/if}

<style>
	:global(html.custom-cursor-active),
	:global(html.custom-cursor-active body),
	:global(html.custom-cursor-active a),
	:global(html.custom-cursor-active button),
	:global(html.custom-cursor-active [role='button']) {
		cursor: none !important;
	}

	.morph-cursor-container {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: 999999;
		opacity: 0;
		transition: opacity 0.3s ease;
		overflow: hidden;
	}

	.morph-cursor-container.is-visible {
		opacity: 1;
	}

	.cursor-goo-filter {
		position: absolute;
		width: 0;
		height: 0;
		pointer-events: none;
	}

	.cursor-blob {
		position: absolute;
		top: 0;
		left: 0;
		pointer-events: none;
		will-change: transform, width, height, border-radius;
		opacity: 0.38;
		mix-blend-mode: screen;
		display: flex;
		align-items: center;
		justify-content: center;
		transition:
			opacity 0.25s ease,
			background-color 0.45s ease;
	}

	.morph-cursor-container.is-hovered .cursor-blob {
		opacity: 0.28;
	}

	.morph-cursor-container.is-pressed .cursor-blob {
		opacity: 0.55;
	}

	.cursor-dot {
		position: absolute;
		top: 0;
		left: 0;
		width: 8px;
		height: 8px;
		border-radius: 50%;
		pointer-events: none;
		will-change: transform;
		transition:
			transform 0.05s linear,
			opacity 0.2s ease,
			background-color 0.45s ease;
		box-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
	}

	.morph-cursor-container.is-hovered .cursor-dot {
		opacity: 0.8;
		transform: scale(0.65);
	}

	.morph-cursor-container.is-pressed .cursor-dot {
		transform: scale(1.3);
	}

	.cursor-label {
		font-family: 'Manrope', sans-serif;
		font-size: 0.72rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #ffffff;
		pointer-events: none;
	}
</style>
