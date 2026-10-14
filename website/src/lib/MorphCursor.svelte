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

	// Animated cursor dot/pill state
	let blobX = $state(-100);
	let blobY = $state(-100);
	let blobWidth = $state(22);
	let blobHeight = $state(22);
	let blobRadius = $state(999);
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

		// Extended magnetic snap margin (40px)
		const SNAP_MARGIN = 40;

		const findInteractiveTarget = (mx: number, my: number): HTMLElement | null => {
			const candidates = document.querySelectorAll<HTMLElement>(
				'a, button, [role="button"], .round-flip-btn, .chat-launcher, .nav-link, .footer-link-btn'
			);

			let bestMatch: HTMLElement | null = null;
			let minDistance = Infinity;

			for (let i = 0; i < candidates.length; i++) {
				const el = candidates[i];
				// Exclude non-interactive packaging cards
				if (el.closest('.flip-stage') && !el.classList.contains('round-flip-btn')) continue;
				// Exclude internal chat message area
				if (el.closest('.chat-messages') || el.closest('.chat-input-bar')) continue;

				const r = el.getBoundingClientRect();
				if (
					mx >= r.left - SNAP_MARGIN &&
					mx <= r.right + SNAP_MARGIN &&
					my >= r.top - SNAP_MARGIN &&
					my <= r.bottom + SNAP_MARGIN
				) {
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

				const targetCenterX = targetRect.x + targetRect.width / 2;
				const targetCenterY = targetRect.y + targetRect.height / 2;

				// Slower, graceful morph interpolation (0.14 rate)
				blobX += (targetCenterX - blobX) * 0.14;
				blobY += (targetCenterY - blobY) * 0.14;
				blobWidth += (targetRect.width - blobWidth) * 0.14;
				blobHeight += (targetRect.height - blobHeight) * 0.14;
				blobRadius += (targetRect.radius - blobRadius) * 0.14;
				blobOpacity += (1 - blobOpacity) * 0.14;
			} else {
				if (targetElement) {
					targetElement.classList.remove('morph-cursor-hovered');
					targetElement = null;
				}
				isHovered = false;

				// Free travel: perfectly crisp, clean solid circular cursor dot (no fluid wobble or bubble stretch)
				const baseSize = isPressed ? 18 : 22;

				blobX += (mouseX - blobX) * 0.18;
				blobY += (mouseY - blobY) * 0.18;
				blobWidth += (baseSize - blobWidth) * 0.14;
				blobHeight += (baseSize - blobHeight) * 0.14;
				blobRadius += (999 - blobRadius) * 0.14;
				blobOpacity += (1 - blobOpacity) * 0.14;
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
	<!-- Morphing Cursor Layer: z-index 10000 ensures it sits over the header, but underneath active text/icons -->
	<div
		class="morph-cursor-layer"
		class:is-visible={visible}
		class:is-hovered={isHovered}
		class:is-pressed={isPressed}
		aria-hidden="true"
	>
		<div
			class="clean-cursor-blob"
			style="
				transform: translate3d({blobX - blobWidth / 2}px, {blobY - blobHeight / 2}px, 0);
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

	/* High z-index (10000) so it morphs directly over top of the fixed floating header (z-index 1000)
	   while interactive content text/icons sit at z-index 10001 */
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

	.clean-cursor-blob {
		position: absolute;
		top: 0;
		left: 0;
		pointer-events: none;
		will-change: transform, width, height, border-radius;
		transition: background-color 0.4s ease;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
	}

	/* INTERACTIVE HOVERED STATES:
	   Text, labels, and icons sit visibly above the morphed cursor shape (z-index 10001),
	   and all interactive components adopt their brand-specific background colors (never white) */
	:global(a.morph-cursor-hovered),
	:global(button.morph-cursor-hovered),
	:global(.round-flip-btn.morph-cursor-hovered),
	:global(.hero-btn-primary.morph-cursor-hovered),
	:global(.hero-btn-secondary.morph-cursor-hovered),
	:global(.flat-action-btn.morph-cursor-hovered),
	:global(.flat-outline-btn.morph-cursor-hovered),
	:global(.chat-btn.morph-cursor-hovered),
	:global(.chat-launcher.morph-cursor-hovered),
	:global(.nav-link.morph-cursor-hovered),
	:global(.footer-links a.morph-cursor-hovered),
	:global(.footer-link-btn.morph-cursor-hovered) {
		position: relative;
		z-index: 10001 !important;
		transform: scale(1.05) !important;
		transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.25s ease, background-color 0.25s ease !important;
	}

	/* Primary action buttons shift to tertiary surface with primary text */
	:global(.hero-btn-primary.morph-cursor-hovered),
	:global(.flat-action-btn.morph-cursor-hovered),
	:global(.chat-btn.morph-cursor-hovered),
	:global(.chat-launcher.morph-cursor-hovered) {
		background-color: var(--color-tertiary) !important;
		color: var(--color-primary) !important;
	}

	/* Tertiary buttons and round flip buttons switch to primary background with tertiary text */
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

	/* Footer links gain an elevated brand background pill with high-contrast text */
	:global(.footer-links a.morph-cursor-hovered),
	:global(.footer-link-btn.morph-cursor-hovered) {
		background-color: var(--color-primary) !important;
		color: var(--color-tertiary) !important;
	}
</style>
