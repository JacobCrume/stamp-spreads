<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		primaryColor: string;
		secondaryColor: string;
		tertiaryColor: string;
	}

	let { primaryColor, secondaryColor, tertiaryColor }: Props = $props();

	let visible = $state(false);
	let isHovered = $state(false);
	let isPressed = $state(false);
	let hasPointer = $state(false);

	// Currently tracked target element
	let targetElement: HTMLElement | null = null;
	let targetRect = {
		x: 0,
		y: 0,
		width: 0,
		height: 0,
		radius: 999
	};

	// Mouse coordinates
	let mouseX = 0;
	let mouseY = 0;
	let prevMouseX = 0;
	let prevMouseY = 0;

	// Animated cursor blob state
	let blobX = $state(-100);
	let blobY = $state(-100);
	let blobWidth = $state(30);
	let blobHeight = $state(30);
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

		window.addEventListener('mousemove', onMouseMove, { passive: true });
		window.addEventListener('mousedown', onMouseDown);
		window.addEventListener('mouseup', onMouseUp);
		document.documentElement.addEventListener('mouseleave', onMouseLeave);
		document.documentElement.addEventListener('mouseenter', onMouseEnter);

		let animId: number;

		// Interactive target detection with an extended magnetic snap threshold (32px radius)
		const SNAP_MARGIN = 28;

		const findInteractiveTarget = (mx: number, my: number): HTMLElement | null => {
			// Find all clickable candidates in viewport
			const candidates = document.querySelectorAll<HTMLElement>(
				'a, button, [role="button"], .round-flip-btn, .chat-launcher, .nav-link'
			);

			let bestMatch: HTMLElement | null = null;
			let minDistance = Infinity;

			for (let i = 0; i < candidates.length; i++) {
				const el = candidates[i];
				// Guard: Exclude packaging cards or SVG card elements
				if (el.closest('.flip-stage') && !el.classList.contains('round-flip-btn')) continue;
				// Guard: Exclude interior chat contents
				if (el.closest('.chat-messages') || el.closest('.chat-input-bar')) continue;

				const r = el.getBoundingClientRect();
				// Check if point is inside expanded bounding box
				if (
					mx >= r.left - SNAP_MARGIN &&
					mx <= r.right + SNAP_MARGIN &&
					my >= r.top - SNAP_MARGIN &&
					my <= r.bottom + SNAP_MARGIN
				) {
					// Distance to center of element
					const cx = r.left + r.width / 2;
					const cy = r.top + r.height / 2;
					const dist = Math.hypot(mx - cx, my - cy);
					if (dist < minDistance) {
						minDistance = dist;
						bestMatch = el;
					}
				}
			}

			return bestMatch;
		};

		const tick = () => {
			// Calculate velocity for natural stretching when traveling
			const dx = mouseX - prevMouseX;
			const dy = mouseY - prevMouseY;
			const speed = Math.sqrt(dx * dx + dy * dy);
			prevMouseX = mouseX;
			prevMouseY = mouseY;

			// Check for magnet targets
			const detected = findInteractiveTarget(mouseX, mouseY);

			if (detected) {
				if (targetElement && targetElement !== detected) {
					targetElement.classList.remove('morph-cursor-hovered');
				}
				targetElement = detected;
				targetElement.classList.add('morph-cursor-hovered');
				isHovered = true;

				const r = targetElement.getBoundingClientRect();
				const computed = window.getComputedStyle(targetElement);
				const br = parseFloat(computed.borderRadius) || 16;

				targetRect.x = r.left;
				targetRect.y = r.top;
				targetRect.width = r.width;
				targetRect.height = r.height;
				targetRect.radius = Math.min(br, r.height / 2);

				// Fluidly morph cursor dimensions and position into the target component
				const targetCenterX = targetRect.x + targetRect.width / 2;
				const targetCenterY = targetRect.y + targetRect.height / 2;

				blobX += (targetCenterX - blobX) * 0.28;
				blobY += (targetCenterY - blobY) * 0.28;
				blobWidth += (targetRect.width - blobWidth) * 0.28;
				blobHeight += (targetRect.height - blobHeight) * 0.28;
				blobRadius += (targetRect.radius - blobRadius) * 0.28;

				// While morphing into a component, lock angle and scale to 0 and 1 (no rotation during morph)
				blobAngle = 0;
				blobScaleX += (1 - blobScaleX) * 0.3;
				blobScaleY += (1 - blobScaleY) * 0.3;
				// Maintain full solid presence as the component's back fill
				blobOpacity += (1 - blobOpacity) * 0.3;
			} else {
				if (targetElement) {
					targetElement.classList.remove('morph-cursor-hovered');
					targetElement = null;
				}
				isHovered = false;

				// Free travel: vibrant fluid dot that stretches slightly along direction of travel
				const baseSize = isPressed ? 22 : 30;
				const stretch = Math.min(speed * 0.015, 0.4);

				// Only calculate angle if real motion exists to avoid jitter
				if (speed > 2.5) {
					blobAngle = Math.atan2(dy, dx);
				}

				blobX += (mouseX - blobX) * 0.26;
				blobY += (mouseY - blobY) * 0.26;
				blobWidth += (baseSize - blobWidth) * 0.24;
				blobHeight += (baseSize - blobHeight) * 0.24;
				blobRadius += (999 - blobRadius) * 0.24;

				const targetScaleX = 1 + stretch;
				const targetScaleY = 1 / (1 + stretch);

				blobScaleX += (targetScaleX - blobScaleX) * 0.22;
				blobScaleY += (targetScaleY - blobScaleY) * 0.22;
				blobOpacity += (1 - blobOpacity) * 0.25;
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
			document.documentElement.removeEventListener('mouseleave', onMouseLeave);
			document.documentElement.removeEventListener('mouseenter', onMouseEnter);
		};
	});
