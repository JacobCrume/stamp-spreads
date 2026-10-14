<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		primaryColor: string;
	}

	let { primaryColor }: Props = $props();

	let visible = $state(false);
	let isHovered = $state(false);
	let isPressed = $state(false);

	let hasPointer = $state(false);

	// Target element bounding box when hovering interactive elements
	let targetElement: HTMLElement | null = null;
	let targetRect = {
		x: 0,
		y: 0,
		width: 0,
		height: 0,
		radius: 999
	};

	// Mouse coords
	let mouseX = 0;
	let mouseY = 0;
	let prevMouseX = 0;
	let prevMouseY = 0;

	// Animated cursor blob state
	let blobX = $state(-100);
	let blobY = $state(-100);
	let blobWidth = $state(32);
	let blobHeight = $state(32);
	let blobRadius = $state(999);
	let blobScaleX = $state(1);
	let blobScaleY = $state(1);
	let blobAngle = $state(0);
	let blobOpacity = $state(1);

	onMount(() => {
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
				blobX = mouseX;
				blobY = mouseY;
				prevMouseX = mouseX;
				prevMouseY = mouseY;
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

			// Strict interactive selector: buttons, links, inputs, and the round flip button.
			// EXCLUDES packaging cards, SVG images, or text containers.
			const interactive = target.closest(
				'a, button, [role="button"], input, select, textarea, .round-flip-btn'
			) as HTMLElement | null;

			// Explicitly ignore any packaging cards or svgs if erroneously captured
			if (interactive && (interactive.closest('.flip-stage') && !interactive.classList.contains('round-flip-btn'))) {
				return;
			}

			if (interactive) {
				if (targetElement && targetElement !== interactive) {
					targetElement.classList.remove('morph-cursor-hovered');
				}
				targetElement = interactive;
				targetElement.classList.add('morph-cursor-hovered');
				isHovered = true;

				const r = interactive.getBoundingClientRect();
				const computed = window.getComputedStyle(interactive);
				const br = parseFloat(computed.borderRadius) || 16;

				targetRect = {
					x: r.left,
					y: r.top,
					width: r.width,
					height: r.height,
					radius: Math.min(br, r.height / 2)
				};
			} else {
				if (targetElement) {
					targetElement.classList.remove('morph-cursor-hovered');
					targetElement = null;
				}
				isHovered = false;
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
			// Calculate velocity for fluid stretching when freely moving
			const dx = mouseX - prevMouseX;
			const dy = mouseY - prevMouseY;
			const speed = Math.sqrt(dx * dx + dy * dy);
			prevMouseX = mouseX;
			prevMouseY = mouseY;

			if (isHovered && targetElement) {
				// Keep track of moving targets (e.g. while scrolling)
				const r = targetElement.getBoundingClientRect();
				const computed = window.getComputedStyle(targetElement);
				const br = parseFloat(computed.borderRadius) || 16;

				targetRect.x = r.left;
				targetRect.y = r.top;
				targetRect.width = r.width;
				targetRect.height = r.height;
				targetRect.radius = Math.min(br, r.height / 2);

				// Morph cursor directly into the shape and coordinates of the target element
				const targetCenterX = targetRect.x + targetRect.width / 2;
				const targetCenterY = targetRect.y + targetRect.height / 2;

				blobX += (targetCenterX - blobX) * 0.28;
				blobY += (targetCenterY - blobY) * 0.28;
				blobWidth += (targetRect.width - blobWidth) * 0.28;
				blobHeight += (targetRect.height - blobHeight) * 0.28;
				blobRadius += (targetRect.radius - blobRadius) * 0.28;

				// Neutralize stretching while locked onto element
				blobScaleX += (1 - blobScaleX) * 0.3;
				blobScaleY += (1 - blobScaleY) * 0.3;
				blobAngle += (0 - blobAngle) * 0.3;
				blobOpacity += (0.92 - blobOpacity) * 0.25;
			} else {
				// Fluid velocity-based jelly stretch along cursor trajectory
				const baseSize = isPressed ? 24 : 32;
				const stretch = Math.min(speed * 0.018, 0.45);
				const currentAngle = speed > 1 ? Math.atan2(dy, dx) : blobAngle;

				blobX += (mouseX - blobX) * 0.24;
				blobY += (mouseY - blobY) * 0.24;
				blobWidth += (baseSize - blobWidth) * 0.22;
				blobHeight += (baseSize - blobHeight) * 0.22;
				blobRadius += (999 - blobRadius) * 0.22;

				const targetScaleX = 1 + stretch;
				const targetScaleY = 1 / (1 + stretch);

				blobScaleX += (targetScaleX - blobScaleX) * 0.2;
				blobScaleY += (targetScaleY - blobScaleY) * 0.2;
				blobAngle += (currentAngle - blobAngle) * 0.25;
				blobOpacity += (1 - blobOpacity) * 0.2;
			}

			animId = requestAnimationFrame(tick);
		};

		animId = requestAnimationFrame(tick);

		return () => {
			cancelAnimationFrame(animId);
			if (targetElement) {
				targetElement.classList.remove('morph-cursor-hovered');
			}
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
	<!-- Single Fluid Morphing Cursor (No Inner Dot, Morphs into Interactive Components) -->
	<div
		class="morph-cursor-layer"
		class:is-visible={visible}
		class:is-hovered={isHovered}
		class:is-pressed={isPressed}
		aria-hidden="true"
	>
		<div
			class="fluid-cursor-blob"
			style="
				transform: translate3d({blobX - blobWidth / 2}px, {blobY - blobHeight / 2}px, 0) rotate({blobAngle}rad) scale({blobScaleX}, {blobScaleY});
				width: {blobWidth}px;
				height: {blobHeight}px;
				border-radius: {blobRadius}px;
				background-color: {primaryColor};
				opacity: {blobOpacity};
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

	.morph-cursor-layer {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: 10000;
		opacity: 0;
		transition: opacity 0.25s ease;
		overflow: hidden;
	}

	.morph-cursor-layer.is-visible {
		opacity: 1;
	}

	.fluid-cursor-blob {
		position: absolute;
		top: 0;
		left: 0;
		pointer-events: none;
		will-change: transform, width, height, border-radius, opacity;
		transform-origin: center center;
		transition: background-color 0.45s ease;
	}

	/* When cursor is freely moving, it's a solid, vibrant brand fluid pill */
	.morph-cursor-layer:not(.is-hovered) .fluid-cursor-blob {
		mix-blend-mode: normal;
	}

	/* When morphing into an interactive component, place it seamlessly behind the component's label/icon */
	.morph-cursor-layer.is-hovered .fluid-cursor-blob {
		mix-blend-mode: normal;
		filter: drop-shadow(0 8px 24px rgba(0, 0, 0, 0.28));
	}

	/* INTERACTIVE HOVERED STATES ACROSS THE SITE:
	   Elements adopt their hovered state when cursor morphs into them */
	:global(a.morph-cursor-hovered),
	:global(button.morph-cursor-hovered),
	:global(.round-flip-btn.morph-cursor-hovered),
	:global(.hero-btn-primary.morph-cursor-hovered),
	:global(.hero-btn-secondary.morph-cursor-hovered),
	:global(.flat-action-btn.morph-cursor-hovered),
	:global(.flat-outline-btn.morph-cursor-hovered),
	:global(.chat-btn.morph-cursor-hovered),
	:global(.nav-link.morph-cursor-hovered) {
		position: relative;
		z-index: 10001 !important;
		transform: scale(1.05) !important;
		transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.25s ease, background-color 0.25s ease !important;
	}

	/* Buttons with primary backgrounds invert to high contrast when hovered */
	:global(.hero-btn-primary.morph-cursor-hovered),
	:global(.flat-action-btn.morph-cursor-hovered),
	:global(.chat-btn.morph-cursor-hovered) {
		background-color: #ffffff !important;
		color: #240340 !important;
	}

	/* Tertiary / outline buttons switch to primary background with tertiary text */
	:global(.hero-btn-secondary.morph-cursor-hovered),
	:global(.flat-outline-btn.morph-cursor-hovered),
	:global(.round-flip-btn.morph-cursor-hovered) {
		background-color: var(--color-primary) !important;
		color: var(--color-tertiary) !important;
	}

	/* Nav links brighten on hover */
	:global(.nav-link.morph-cursor-hovered) {
		color: #ffffff !important;
	}
</style>
