<script lang="ts">
	import { onMount, onDestroy, tick } from 'svelte';
	import { marked } from 'marked';
	import { colorScheme } from './theme.svelte';

	marked.setOptions({
		gfm: true,
		breaks: true
	});

	function renderMarkdown(raw: string): string {
		if (!raw) return '';
		try {
			return marked.parse(raw) as string;
		} catch {
			return raw;
		}
	}

	interface Message {
		id: number;
		sender: 'user' | 'bot';
		text: string;
		timestamp: string;
	}

	let isOpen = $state(false);
	let userInput = $state('');
	let isThinking = $state(false);

	let messagesContainer: HTMLDivElement | null = $state(null);
	let inputElement: HTMLInputElement | null = $state(null);
	let barElement: HTMLDivElement | null = $state(null);

	let messages: Message[] = $state([
		{
			id: 1,
			sender: 'bot',
			text: "Kia ora! I'm Stamp's assistant. Ask me anything about our peel-and-press toast spreads, launch flavours, allergens, pricing ($5.00 NZD / sheet), or how to apply Stamp.",
			timestamp: 'Just now'
		}
	]);

	const quickQuestions = [
		'What is Stamp?',
		'How do I use it?',
		'4 Launch Flavours',
		'Allergens info',
		'Pantry shelf life'
	];

	function getTimeString() {
		const now = new Date();
		return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	}

	async function scrollToBottom() {
		await tick();
		if (messagesContainer) {
			messagesContainer.scrollTop = messagesContainer.scrollHeight;
		}
	}

	function expandBar() {
		if (!isOpen) {
			isOpen = true;
			scrollToBottom();
			setTimeout(() => inputElement?.focus(), 150);
		}
	}

	function collapseBar() {
		isOpen = false;
	}

	let handleOpenChat: (() => void) | null = null;
	let handleClickOutside: ((e: MouseEvent) => void) | null = null;

	onMount(() => {
		if (typeof window !== 'undefined') {
			const url = new URL(window.location.href);
			if (url.searchParams.get('chat') === 'open' || window.location.hash === '#chat') {
				isOpen = true;
			}

			handleOpenChat = () => {
				isOpen = true;
				scrollToBottom();
				setTimeout(() => inputElement?.focus(), 150);
			};
			window.addEventListener('stamp:open-chat', handleOpenChat);

			// Hide chat responses when clicking away from the bar
			handleClickOutside = (e: MouseEvent) => {
				if (!isOpen) return;
				const target = e.target as HTMLElement | null;
				if (!target) return;

				// If click was inside the bar container or popup, keep open
				if (barElement && barElement.contains(target)) {
					return;
				}

				collapseBar();
			};
			document.addEventListener('click', handleClickOutside);
		}
	});

	onDestroy(() => {
		if (typeof window !== 'undefined') {
			if (handleOpenChat) window.removeEventListener('stamp:open-chat', handleOpenChat);
			if (handleClickOutside) document.removeEventListener('click', handleClickOutside);
		}
	});

	async function handleSend(textToSend?: string) {
		const query = (textToSend || userInput).trim();
		if (!query || isThinking) return;

		const userMsg: Message = {
			id: Date.now(),
			sender: 'user',
			text: query,
			timestamp: getTimeString()
		};
		messages.push(userMsg);
		userInput = '';
		isThinking = true;
		isOpen = true;
		scrollToBottom();

		const history = messages
			.filter((m) => m.id !== userMsg.id)
			.slice(-6)
			.map((m) => ({
				role: m.sender === 'user' ? 'user' : 'assistant',
				content: m.text
			}));

		try {
			const res = await fetch('/api/chat', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ message: query, history })
			});

			if (res.ok) {
				const data = await res.json();
				messages.push({
					id: Date.now() + 1,
					sender: 'bot',
					text: data.answer,
					timestamp: getTimeString()
				});
			} else {
				messages.push({
					id: Date.now() + 1,
					sender: 'bot',
					text: "I couldn't reach the server right now. Stamp is a 10 g peel-and-press spread disc for hot toast ($5.00 NZD / sheet). Please try again shortly.",
					timestamp: getTimeString()
				});
			}
		} catch {
			messages.push({
				id: Date.now() + 1,
				sender: 'bot',
				text: "Network connection error. Stamp discs are 10 g each, 8 per sheet for $5.00 NZD. Feel free to re-ask your question.",
				timestamp: getTimeString()
			});
		} finally {
			isThinking = false;
			scrollToBottom();
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			handleSend();
		} else if (e.key === 'Escape') {
			collapseBar();
		}
	}