</script>

{#if hasPointer}
	<!-- Morphing Cursor Layer: Sits behind component text/icons (z-index 990) so it morphs seamlessly into the component's background -->
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
				transform: translate3d({blobX - blobWidth / 2}px, {blobY - blobHeight / 2}px, 0) {isHovered ? '' : `rotate(${blobAngle}rad)`} scale({blobScaleX}, {blobScaleY});
				width: {blobWidth}px;
				height: {blobHeight}px;
				border-radius: {blobRadius}px;
				background-color: {isHovered ? tertiaryColor : primaryColor};
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
		z-index: 990;
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
		transition: background-color 0.4s ease;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.22);
	}

	/* ALL INTERACTIVE HOVERED STATES:
	   Elements morph to/from a visible background using authentic palette colors (NEVER white),
	   with their text/icons sitting clearly above the morphed cursor shape */
	:global(a.morph-cursor-hovered),
	:global(button.morph-cursor-hovered),
	:global(.round-flip-btn.morph-cursor-hovered),
	:global(.hero-btn-primary.morph-cursor-hovered),
	:global(.hero-btn-secondary.morph-cursor-hovered),
	:global(.flat-action-btn.morph-cursor-hovered),
	:global(.flat-outline-btn.morph-cursor-hovered),
	:global(.chat-btn.morph-cursor-hovered),
	:global(.chat-launcher.morph-cursor-hovered),
	:global(.nav-link.morph-cursor-hovered) {
		position: relative;
		z-index: 1005 !important;
		transform: scale(1.05) !important;
		transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.22s ease, background-color 0.22s ease !important;
	}

	/* Primary action buttons shift into tertiary color with electric primary text */
	:global(.hero-btn-primary.morph-cursor-hovered),
	:global(.flat-action-btn.morph-cursor-hovered),
	:global(.chat-btn.morph-cursor-hovered),
	:global(.chat-launcher.morph-cursor-hovered) {
		background-color: var(--color-tertiary) !important;
		color: var(--color-primary) !important;
	}

	/* Tertiary buttons and round-flip buttons switch to electric primary background with tertiary icons/text */
	:global(.hero-btn-secondary.morph-cursor-hovered),
	:global(.flat-outline-btn.morph-cursor-hovered),
	:global(.round-flip-btn.morph-cursor-hovered) {
		background-color: var(--color-primary) !important;
		color: var(--color-tertiary) !important;
	}

	/* Header navigation links gain a sleek tertiary pill background and vibrant primary text */
	:global(.nav-link.morph-cursor-hovered:not(.chat-btn)) {
		background-color: var(--color-primary) !important;
		color: var(--color-tertiary) !important;
	}
</style>
