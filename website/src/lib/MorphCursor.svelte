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

	// Currently hovered interactive element
	let targetElement: HTMLElement | null = null;
	let targetRect = {
		x: 0,
		y: 0,
		width: 0,
		height: 0,
		radius: 999
	};

	// Mouse coordinates & historical movement
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

		// Check hovered element
		const onMouseOver = (e: MouseEvent) => {
			const target = e.target as HTMLElement | null;
			if (!target) return;

			// Strict interactive selector: only actual action items
			// EXCLUDES: packaging cards, svgs, chat window/input area, containers
			const interactive = target.closest(
				'a, button, [role="button"], .round-flip-btn, .chat-launcher'
			) as HTMLElement | null;

			// Guard: If inside packaging flip-stage and NOT the flip button, ignore completely
			if (interactive && interactive.closest('.flip-stage') && !interactive.classList.contains('round-flip-btn')) {
				return;
			}

			// Guard: If inside chat message list or chat input/window, ignore
			if (interactive && (interactive.closest('.chat-messages') || interactive.closest('.chat-input-bar'))) {
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
				// Keep track of moving targets (e.g. while scrolling or floating)
				const r = targetElement.getBoundingClientRect();
				const computed = window.getComputedStyle(targetElement);
				const br = parseFloat(computed.borderRadius) || 16;

				targetRect.x = r.left;
				targetRect.y = r.top;
				targetRect.width = r.width;
				targetRect.height = r.height;
				targetRect.radius = Math.min(br, r.height / 2);

				// Snap to the target component's exact geometry behind it
				const targetCenterX = targetRect.x + targetRect.width / 2;
				const targetCenterY = targetRect.y + targetRect.height / 2;

				blobX += (targetCenterX - blobX) * 0.32;
				blobY += (targetCenterY - blobY) * 0.32;
				blobWidth += (targetRect.width - blobWidth) * 0.32;
				blobHeight += (targetRect.height - blobHeight) * 0.32;
				blobRadius += (targetRect.radius - blobRadius) * 0.32;

				// Immediately reset angle and scale to 0 and 1 so it NEVER rotates during morph
				blobAngle = 0;
				blobScaleX += (1 - blobScaleX) * 0.35;
				blobScaleY += (1 - blobScaleY) * 0.35;
				// Fade out the blob into the component so it smoothly becomes the component itself
				blobOpacity += (0 - blobOpacity) * 0.28;
			} else {
				// Free movement: Vibrant brand fluid dot that stretches slightly along direction of travel
				const baseSize = isPressed ? 22 : 30;
				const stretch = Math.min(speed * 0.015, 0.4);

				// Only calculate angle if actual motion exists, preventing jitter or weird snap rotations
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
			document.removeEventListener('mouseover', onMouseOver);
			document.documentElement.removeEventListener('mouseleave', onMouseLeave);
			document.documentElement.removeEventListener('mouseenter', onMouseEnter);
		};
	});
</script>

{#if hasPointer}
	<!-- Morphing Cursor Layer -->
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

	/* Keep cursor layer beneath the fixed floating header (z-index 1000) and chat widget (z-index 9999)
	   so it never overlays on top of text, icons, or navigation buttons */
	.morph-cursor-layer {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: 900;
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

	/* INTERACTIVE HOVERED STATES:
	   Components morph into their high-contrast active state as cursor glides in */
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
		transform: scale(1.06) !important;
		transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.22s ease, background-color 0.22s ease !important;
	}

	/* Primary action buttons shift to crisp high-contrast white */
	:global(.hero-btn-primary.morph-cursor-hovered),
	:global(.flat-action-btn.morph-cursor-hovered),
	:global(.chat-btn.morph-cursor-hovered),
	:global(.chat-launcher.morph-cursor-hovered) {
		background-color: #ffffff !important;
		color: #240340 !important;
	}

	/* Tertiary solid buttons & round flip buttons switch to electric primary background */
	:global(.hero-btn-secondary.morph-cursor-hovered),
	:global(.flat-outline-btn.morph-cursor-hovered),
	:global(.round-flip-btn.morph-cursor-hovered) {
		background-color: var(--color-primary) !important;
		color: var(--color-tertiary) !important;
	}

	/* Nav links in header brighten to pure white */
	:global(.nav-link.morph-cursor-hovered:not(.chat-btn)) {
		color: #ffffff !important;
		opacity: 1 !important;
	}
</style>
