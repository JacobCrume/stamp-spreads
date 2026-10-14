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

		// PROXY CLICK: If user clicks while an interactive target is magnetically snapped/hovered,
		// trigger that element's click action directly so clicks never miss!
		const onClick = (e: MouseEvent) => {
			if (targetElement) {
				// If the native event target wasn't already inside the targetElement, trigger it directly
				const nativeTarget = e.target as HTMLElement | null;
				if (!nativeTarget || !targetElement.contains(nativeTarget)) {
					targetElement.click();
				}
			}
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
		window.addEventListener('click', onClick);
		document.documentElement.addEventListener('mouseleave', onMouseLeave);
		document.documentElement.addEventListener('mouseenter', onMouseEnter);

		let animId: number;

		// Generous magnetic snap envelope (36px)
		const SNAP_MARGIN = 36;

		const findInteractiveTarget = (mx: number, my: number): HTMLElement | null => {
			const candidates = document.querySelectorAll<HTMLElement>(
				'a, button, [role="button"], .round-flip-btn, .chat-launcher, .nav-link, .footer-link-btn'
			);

			let bestMatch: HTMLElement | null = null;
			let minDistance = Infinity;

			for (let i = 0; i < candidates.length; i++) {
				const el = candidates[i];
				// Guard: Exclude non-interactive packaging cards
				if (el.closest('.flip-stage') && !el.classList.contains('round-flip-btn')) continue;
				// Guard: Exclude internal chat message area
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

				// Slow, graceful morph interpolation (0.12 rate)
				blobX += (targetCenterX - blobX) * 0.12;
				blobY += (targetCenterY - blobY) * 0.12;
				blobWidth += (targetRect.width - blobWidth) * 0.12;
				blobHeight += (targetRect.height - blobHeight) * 0.12;
				blobRadius += (targetRect.radius - blobRadius) * 0.12;
			} else {
				if (targetElement) {
					targetElement.classList.remove('morph-cursor-hovered');
					targetElement = null;
				}
				isHovered = false;

				// Free travel: perfectly crisp, clean circular cursor dot
				const baseSize = isPressed ? 18 : 22;

				blobX += (mouseX - blobX) * 0.18;
				blobY += (mouseY - blobY) * 0.18;
				blobWidth += (baseSize - blobWidth) * 0.14;
				blobHeight += (baseSize - blobHeight) * 0.14;
				blobRadius += (999 - blobRadius) * 0.14;
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
			window.removeEventListener('click', onClick);
			document.documentElement.removeEventListener('mouseleave', onMouseLeave);
			document.documentElement.removeEventListener('mouseenter', onMouseEnter);
		};
	});
</script>

{#if hasPointer}
	<!-- Morphing Cursor Layer:
	     Using mix-blend-mode: screen and semi-transparent fills, or transparent cutout,
	     so the cursor never covers or blacks out the button text/icons -->
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

	/* The cursor layer is fixed at z-index 99999.
	   When hovered, we use mix-blend-mode: screen / translucent fill
	   so that underneath text, wordmarks, and icons remain crystal clear */
	.morph-cursor-layer {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: 99999;
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
		transition: background-color 0.4s ease, opacity 0.25s ease;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
	}

	/* In free travel: solid vibrant cursor dot */
	.morph-cursor-layer:not(.is-hovered) .clean-cursor-blob {
		opacity: 1;
	}

	/* While morphing over a component:
	   Give it an elegant translucent glowing pill fill (opacity 0.25)
	   so it envelops the button without hiding its text or labels! */
	.morph-cursor-layer.is-hovered .clean-cursor-blob {
		opacity: 0.32;
		filter: blur(1px);
	}

	/* ALL INTERACTIVE HOVERED STATES ACROSS THE SITE:
	   Elements morph to/from a visible background using brand colors (NEVER white),
	   and scale slightly so the user clearly feels the magnetic attraction */
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
		transform: scale(1.05) !important;
		transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.22s ease, background-color 0.22s ease !important;
	}

	/* Primary action buttons shift into tertiary color with electric primary text */
	:global(.hero-btn-primary.morph-cursor-hovered),
	:global(.flat-action-btn.morph-cursor-hovered) {
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

	/* Header navigation links gain a sleek primary pill background and tertiary text */
	:global(.nav-link.morph-cursor-hovered:not(.chat-btn)) {
		background-color: var(--color-primary) !important;
		color: var(--color-tertiary) !important;
	}

	/* Header Ask Stamp chat-btn shifts to tertiary with primary text when hovered */
	:global(.chat-btn.morph-cursor-hovered) {
		background-color: var(--color-tertiary) !important;
		color: var(--color-primary) !important;
	}

	/* Bottom floating chat launcher button shifts cleanly when hovered */
	:global(.chat-launcher.morph-cursor-hovered) {
		background-color: var(--color-tertiary) !important;
		color: var(--color-primary) !important;
	}

	/* Footer links gain an elevated brand background pill with high-contrast text */
	:global(.footer-links a.morph-cursor-hovered),
	:global(.footer-link-btn.morph-cursor-hovered) {
		background-color: var(--color-primary) !important;
		color: var(--color-tertiary) !important;
	}
</style>
