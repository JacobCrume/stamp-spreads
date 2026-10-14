<script lang="ts">
	import { onMount, onDestroy, tick } from 'svelte';
	import { marked } from 'marked';
	import { colorScheme } from './theme.svelte';

	// Configure marked for clean, safe GFM formatting
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

	let messages: Message[] = $state([
		{
			id: 1,
			sender: 'bot',
			text: "Kia ora! I'm Stamp's assistant. Ask me anything about our peel-and-press toast spreads, launch flavours, allergens, pricing ($5.00 NZD / sheet), or how to apply Stamp.",
			timestamp: 'Just now'
		}
	]);

	const quickQuestions = [
		'What is a Stamp?',
		'How do I use it?',
		'What flavours are there?',
		'Does Peanut contain nuts?',
		'Is it gluten-free?',
		'How much is a sheet?',
		'Will this help my stomach?'
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

	let handleOpenChat: (() => void) | null = null;

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
		}
	});

	onDestroy(() => {
		if (typeof window !== 'undefined' && handleOpenChat) {
			window.removeEventListener('stamp:open-chat', handleOpenChat);
		}
	});

	function toggleChat() {
		isOpen = !isOpen;
		if (isOpen) {
			scrollToBottom();
			setTimeout(() => inputElement?.focus(), 150);
		}
	}

	export function openChat() {
		isOpen = true;
		scrollToBottom();
		setTimeout(() => inputElement?.focus(), 150);
	}

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
		}
	}
</script>

