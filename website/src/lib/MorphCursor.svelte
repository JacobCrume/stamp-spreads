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

	// Animated cursor pill state
	let blobX = $state(-100);
	let blobY = $state(-100);
	let blobWidth = $state(20);
	let blobHeight = $state(20);
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

		// Proxy Click: Clicking anywhere while an element is magnetically morphed clicks it directly
		const onClick = (e: MouseEvent) => {
			if (targetElement) {
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

		// 36px magnetic attraction radius
		const SNAP_MARGIN = 36;

		const findInteractiveTarget = (mx: number, my: number): HTMLElement | null => {
			const candidates = document.querySelectorAll<HTMLElement>(
				'a, button, [role="button"], .round-flip-btn, .chat-launcher, .nav-link, .footer-links a, .footer-link-btn'
			);

			let bestMatch: HTMLElement | null = null;
			let minDistance = Infinity;

			for (let i = 0; i < candidates.length; i++) {
				const el = candidates[i];
				// Guard: Exclude packaging cards or SVG card elements
				if (el.closest('.flip-stage') && !el.classList.contains('round-flip-btn')) continue;
				// Guard: Exclude internal chat messages
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

				// Smooth morph interpolation into element bounds
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

				// Free travel: solid circular dot
				const baseSize = isPressed ? 16 : 20;

				blobX += (mouseX - blobX) * 0.18;
				blobY += (mouseY - blobY) * 0.18;
				blobWidth += (baseSize - blobWidth) * 0.12;
				blobHeight += (baseSize - blobHeight) * 0.12;
				blobRadius += (999 - blobRadius) * 0.12;
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
	     When not hovered: solid cursor dot moving across page.
	     When hovered: morphs into the exact shape & position of the target element,
	     and sits BEHIND its text/icons using an inverse blend cutout or clean background fill. -->
	<div
		class="morph-cursor-layer"
		class:is-visible={visible}
		class:is-hovered={isHovered}
		class:is-pressed={isPressed}
		aria-hidden="true"
	>
		<div
			class="morph-cursor-pill"
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

	/* Place cursor layer at z-index 10000 so it morphs on top of background headers (1000),
	   but underneath interactive component text/icons (10001) */
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

	.morph-cursor-pill {
		position: absolute;
		top: 0;
		left: 0;
		pointer-events: none;
		will-change: transform, width, height, border-radius;
		transition: background-color 0.4s ease;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.22);
	}

	/* In free movement: vibrant brand cursor dot */
	.morph-cursor-layer:not(.is-hovered) .morph-cursor-pill {
		background-color: var(--color-primary);
	}

	/* While morphing over a component:
	   It becomes the solid background of the button! */
	.morph-cursor-layer.is-hovered .morph-cursor-pill {
		opacity: 1;
	}

	/* ALL INTERACTIVE ELEMENTS:
	   Ensure their text and contents sit at z-index 10002 above the morph-cursor-pill (10000),
	   and transparentize their own static background so the morphed cursor shape IS their background! */
	:global(.morph-cursor-hovered) {
		position: relative;
		z-index: 10002 !important;
		transform: scale(1.05) !important;
		background-color: transparent !important;
		transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.22s ease !important;
	}

	/* Content of hovered elements stays razor-sharp:
	   Primary buttons, nav-link, chat-btn text and icons show in bright electric primary color over the morphed tertiary pill */
	:global(.hero-btn-primary.morph-cursor-hovered),
	:global(.flat-action-btn.morph-cursor-hovered),
	:global(.chat-btn.morph-cursor-hovered),
	:global(.chat-launcher.morph-cursor-hovered),
	:global(.nav-link.morph-cursor-hovered),
	:global(.footer-links a.morph-cursor-hovered),
	:global(.footer-link-btn.morph-cursor-hovered) {
		color: var(--color-primary) !important;
		text-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
	}

	:global(.hero-btn-secondary.morph-cursor-hovered),
	:global(.flat-outline-btn.morph-cursor-hovered),
	:global(.round-flip-btn.morph-cursor-hovered) {
		color: var(--color-primary) !important;
	}
</style>
