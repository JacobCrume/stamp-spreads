<script lang="ts">
	import { onMount, onDestroy, tick } from 'svelte';

	interface Message {
		id: number;
		sender: 'user' | 'bot';
		text: string;
		topicTitle?: string;
		isRefusal?: boolean;
		source?: 'openrouter' | 'fallback_deterministic' | 'local_client';
		model?: string;
		timestamp: string;
	}

	interface ChatStatus {
		checked: boolean;
		openrouterConfigured: boolean;
		model: string;
	}

	let isOpen = $state(false);
	let userInput = $state('');
	let isThinking = $state(false);
	let chatStatus: ChatStatus = $state({
		checked: false,
		openrouterConfigured: false,
		model: 'nvidia/nemotron-3-ultra-550b-a55b:free'
	});

	let messagesContainer: HTMLDivElement | null = $state(null);
	let inputElement: HTMLInputElement | null = $state(null);

	let messages: Message[] = $state([
		{
			id: 1,
			sender: 'bot',
			text: "Kia ora! I'm Stamp's assistant. Ask me anything about our peel-and-press toast spreads, launch flavours, allergens, pricing ($5.00 NZD), or how to apply Stamp.",
			topicTitle: 'Support Guide',
			source: 'fallback_deterministic',
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
		(async () => {
			try {
				const res = await fetch('/api/chat');
				if (res.ok) {
					const data = await res.json();
					chatStatus = {
						checked: true,
						openrouterConfigured: !!data.openrouterConfigured,
						model: data.model || 'nvidia/nemotron-3-ultra-550b-a55b:free'
					};
				} else {
					chatStatus.checked = true;
				}
			} catch {
				chatStatus.checked = true;
			}
		})();

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
					topicTitle: data.topicTitle,
					isRefusal: !!data.isRefusal,
					source: data.source,
					model: data.model,
					timestamp: getTimeString()
				});
			} else {
				messages.push({
					id: Date.now() + 1,
					sender: 'bot',
					text: "I couldn't reach the server right now. Stamp is a 10 g peel-and-press spread disc for hot toast ($5.00 NZD / sheet). Please try again shortly.",
					topicTitle: 'Connection Error',
					source: 'fallback_deterministic',
					timestamp: getTimeString()
				});
			}
		} catch {
			messages.push({
				id: Date.now() + 1,
				sender: 'bot',
				text: "Network error. Stamp discs are 10 g each, 8 per sheet for $5.00 NZD. Feel free to re-ask your question.",
				topicTitle: 'Network Notice',
				source: 'fallback_deterministic',
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
		<div class="chat-window" role="dialog" aria-label="Stamp Support Chat">
			<div class="chat-header">
				<div class="header-left">
					<div class="avatar">S</div>
					<div>
						<div class="header-title">Stamp Support</div>
						<div class="header-sub">
							{#if chatStatus.openrouterConfigured}
								<span class="status-dot green"></span>
								<span class="model-tag" title="Powered by OpenRouter">{chatStatus.model.split('/').pop()}</span>
							{:else}
								<span class="status-dot purple"></span>
								<span class="model-tag">Spec Knowledge Engine</span>
							{/if}
						</div>
					</div>
				</div>
				<button class="close-btn" onclick={toggleChat} aria-label="Close Chat">
					✕
				</button>
			</div>

			<div class="quick-chips">
				{#each quickQuestions as q}
					<button class="chip" onclick={() => handleSend(q)} disabled={isThinking}>{q}</button>
				{/each}
			</div>

			<div class="chat-messages" bind:this={messagesContainer}>
				{#each messages as msg (msg.id)}
					<div class="msg-row {msg.sender}">
						{#if msg.sender === 'bot'}
							<div class="bot-badge">S</div>
						{/if}
						<div class="msg-bubble {msg.sender} {msg.isRefusal ? 'refusal' : ''}">
							{#if msg.topicTitle}
								<div class="msg-topic {msg.isRefusal ? 'refusal' : ''}">{msg.topicTitle}</div>
							{/if}
							<div class="msg-text">{msg.text}</div>
							<div class="msg-meta">
								<span>{msg.timestamp}</span>
								{#if msg.source === 'openrouter'}
									<span class="source-tag ai">OpenRouter</span>
								{:else if msg.source === 'fallback_deterministic'}
									<span class="source-tag spec">Verified Spec</span>
								{/if}
							</div>
						</div>
					</div>
				{/each}

				{#if isThinking}
					<div class="msg-row bot">
						<div class="bot-badge">S</div>
						<div class="msg-bubble bot thinking">
							<span class="dot"></span>
							<span class="dot"></span>
							<span class="dot"></span>
						</div>
					</div>
				{/if}
			</div>

			<div class="chat-input-area">
				<input
					type="text"
					bind:this={inputElement}
					bind:value={userInput}
					onkeydown={handleKeydown}
					placeholder="Ask about flavours, allergens, price..."
					disabled={isThinking}
					aria-label="Your question"
				/>
				<button
					class="send-btn"
					onclick={() => handleSend()}
					disabled={!userInput.trim() || isThinking}
					aria-label="Send message"
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
		aria-label={isOpen ? 'Close chat' : 'Open customer support chat'}
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
		background: linear-gradient(135deg, #3b0764 0%, #1f0436 100%);
		color: #ffffff;
		border: 1.5px solid #e24bff;
		padding: 12px 20px;
		border-radius: 9999px;
		cursor: pointer;
		box-shadow: 0 8px 24px rgba(59, 7, 100, 0.45);
		transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
		font-weight: 700;
		font-size: 0.95rem;
	}

	.chat-launcher:hover {
		transform: translateY(-2px) scale(1.03);
		box-shadow: 0 12px 32px rgba(226, 75, 255, 0.5);
		background: #4c0d80;
	}

	.chat-launcher.open {
		padding: 12px 16px;
		border-radius: 50%;
		background: #2a0547;
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
		width: 380px;
		max-width: calc(100vw - 32px);
		height: 560px;
		max-height: calc(100vh - 100px);
		background: #ffffff;
		border-radius: 18px;
		box-shadow: 0 16px 48px rgba(26, 16, 36, 0.28);
		border: 1px solid #ebdcfc;
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
		color: #ffffff;
		padding: 14px 16px;
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 2px solid #e24bff;
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
		font-weight: 700;
		font-size: 0.95rem;
		line-height: 1.2;
	}

	.header-sub {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 0.72rem;
		color: #e6dbf4;
	}

	.status-dot {
		width: 7px;
		height: 7px;
		border-radius: 50%;
		display: inline-block;
	}

	.status-dot.green {
		background: #10b981;
		box-shadow: 0 0 6px #10b981;
	}

	.status-dot.purple {
		background: #e24bff;
	}

	.model-tag {
		font-family: monospace;
		font-size: 0.68rem;
		opacity: 0.9;
	}

	.close-btn {
		background: transparent;
		border: none;
		color: #f3e8ff;
		font-size: 1.1rem;
		cursor: pointer;
		padding: 4px 8px;
		border-radius: 6px;
	}

	.close-btn:hover {
		background: rgba(255, 255, 255, 0.15);
	}

	.quick-chips {
		display: flex;
		gap: 6px;
		padding: 8px 12px;
		background: #fbf8fe;
		overflow-x: auto;
		white-space: nowrap;
		border-bottom: 1px solid #ebdcfc;
		scrollbar-width: thin;
	}

	.chip {
		background: #ffffff;
		border: 1px solid #d8b4fe;
		color: #3b0764;
		padding: 4px 10px;
		border-radius: 12px;
		font-size: 0.73rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.15s;
		flex-shrink: 0;
	}

	.chip:hover:not(:disabled) {
		background: #e24bff;
		color: #ffffff;
		border-color: #e24bff;
	}

	.chat-messages {
		flex: 1;
		padding: 12px;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 10px;
		background: #fdfcff;
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
		background: #3b0764;
		color: #e24bff;
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
		font-size: 0.86rem;
		line-height: 1.45;
		word-break: break-word;
	}

	.msg-bubble.user {
		background: #3b0764;
		color: #ffffff;
		border-bottom-right-radius: 2px;
	}

	.msg-bubble.bot {
		background: #f3e8ff;
		color: #1a1024;
		border-bottom-left-radius: 2px;
		border: 1px solid #e9d5ff;
	}

	.msg-bubble.refusal {
		border-left: 3px solid #dc2626;
		background: #fff1f2;
	}

	.msg-topic {
		font-size: 0.68rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.5px;
		color: #7e22ce;
		margin-bottom: 4px;
	}

	.msg-topic.refusal {
		color: #b91c1c;
	}

	.msg-meta {
		display: flex;
		justify-content: flex-end;
		align-items: center;
		gap: 6px;
		margin-top: 4px;
		font-size: 0.65rem;
		opacity: 0.75;
	}

	.source-tag {
		font-size: 0.62rem;
		padding: 1px 5px;
		border-radius: 4px;
		font-weight: 600;
	}

	.source-tag.ai {
		background: #dbeafe;
		color: #1e40af;
	}

	.source-tag.spec {
		background: #dcfce7;
		color: #166534;
	}

	.msg-bubble.thinking {
		display: flex;
		gap: 4px;
		padding: 12px 16px;
	}

	.dot {
		width: 6px;
		height: 6px;
		background: #9333ea;
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
		padding: 10px 12px;
		border-top: 1px solid #ebdcfc;
		background: #ffffff;
		gap: 8px;
	}

	.chat-input-area input {
		flex: 1;
		border: 1px solid #d8b4fe;
		padding: 8px 12px;
		border-radius: 8px;
		font-size: 0.86rem;
		outline: none;
		font-family: inherit;
	}

	.chat-input-area input:focus {
		border-color: #9333ea;
		box-shadow: 0 0 0 2px rgba(147, 51, 234, 0.15);
	}

	.send-btn {
		background: #3b0764;
		color: #ffffff;
		border: none;
		width: 36px;
		height: 36px;
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: background 0.15s;
		font-size: 0.9rem;
	}

	.send-btn:hover:not(:disabled) {
		background: #5b1399;
	}

	.send-btn:disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}
</style>