</script>

<!-- FIXED BOTTOM CHAT BAR DOCKED AT SCREEN BOTTOM IN SAME COLOR AS HEADER (TERTIARY BG) -->
<div class="bottom-chat-wrapper" bind:this={barElement}>
	<!-- CHAT RESPONSES FLYOUT (APPEARS ABOVE THE BAR) -->
	{#if isOpen}
		<div
			class="responses-flyout"
			role="dialog"
			aria-label="Stamp Conversation"
			style:background-color={colorScheme.tertiary}
		>
			<!-- Top Header of the Flyout -->
			<div class="flyout-header" style:color={colorScheme.primary}>
				<div class="flyout-title-wrap">
					<span class="bot-badge-small" style:background-color={colorScheme.primary} style:color={colorScheme.tertiary}>S</span>
					<div class="flyout-title">
						<strong>Stamp Assistant</strong>
						<span class="online-pill">
							<span class="online-dot" style:background-color={colorScheme.primary}></span>
							Live
						</span>
					</div>
				</div>
				<button
					type="button"
					class="close-flyout-btn"
					onclick={collapseBar}
					aria-label="Close responses"
					style:color={colorScheme.primary}
				>
					✕
				</button>
			</div>

			<!-- Quick Chips -->
			<div class="flyout-chips">
				{#each quickQuestions as q}
					<button
						type="button"
						class="chip-pill"
						onclick={() => handleSend(q)}
						disabled={isThinking}
						style:color={colorScheme.primary}
						style:background-color="rgba(255, 255, 255, 0.08)"
					>
						{q}
					</button>
				{/each}
			</div>

			<!-- Scrollable Messages Window -->
			<div class="flyout-messages" bind:this={messagesContainer}>
				{#each messages as msg (msg.id)}
					<div class="msg-row {msg.sender}">
						{#if msg.sender === 'bot'}
							<div class="bot-icon" style:background-color={colorScheme.primary} style:color={colorScheme.tertiary}>S</div>
						{/if}
						<div
							class="msg-bubble {msg.sender}"
							style:background-color={msg.sender === 'user' ? colorScheme.primary : 'rgba(255, 255, 255, 0.1)'}
							style:color={msg.sender === 'user' ? colorScheme.tertiary : '#ffffff'}
						>
							<div class="msg-text prose">
								{@html renderMarkdown(msg.text)}
							</div>
							<div class="msg-time" style:color={msg.sender === 'user' ? colorScheme.tertiary : colorScheme.primary}>
								{msg.timestamp}
							</div>
						</div>
					</div>
				{/each}

				{#if isThinking}
					<div class="msg-row bot">
						<div class="bot-icon" style:background-color={colorScheme.primary} style:color={colorScheme.tertiary}>S</div>
						<div class="msg-bubble bot thinking" style:background-color="rgba(255, 255, 255, 0.1)">
							<span class="thinking-dot" style:background-color={colorScheme.primary}></span>
							<span class="thinking-dot" style:background-color={colorScheme.primary}></span>
							<span class="thinking-dot" style:background-color={colorScheme.primary}></span>
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}

	<!-- BOTTOM DOCKED CHAT BAR (TERTIARY BG, MATCHES FLOATING HEADER) -->
	<div
		class="bottom-chat-bar"
		class:expanded={isOpen}
		style:background-color={colorScheme.tertiary}
		style:color={colorScheme.primary}
	>
		<!-- Left Icon / Indicator -->
		<button
			type="button"
			class="bar-icon-wrap"
			onclick={expandBar}
			aria-label="Focus Stamp assistant input"
			style:color={colorScheme.primary}
		>
			<svg class="chat-speech-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
				<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
			</svg>
		</button>

		<!-- Input field -->
		<input
			type="text"
			class="bar-input"
			bind:this={inputElement}
			bind:value={userInput}
			onfocus={expandBar}
			onkeydown={handleKeydown}
			placeholder={isOpen ? "Type your question about Stamp..." : "Ask Stamp anything..."}
			disabled={isThinking}
			aria-label="Ask Stamp anything"
			style:color="#ffffff"
		/>

		<!-- Send Action or Status -->
		{#if userInput.trim().length > 0}
			<button
				type="button"
				class="bar-send-btn"
				onclick={() => handleSend()}
				disabled={isThinking}
				aria-label="Send query"
				style:background-color={colorScheme.primary}
				style:color={colorScheme.tertiary}
			>
				<svg class="send-arrow-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
					<line x1="22" y1="2" x2="11" y2="13"></line>
					<polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
				</svg>
			</button>
		{:else if isOpen}
			<button
				type="button"
				class="bar-close-btn"
				onclick={collapseBar}
				aria-label="Minimize chat bar"
				style:color={colorScheme.primary}
			>
				✕
			</button>
		{/if}
	</div>
</div>

<style>
	/* BOTTOM CHAT BAR WRAPPER */
	.bottom-chat-wrapper {
		position: fixed;
		bottom: 20px;
		left: 50%;
		transform: translateX(-50%);
		width: calc(100% - 32px);
		max-width: 720px;
		z-index: 9999;
		display: flex;
		flex-direction: column;
		align-items: center;
		font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}

	/* BOTTOM CHAT BAR */
	.bottom-chat-bar {
		width: 320px;
		height: 52px;
		border-radius: 9999px;
		display: flex;
		align-items: center;
		padding: 0.35rem 0.6rem 0.35rem 1rem;
		gap: 0.75rem;
		cursor: text;
		border: none;
		box-shadow: 0 10px 32px rgba(0, 0, 0, 0.32);
		transition:
			width 0.45s cubic-bezier(0.16, 1, 0.3, 1),
			height 0.35s ease,
			background-color 0.45s ease,
			color 0.45s ease;
	}

	.bottom-chat-bar:hover {
		width: 360px;
	}

	.bottom-chat-bar.expanded {
		width: 100%;
		max-width: 720px;
		height: 56px;
	}

	.bar-icon-wrap {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		background: transparent;
		border: none;
		cursor: pointer;
		padding: 0;
		flex-shrink: 0;
	}

	.chat-speech-svg {
		width: 22px;
		height: 22px;
	}

	.bar-input {
		flex: 1;
		background: transparent;
		border: none;
		outline: none;
		font-family: inherit;
		font-size: 0.95rem;
		font-weight: 700;
		min-width: 0;
	}

	.bar-input::placeholder {
		color: rgba(255, 255, 255, 0.6);
		font-weight: 600;
	}

	.bar-send-btn {
		width: 38px;
		height: 38px;
		border-radius: 50%;
		border: none;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		flex-shrink: 0;
		transition: transform 0.15s ease;
	}

	.bar-send-btn:hover {
		transform: scale(1.08);
	}

	.send-arrow-svg {
		width: 17px;
		height: 17px;
		transform: translate(-1px, 1px);
	}

	.bar-close-btn {
		background: transparent;
		border: none;
		font-size: 1.1rem;
		cursor: pointer;
		padding: 0.4rem;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		opacity: 0.75;
		transition: opacity 0.15s ease;
	}

	.bar-close-btn:hover {
		opacity: 1;
	}

	/* RESPONSES FLYOUT ABOVE THE BAR */
	.responses-flyout {
		width: 100%;
		max-height: 480px;
		border-radius: 24px;
		margin-bottom: 12px;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		box-shadow: 0 16px 48px rgba(0, 0, 0, 0.42);
		animation: flyoutSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1);
		transition: background-color 0.45s ease;
	}

	@keyframes flyoutSlideUp {
		from {
			opacity: 0;
			transform: translateY(20px) scale(0.97);
		}
		to {
			opacity: 1;
			transform: translateY(0) scale(1);
		}
	}

	.flyout-header {
		padding: 1rem 1.4rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
		border-bottom: 1px solid rgba(255, 255, 255, 0.08);
		flex-shrink: 0;
	}

	.flyout-title-wrap {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.bot-badge-small {
		width: 28px;
		height: 28px;
		border-radius: 50%;
		font-weight: 900;
		font-size: 0.85rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.flyout-title {
		display: flex;
		align-items: baseline;
		gap: 0.6rem;
		font-size: 0.95rem;
	}

	.online-pill {
		font-size: 0.72rem;
		font-weight: 700;
		display: inline-flex;
		align-items: center;
		gap: 4px;
		opacity: 0.85;
	}

	.online-dot {
		width: 6px;
		height: 6px;
		border-radius: 50%;
	}

	.close-flyout-btn {
		background: transparent;
		border: none;
		font-size: 1.15rem;
		cursor: pointer;
		padding: 0.2rem 0.5rem;
		opacity: 0.75;
		transition: opacity 0.15s;
	}

	.close-flyout-btn:hover {
		opacity: 1;
	}

	.flyout-chips {
		display: flex;
		gap: 6px;
		padding: 0.6rem 1.2rem;
		overflow-x: auto;
		white-space: nowrap;
		flex-shrink: 0;
		scrollbar-width: thin;
	}

	.chip-pill {
		padding: 0.35rem 0.8rem;
		border-radius: 9999px;
		font-size: 0.75rem;
		font-weight: 700;
		border: none;
		cursor: pointer;
		flex-shrink: 0;
		transition: transform 0.15s ease, background-color 0.15s ease;
	}

	.chip-pill:hover {
		transform: scale(1.04);
		background-color: rgba(255, 255, 255, 0.16) !important;
	}

	.flyout-messages {
		flex: 1;
		padding: 1.2rem 1.4rem;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 0.9rem;
		max-height: 340px;
	}

	.msg-row {
		display: flex;
		gap: 0.6rem;
		align-items: flex-start;
	}

	.msg-row.user {
		justify-content: flex-end;
	}

	.bot-icon {
		width: 26px;
		height: 26px;
		border-radius: 50%;
		font-weight: 900;
		font-size: 0.75rem;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		margin-top: 2px;
	}

	.msg-bubble {
		max-width: 82%;
		padding: 0.75rem 1rem;
		border-radius: 16px;
		font-size: 0.9rem;
		line-height: 1.5;
		word-break: break-word;
	}

	.msg-bubble.user {
		border-bottom-right-radius: 4px;
		font-weight: 700;
	}

	.msg-bubble.bot {
		border-bottom-left-radius: 4px;
	}

	.msg-text.prose :global(p) {
		margin: 0 0 0.4rem 0;
	}

	.msg-text.prose :global(p:last-child) {
		margin-bottom: 0;
	}

	.msg-text.prose :global(ul),
	.msg-text.prose :global(ol) {
		margin: 0.3rem 0 0.4rem 1.1rem;
		padding: 0;
	}

	.msg-text.prose :global(li) {
		margin-bottom: 0.2rem;
	}

	.msg-text.prose :global(strong) {
		font-weight: 900;
		color: inherit;
	}

	.msg-time {
		display: flex;
		justify-content: flex-end;
		margin-top: 4px;
		font-size: 0.68rem;
		font-weight: 700;
		opacity: 0.8;
	}

	.msg-bubble.thinking {
		display: flex;
		gap: 5px;
		padding: 0.85rem 1.1rem;
	}

	.thinking-dot {
		width: 6px;
		height: 6px;
		border-radius: 50%;
		animation: pulseDot 1s infinite alternate;
	}

	.thinking-dot:nth-child(2) {
		animation-delay: 0.2s;
	}
	.thinking-dot:nth-child(3) {
		animation-delay: 0.4s;
	}

	@keyframes pulseDot {
		from {
			opacity: 0.3;
			transform: scale(0.8);
		}
		to {
			opacity: 1;
			transform: scale(1.1);
		}
	}

	@media (max-width: 640px) {
		.bottom-chat-wrapper {
			bottom: 12px;
			width: calc(100% - 20px);
		}
		.bottom-chat-bar {
			width: 270px;
		}
		.responses-flyout {
			max-height: 400px;
		}
	}
</style>