<div class="chat-widget-root">
	{#if isOpen}
		<div
			class="chat-window"
			role="dialog"
			aria-label="Stamp Customer Support"
			style:background-color={colorScheme.tertiary}
		>
			<div
				class="chat-header"
				style:background-color={colorScheme.tertiary}
				style:color={colorScheme.primary}
			>
				<div class="header-left">
					<div class="avatar" style:background-color={colorScheme.primary} style:color={colorScheme.tertiary}>S</div>
					<div>
						<div class="header-title" style:color={colorScheme.primary}>Stamp Support</div>
						<div class="header-sub">
							<span class="status-dot green"></span>
							<span style:color={colorScheme.primary}>Online · Ready to help</span>
						</div>
					</div>
				</div>
				<button class="close-btn" onclick={toggleChat} aria-label="Close Chat" style:color={colorScheme.primary}>
					✕
				</button>
			</div>

			<div class="quick-chips" style:background-color={colorScheme.tertiary}>
				{#each quickQuestions as q}
					<button
						class="chip"
						onclick={() => handleSend(q)}
						disabled={isThinking}
						style:background-color={colorScheme.secondary}
						style:color={colorScheme.tertiary}
					>
						{q}
					</button>
				{/each}
			</div>

			<div class="chat-messages" bind:this={messagesContainer} style:background-color={colorScheme.tertiary}>
				{#each messages as msg (msg.id)}
					<div class="msg-row {msg.sender}">
						{#if msg.sender === 'bot'}
							<div class="bot-badge" style:background-color={colorScheme.primary} style:color={colorScheme.tertiary}>S</div>
						{/if}
						<div
							class="msg-bubble {msg.sender}"
							style:background-color={msg.sender === 'user' ? colorScheme.primary : 'rgba(255, 255, 255, 0.12)'}
							style:color={msg.sender === 'user' ? colorScheme.tertiary : '#ffffff'}
						>
							<div class="msg-text prose">
								{@html renderMarkdown(msg.text)}
							</div>
							<div class="msg-meta">
								<span style:color={msg.sender === 'user' ? colorScheme.tertiary : colorScheme.primary}>{msg.timestamp}</span>
							</div>
						</div>
					</div>
				{/each}

				{#if isThinking}
					<div class="msg-row bot">
						<div class="bot-badge" style:background-color={colorScheme.primary} style:color={colorScheme.tertiary}>S</div>
						<div class="msg-bubble bot thinking" style:background-color="rgba(255, 255, 255, 0.12)">
							<span class="dot" style:background-color={colorScheme.primary}></span>
							<span class="dot" style:background-color={colorScheme.primary}></span>
							<span class="dot" style:background-color={colorScheme.primary}></span>
						</div>
					</div>
				{/if}
			</div>

			<div class="chat-input-area" style:background-color={colorScheme.tertiary}>
				<input
					type="text"
					bind:this={inputElement}
					bind:value={userInput}
					onkeydown={handleKeydown}
					placeholder="Ask about flavours, allergens, price..."
					disabled={isThinking}
					aria-label="Your question"
					style:background-color="rgba(255, 255, 255, 0.1)"
					style:color="#ffffff"
				/>
				<button
					class="send-btn"
					onclick={() => handleSend()}
					disabled={!userInput.trim() || isThinking}
					aria-label="Send message"
					style:background-color={colorScheme.primary}
					style:color={colorScheme.tertiary}
				>
					➤
				</button>
			</div>
		</div>
	{/if}

	<!-- Launcher Button -->
	<button
		class="chat-launcher {isOpen ? 'open' : ''}"
		onclick={toggleChat}
		aria-label={isOpen ? 'Close support chat' : 'Open customer support chat'}
		style:background-color={isOpen ? colorScheme.tertiary : colorScheme.primary}
		style:color={isOpen ? colorScheme.primary : colorScheme.tertiary}
	>
		{#if isOpen}
			<span class="launcher-icon">✕</span>
		{:else}
			<span class="launcher-icon">💬</span>
			<span class="launcher-text">Ask Stamp</span>
		{/if}
	</button>
</div>

<style>
	.chat-widget-root {
		position: fixed;
		bottom: 24px;
		right: 24px;
		z-index: 9999;
		font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}

	.chat-launcher {
		display: flex;
		align-items: center;
		gap: 8px;
		background: #e24bff;
		color: #240340;
		border: none;
		padding: 12px 20px;
		border-radius: 9999px;
		cursor: pointer;
		transition: all 0.2s ease;
		font-weight: 900;
		font-size: 0.95rem;
		min-height: 48px;
	}

	.chat-launcher:hover {
		transform: scale(1.04);
		background: #f4c7ff;
	}

	.chat-launcher.open {
		padding: 12px 16px;
		border-radius: 50%;
		background: #3b0764;
		color: #e24bff;
		min-width: 48px;
	}

	.launcher-icon {
		font-size: 1.15rem;
		display: inline-flex;
		align-items: center;
		justify-content: center;
	}

	.chat-window {
		position: absolute;
		bottom: 64px;
		right: 0;
		width: 390px;
		max-width: calc(100vw - 32px);
		height: 560px;
		max-height: calc(100vh - 100px);
		background: #240340;
		border-radius: 18px;
		border: none;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		animation: slideUp 0.22s cubic-bezier(0.16, 1, 0.3, 1);
	}

	@keyframes slideUp {
		from {
			opacity: 0;
			transform: translateY(16px) scale(0.96);
		}
		to {
			opacity: 1;
			transform: translateY(0) scale(1);
		}
	}

	.chat-header {
		background: #3b0764;
		color: #f4c7ff;
		padding: 14px 16px;
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: none;
		flex-shrink: 0;
	}

	.header-left {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.avatar {
		width: 32px;
		height: 32px;
		border-radius: 50%;
		background: #e24bff;
		color: #3b0764;
		font-weight: 800;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 0.95rem;
	}

	.header-title {
		font-weight: 800;
		font-size: 0.98rem;
		line-height: 1.2;
		color: #ffffff;
	}

	.header-sub {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 0.74rem;
		color: #e24bff;
		margin-top: 1px;
	}

	.status-dot {
		width: 7px;
		height: 7px;
		border-radius: 50%;
		display: inline-block;
	}

	.status-dot.green {
		background: #00ffaa;
	}

	.close-btn {
		background: transparent;
		border: none;
		color: #e24bff;
		font-size: 1.2rem;
		cursor: pointer;
		padding: 6px 10px;
		border-radius: 8px;
		min-width: 36px;
		min-height: 36px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.close-btn:hover {
		background: rgba(226, 75, 255, 0.2);
	}

	.quick-chips {
		display: flex;
		gap: 6px;
		padding: 8px 12px;
		background: #1e0235;
		overflow-x: auto;
		white-space: nowrap;
		border-bottom: none;
		scrollbar-width: thin;
		flex-shrink: 0;
		-webkit-overflow-scrolling: touch;
	}

	.chip {
		background: #3b0764;
		border: none;
		color: #ffd640;
		padding: 6px 12px;
		border-radius: 9999px;
		font-size: 0.75rem;
		font-weight: 800;
		cursor: pointer;
		transition: all 0.15s;
		flex-shrink: 0;
		min-height: 32px;
		display: inline-flex;
		align-items: center;
	}

	.chip:hover:not(:disabled) {
		background: #e24bff;
		color: #3b0764;
	}

	.chat-messages {
		flex: 1;
		padding: 14px;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 12px;
		background: #240340;
		-webkit-overflow-scrolling: touch;
	}

	.msg-row {
		display: flex;
		gap: 8px;
		max-width: 88%;
	}

	.msg-row.user {
		align-self: flex-end;
		flex-direction: row-reverse;
	}

	.msg-row.bot {
		align-self: flex-start;
	}

	.bot-badge {
		width: 24px;
		height: 24px;
		border-radius: 50%;
		background: #e24bff;
		color: #3b0764;
		font-size: 0.7rem;
		font-weight: 800;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		margin-top: 2px;
	}

	.msg-bubble {
		padding: 10px 14px;
		border-radius: 14px;
		font-size: 0.88rem;
		line-height: 1.5;
		word-break: break-word;
	}

	.msg-bubble.user {
		background: #e24bff;
		color: #240340;
		border-bottom-right-radius: 2px;
		font-weight: 600;
	}

	.msg-bubble.bot {
		background: #3b0764;
		color: #f4c7ff;
		border-bottom-left-radius: 2px;
		border: none;
	}

	/* Markdown prose styling */
	.msg-text.prose :global(p) {
		margin: 0 0 0.5rem 0;
	}

	.msg-text.prose :global(p:last-child) {
		margin-bottom: 0;
	}

	.msg-text.prose :global(ul),
	.msg-text.prose :global(ol) {
		margin: 0.35rem 0 0.5rem 1.25rem;
		padding: 0;
	}

	.msg-text.prose :global(li) {
		margin-bottom: 0.3rem;
	}

	.msg-text.prose :global(strong) {
		font-weight: 800;
		color: inherit;
	}

	.msg-text.prose :global(code) {
		background: rgba(226, 75, 255, 0.2);
		padding: 1px 4px;
		border-radius: 4px;
		font-size: 0.88em;
		font-family: monospace;
		color: #ffbbfd;
	}

	.msg-meta {
		display: flex;
		justify-content: flex-end;
		align-items: center;
		margin-top: 4px;
		font-size: 0.68rem;
		opacity: 0.75;
	}

	.msg-bubble.thinking {
		display: flex;
		gap: 4px;
		padding: 12px 16px;
	}

	.dot {
		width: 6px;
		height: 6px;
		background: #e24bff;
		border-radius: 50%;
		animation: pulse 1s infinite alternate;
	}

	.dot:nth-child(2) {
		animation-delay: 0.2s;
	}
	.dot:nth-child(3) {
		animation-delay: 0.4s;
	}

	@keyframes pulse {
		from {
			opacity: 0.3;
			transform: scale(0.8);
		}
		to {
			opacity: 1;
			transform: scale(1.1);
		}
	}

	.chat-input-area {
		display: flex;
		padding: 12px 14px;
		border-top: none;
		background: #1a0230;
		gap: 8px;
		flex-shrink: 0;
	}

	.chat-input-area input {
		flex: 1;
		background: #2e054f;
		border: none;
		color: #f4c7ff;
		padding: 10px 14px;
		border-radius: 10px;
		font-size: 0.9rem;
		outline: none;
		font-family: inherit;
		min-height: 44px;
	}

	.chat-input-area input::placeholder {
		color: #be7de0;
	}

	.chat-input-area input:focus {
		background: #3b0764;
	}

	.send-btn {
		background: #e24bff;
		color: #240340;
		border: none;
		width: 44px;
		height: 44px;
		border-radius: 10px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.15s;
		font-size: 1.1rem;
		font-weight: 800;
		flex-shrink: 0;
	}

	.send-btn:hover:not(:disabled) {
		background: #ff85ff;
		transform: scale(1.04);
	}

	.send-btn:disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}

	/* Mobile full-screen / bottom-sheet responsiveness */
	@media (max-width: 640px) {
		.chat-widget-root {
			bottom: 16px;
			right: 16px;
		}

		.chat-launcher {
			padding: 10px 16px;
			font-size: 0.9rem;
		}

		.chat-window {
			position: fixed;
			top: 0;
			left: 0;
			right: 0;
			bottom: 0;
			width: 100vw;
			max-width: 100vw;
			height: 100dvh;
			max-height: 100dvh;
			border-radius: 0;
			border: none;
			box-shadow: none;
			z-index: 10000;
		}

		.chat-header {
			padding: 16px;
			padding-top: max(16px, env(safe-area-inset-top, 16px));
		}

		.chat-input-area {
			padding: 10px 12px;
			padding-bottom: max(12px, env(safe-area-inset-bottom, 12px));
		}

		.msg-row {
			max-width: 92%;
		}
	}
</style>
