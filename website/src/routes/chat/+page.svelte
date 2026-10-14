<script lang="ts">
	import { onMount } from 'svelte';
	import { matchQuestion, type BotResponse } from '../../lib/knowledge';

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

	let userInput = $state('');
	let isThinking = $state(false);
	let chatStatus: ChatStatus = $state({
		checked: false,
		openrouterConfigured: false,
		model: 'openai/gpt-4o-mini'
	});

	let messages: Message[] = $state([
		{
			id: 1,
			sender: 'bot',
			text: "Kia ora! I am Stamp's customer support assistant. Ask me anything about our peel-and-press toast spreads, launch flavours, allergens, pricing ($5.00 NZD / sheet), or how to apply Stamp.",
			topicTitle: 'Support Guide',
			source: 'fallback_deterministic',
			timestamp: 'Just now'
		}
	]);

	const quickQuestions = [
		'What is a Stamp?',
		'How do I use it?',
		'What flavours are there?',
		'Does the Peanut stamp contain nuts?',
		'Is it gluten-free?',
		'How much is a sheet?',
		'Where can I buy it?',
		'My sheet arrived crushed.',
		'Will this help my stomach?',
		'How does it compare with a jar of peanut butter?'
	];

	function getTimeString() {
		const now = new Date();
		return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	}

	onMount(async () => {
		try {
			const res = await fetch('/api/chat');
			if (res.ok) {
				const data = await res.json();
				chatStatus = {
					checked: true,
					openrouterConfigured: !!data.openrouterConfigured,
					model: data.model || 'openai/gpt-4o-mini'
				};
			} else {
				chatStatus.checked = true;
			}
		} catch {
			chatStatus.checked = true;
		}
	});

	async function handleSend(textToSend?: string) {
		const query = (textToSend || userInput).trim();
		if (!query || isThinking) return;

		// Add user message
		const userMsg: Message = {
			id: Date.now(),
			sender: 'user',
			text: query,
			timestamp: getTimeString()
		};
		messages.push(userMsg);
		userInput = '';
		isThinking = true;

		// Build history payload for contextual follow-up
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
				const botMsg: Message = {
					id: Date.now() + 1,
					sender: 'bot',
					text: data.answer,
					topicTitle: data.topicTitle || (data.source === 'openrouter' ? `OpenRouter · ${data.model || 'AI'}` : 'Deterministic Spec'),
					isRefusal: data.isRefusal,
					source: data.source,
					model: data.model,
					timestamp: getTimeString()
				};
				messages.push(botMsg);
			} else {
				// Server error: Clean client-side fallback
				fallbackLocal(query);
			}
		} catch {
			// Network error or offline: Clean client-side fallback
			fallbackLocal(query);
		} finally {
			isThinking = false;
		}
	}

	function fallbackLocal(query: string) {
		const result: BotResponse = matchQuestion(query);
		const botMsg: Message = {
			id: Date.now() + 1,
			sender: 'bot',
			text: result.answer,
			topicTitle: result.topicTitle || 'Local Spec Fallback',
			isRefusal: result.isRefusal,
			source: 'local_client',
			timestamp: getTimeString()
		};
		messages.push(botMsg);
	}

	function handleKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			handleSend();
		}
	}
</script>

<svelte:head>
	<title>Customer Support Chatbot — STAMP</title>
	<meta
		name="description"
		content="Interactive customer support assistant for Stamp toast spreads powered by OpenRouter with deterministic fallback. Instant answers on ingredients, allergens, and pricing."
	/>
</svelte:head>

<div class="chat-page">
	<div class="chat-container">
		<header class="chat-header">
			<div class="header-status">
				<div class="avatar">STAMP</div>
				<div>
					<h1 class="chat-title">Stamp Customer Support</h1>
					<p class="chat-subtitle">
						<span class="status-dot"></span>
						{#if !chatStatus.checked}
							Connecting to support engine...
						{:else if chatStatus.openrouterConfigured}
							Live OpenRouter AI active ({chatStatus.model})
						{:else}
							Deterministic Spec Engine active (OpenRouter fallback)
						{/if}
					</p>
				</div>
			</div>
			<div class="header-badges">
				{#if chatStatus.openrouterConfigured}
					<span class="badge badge-ai">OpenRouter Active</span>
				{:else}
					<span class="badge">Deterministic Engine</span>
				{/if}
				<span class="badge-policy">Regulatory Compliant</span>
			</div>
		</header>

		<!-- Mode indicator banner -->
		<div class="engine-banner {chatStatus.openrouterConfigured ? 'banner-ai' : 'banner-det'}">
			{#if chatStatus.openrouterConfigured}
				<span class="banner-icon">✨</span>
				<span><strong>OpenRouter AI Live:</strong> Connected using <code>{chatStatus.model}</code> with locked Stamp product spec & refusal rules.</span>
			{:else}
				<span class="banner-icon">🛡️</span>
				<span><strong>Spec Engine Running:</strong> Operating on locked deterministic knowledge module. Set <code>OPENROUTER_API_KEY</code> in environment to enable live AI completions.</span>
			{/if}
		</div>

		<!-- Transcript area -->
		<div class="chat-transcript">
			{#each messages as msg (msg.id)}
				<div class="message-row {msg.sender}">
					<div class="message-bubble {msg.isRefusal ? 'refusal' : ''}">
						{#if msg.sender === 'bot' && msg.topicTitle}
							<div class="bubble-tag-row">
								<span class="bubble-tag {msg.isRefusal ? 'tag-refusal' : ''}">
									{msg.topicTitle}
								</span>
								{#if msg.source === 'openrouter'}
									<span class="pill-source pill-ai">OpenRouter AI</span>
								{:else if msg.source === 'fallback_deterministic'}
									<span class="pill-source pill-det">Spec Engine</span>
								{:else if msg.source === 'local_client'}
									<span class="pill-source pill-local">Client Fallback</span>
								{/if}
							</div>
						{/if}
						<div class="bubble-text">{msg.text}</div>
						<div class="bubble-meta">{msg.timestamp}</div>
					</div>
				</div>
			{/each}

			{#if isThinking}
				<div class="message-row bot">
					<div class="message-bubble thinking">
						<span class="dot"></span>
						<span class="dot"></span>
						<span class="dot"></span>
						<span class="thinking-text">Stamp assistant is typing...</span>
					</div>
				</div>
			{/if}
		</div>

		<!-- Quick prompt chips -->
		<div class="quick-prompts-tray">
			<div class="prompts-label">Suggested Test Questions:</div>
			<div class="chips-scroll">
				{#each quickQuestions as q}
					<button type="button" class="chip-btn" onclick={() => handleSend(q)}>
						{q}
					</button>
				{/each}
			</div>
		</div>

		<!-- Input bar -->
		<footer class="chat-input-bar">
			<input
				type="text"
				class="chat-input"
				placeholder="Ask about flavours, ingredients, pricing, or instructions..."
				bind:value={userInput}
				onkeydown={handleKeyDown}
			/>
			<button
				type="button"
				class="send-btn"
				onclick={() => handleSend()}
				disabled={!userInput.trim() || isThinking}
			>
				{isThinking ? 'Sending...' : 'Send'}
			</button>
		</footer>
	</div>

	<div class="spec-sidebar">
		<h2 class="sidebar-title">Chatbot Architecture & Policy</h2>

		<div class="policy-card">
			<h3 class="card-subtitle">Hybrid Architecture</h3>
			<p class="policy-desc">
				Integrated with OpenRouter API (<code>https://openrouter.ai/api/v1/chat/completions</code>) defaulting to <code>openai/gpt-4o-mini</code>. Includes an automatic fallback to our deterministic knowledge engine when <code>OPENROUTER_API_KEY</code> is unset, ensuring zero downtime.
			</p>
		</div>

		<div class="policy-card">
			<h3 class="card-subtitle">Locked System Prompt</h3>
			<p class="policy-desc">
				The model is anchored by the full product specification (<code>brand/product-spec.md</code>): exact 10 g discs, $5.00 shelf price ($6.25/100g), 12-month pantry stability, and exact industrial formulas (e.g. 80% yeast extract + 15.5% barley malt).
			</p>
		</div>

		<div class="policy-card">
			<h3 class="card-subtitle">Strict Regulatory Refusals</h3>
			<p class="policy-desc">
				Under Food Standards Australia New Zealand (FSANZ), therapeutic claims are illegal for food spreads. Queries regarding medical cures, digestive treatments, organic claims, or false gluten-free status are intercepted and firmly refused.
			</p>
		</div>

		<div class="policy-card">
			<h3 class="card-subtitle">Customer Care Procedures</h3>
			<p class="policy-desc">
				Damaged or crushed sheet reports trigger immediate instructions to photo the batch number on the back of the card and email <code>support@stampbreakfast.nz</code> for free replacement or refund.
			</p>
		</div>
	</div>
</div>

<style>
	.chat-page {
		max-width: 1120px;
		margin: 2rem auto;
		padding: 0 1.5rem 3rem;
		display: grid;
		grid-template-columns: 1fr 340px;
		gap: 2rem;
		align-items: start;
	}

	.chat-container {
		background: #ffffff;
		border: 1px solid #e1c7f7;
		border-radius: 14px;
		display: flex;
		flex-direction: column;
		height: 740px;
		box-shadow: 0 8px 30px rgba(59, 7, 100, 0.08);
		overflow: hidden;
	}

	.chat-header {
		background: #3b0764;
		color: #ffffff;
		padding: 1.25rem 1.5rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
		border-bottom: 3px solid #e24bff;
	}

	.header-status {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.avatar {
		width: 44px;
		height: 44px;
		background: #e24bff;
		color: #3b0764;
		font-weight: 800;
		font-size: 0.95rem;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		letter-spacing: -0.02em;
	}

	.chat-title {
		font-size: 1.2rem;
		font-weight: 800;
	}

	.chat-subtitle {
		font-size: 0.8rem;
		opacity: 0.9;
		display: flex;
		align-items: center;
		gap: 0.4rem;
	}

	.status-dot {
		width: 8px;
		height: 8px;
		background: #10b981;
		border-radius: 50%;
		display: inline-block;
	}

	.header-badges {
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
		align-items: flex-end;
	}

	.badge {
		font-size: 0.72rem;
		font-weight: 700;
		background: rgba(226, 75, 255, 0.2);
		border: 1px solid #e24bff;
		color: #fce7fe;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
	}

	.badge-ai {
		background: rgba(16, 185, 129, 0.25);
		border: 1px solid #34d399;
		color: #d1fae5;
	}

	.badge-policy {
		font-size: 0.72rem;
		font-weight: 700;
		background: rgba(16, 185, 129, 0.2);
		border: 1px solid #10b981;
		color: #a7f3d0;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
	}

	.engine-banner {
		padding: 0.55rem 1.25rem;
		font-size: 0.78rem;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		border-bottom: 1px solid #ecd8ff;
	}

	.banner-det {
		background: #faf5ff;
		color: #581c87;
	}

	.banner-ai {
		background: #ecfdf5;
		color: #065f46;
		border-color: #a7f3d0;
	}

	.banner-icon {
		font-size: 0.95rem;
	}

	.engine-banner code {
		font-size: 0.74rem;
		padding: 0.1rem 0.25rem;
		background: rgba(0, 0, 0, 0.06);
		border-radius: 3px;
	}

	.chat-transcript {
		flex: 1;
		overflow-y: auto;
		padding: 1.5rem;
		background: #faf7fd;
		display: flex;
		flex-direction: column;
		gap: 1.25rem;
	}

	.message-row {
		display: flex;
		width: 100%;
	}

	.message-row.user {
		justify-content: flex-end;
	}

	.message-row.bot {
		justify-content: flex-start;
	}

	.message-bubble {
		max-width: 82%;
		padding: 1rem 1.25rem;
		border-radius: 14px;
		position: relative;
		font-size: 0.95rem;
		line-height: 1.5;
	}

	.message-row.user .message-bubble {
		background: #3b0764;
		color: #ffffff;
		border-bottom-right-radius: 2px;
	}

	.message-row.bot .message-bubble {
		background: #ffffff;
		color: #1a1024;
		border: 1px solid #ebd4ff;
		border-bottom-left-radius: 2px;
		box-shadow: 0 2px 8px rgba(59, 7, 100, 0.04);
	}

	.message-bubble.refusal {
		border-left: 4px solid #ef4444;
		background: #fef7f7;
	}

	.bubble-tag-row {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 0.35rem;
	}

	.bubble-tag {
		font-size: 0.74rem;
		font-weight: 800;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		color: #9333ea;
	}

	.tag-refusal {
		color: #dc2626 !important;
	}

	.pill-source {
		font-size: 0.65rem;
		font-weight: 700;
		padding: 0.1rem 0.35rem;
		border-radius: 3px;
		text-transform: uppercase;
	}

	.pill-ai {
		background: #dcfce7;
		color: #166534;
		border: 1px solid #86efac;
	}

	.pill-det {
		background: #f3e8ff;
		color: #6b21a8;
		border: 1px solid #d8b4fe;
	}

	.pill-local {
		background: #fef3c7;
		color: #92400e;
		border: 1px solid #fde68a;
	}

	.bubble-text {
		white-space: pre-line;
	}

	.bubble-meta {
		font-size: 0.72rem;
		opacity: 0.6;
		margin-top: 0.5rem;
		text-align: right;
	}

	.thinking {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.8rem 1.25rem;
	}

	.thinking-text {
		font-size: 0.82rem;
		color: #7c3aed;
		font-style: italic;
	}

	.dot {
		width: 7px;
		height: 7px;
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
		0% {
			opacity: 0.3;
			transform: scale(0.8);
		}
		100% {
			opacity: 1;
			transform: scale(1.1);
		}
	}

	.quick-prompts-tray {
		background: #ffffff;
		border-top: 1px solid #f0deff;
		padding: 0.75rem 1.25rem;
	}

	.prompts-label {
		font-size: 0.75rem;
		font-weight: 800;
		color: #6a4a85;
		margin-bottom: 0.4rem;
		text-transform: uppercase;
		letter-spacing: 0.04em;
	}

	.chips-scroll {
		display: flex;
		gap: 0.5rem;
		overflow-x: auto;
		padding-bottom: 0.25rem;
	}

	.chip-btn {
		white-space: nowrap;
		background: #f4e8ff;
		border: 1px solid #dec2fa;
		color: #3b0764;
		font-size: 0.8rem;
		font-weight: 600;
		padding: 0.4rem 0.8rem;
		border-radius: 999px;
		cursor: pointer;
		transition: all 0.15s ease;
	}

	.chip-btn:hover {
		background: #e24bff;
		color: #ffffff;
		border-color: #e24bff;
	}

	.chat-input-bar {
		background: #ffffff;
		border-top: 1px solid #ebd4ff;
		padding: 1rem 1.25rem;
		display: flex;
		gap: 0.75rem;
	}

	.chat-input {
		flex: 1;
		padding: 0.75rem 1rem;
		border: 1px solid #d4a6f7;
		border-radius: 8px;
		font-size: 0.95rem;
		outline: none;
		font-family: inherit;
	}

	.chat-input:focus {
		border-color: #3b0764;
		box-shadow: 0 0 0 2px rgba(59, 7, 100, 0.1);
	}

	.send-btn {
		background: #3b0764;
		color: #ffffff;
		border: none;
		border-radius: 8px;
		padding: 0 1.5rem;
		font-weight: 700;
		cursor: pointer;
		transition: background 0.15s ease;
	}

	.send-btn:hover:not(:disabled) {
		background: #550a8a;
	}

	.send-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.spec-sidebar {
		background: #ffffff;
		border: 1px solid #ebd4ff;
		border-radius: 12px;
		padding: 1.75rem;
		box-shadow: 0 4px 16px rgba(59, 7, 100, 0.04);
	}

	.sidebar-title {
		font-size: 1.2rem;
		font-weight: 800;
		color: #3b0764;
		margin-bottom: 1.25rem;
		border-bottom: 2px solid #f2e4ff;
		padding-bottom: 0.75rem;
	}

	.policy-card {
		margin-bottom: 1.25rem;
	}

	.card-subtitle {
		font-size: 0.95rem;
		font-weight: 700;
		color: #3b0764;
		margin-bottom: 0.35rem;
	}

	.policy-desc {
		font-size: 0.85rem;
		color: #4a3560;
		line-height: 1.5;
	}

	code {
		background: #f3e8ff;
		padding: 0.1rem 0.3rem;
		border-radius: 3px;
		font-size: 0.8rem;
		color: #3b0764;
	}

	@media (max-width: 900px) {
		.chat-page {
			grid-template-columns: 1fr;
		}
		.chat-container {
			height: 600px;
		}
		.spec-sidebar {
			order: 2;
		}
	}
</style>
