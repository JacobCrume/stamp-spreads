<script lang="ts">
	import { onMount } from 'svelte';
	import { marked } from 'marked';
	import Wordmark from '../../lib/Wordmark.svelte';
	import { setSectionTheme } from '../../lib/theme.svelte';

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

	function countLines(str: string): number {
		if (!str) return 0;
		let count = 1;
		for (let i = 0; i < str.length; i++) {
			if (str.charCodeAt(i) === 10) count++;
		}
		return count;
	}

	interface ChatSummary {
		id: string;
		title: string;
		date: string;
		turnsCount: number;
		totalSteps: number;
		toolCallsCount: number;
		subagentsCount: number;
		file: string;
	}

	interface ToolCallItem {
		kind: 'tool';
		name: string;
		summary: string;
		args: Record<string, any>;
		stepIndex: number;
		output: string;
	}

	interface ResponseItem {
		kind: 'response';
		content: string;
	}

	interface ThinkingItem {
		kind: 'thinking';
		content: string;
	}

	interface SystemItem {
		kind: 'system';
		sender?: string | null;
		content: string;
	}

	type TurnItem = ToolCallItem | ResponseItem | ThinkingItem | SystemItem;

	interface Turn {
		turnNum: number;
		createdAt: string;
		timeStr: string;
		userPrompt: string;
		userMeta: string;
		items: TurnItem[];
	}

	interface SubagentWorker {
		id: string;
		name: string;
		role: string;
		title: string;
		parent: string;
		stepsCount: number;
		timeline: string;
		items: TurnItem[];
	}

	interface ChatDetail {
		id: string;
		title: string;
		startTime: string;
		endTime: string;
		turnsCount: number;
		totalSteps: number;
		totalToolCalls: number;
		turns: Turn[];
		subagents: SubagentWorker[];
	}

	let chats = $state<ChatSummary[]>([]);
	let selectedChatId = $state<string>('');
	let activeChat = $state<ChatDetail | null>(null);
	let isLoading = $state(true);
	let errorMsg = $state('');

	let searchQuery = $state('');
	let showSubagents = $state(false);
	// Tool calls hidden by default
	let hideToolCalls = $state(true);

	// Toggling tool calls is purely a CSS class toggle for instant performance
	function toggleToolCalls() {
		hideToolCalls = !hideToolCalls;
	}

	let filteredTurns = $derived.by(() => {
		if (!activeChat) return [];
		return activeChat.turns.filter((turn) => {
			if (searchQuery.trim()) {
				const q = searchQuery.toLowerCase();
				const inPrompt = turn.userPrompt.toLowerCase().includes(q);
				const inItems = turn.items.some((it) => {
					if (it.kind === 'response') return it.content.toLowerCase().includes(q);
					if (it.kind === 'thinking' || it.kind === 'system') return it.content.toLowerCase().includes(q);
					if (it.kind === 'tool') {
						return (
							it.name.toLowerCase().includes(q) ||
							it.summary.toLowerCase().includes(q) ||
							(it.output && it.output.toLowerCase().includes(q))
						);
					}
					return false;
				});
				if (!inPrompt && !inItems) return false;
			}
			return true;
		});
	});

	async function loadManifest() {
		try {
			isLoading = true;
			const res = await fetch('/data/transcripts/manifest.json');
			if (!res.ok) throw new Error('Could not load chats manifest');
			chats = await res.json();
			if (chats.length > 0) {
				const url = new URL(window.location.href);
				const paramId = url.searchParams.get('chat');
				const targetId = (paramId && chats.some((c) => c.id === paramId)) ? paramId : chats[0].id;
				await selectChat(targetId);
			}
		} catch (err: any) {
			errorMsg = err.message || 'Error loading chats';
		} finally {
			isLoading = false;
		}
	}

	async function selectChat(id: string) {
		selectedChatId = id;
		showSubagents = false;
		if (typeof window !== 'undefined') {
			const url = new URL(window.location.href);
			url.searchParams.set('chat', id);
			window.history.replaceState(null, '', url.toString());
		}
		try {
			isLoading = true;
			const res = await fetch(`/data/transcripts/${id}.json`);
			if (!res.ok) throw new Error(`Could not load chat data for ${id}`);
			activeChat = await res.json();
		} catch (err: any) {
			errorMsg = err.message || 'Error loading chat';
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		setSectionTheme('yeast');
		loadManifest();
	});
</script>

<svelte:head>
	<title>STAMP Transcripts</title>
</svelte:head>

<div class="stamp-transcript-app">
	<!-- SIDEBAR: LIST OF CHATS (TERTIARY BG #3b0764, ROUNDED RIGHT CORNERS) -->
	<aside class="sidebar">
		<div class="sidebar-header">
			<a href="/" class="wordmark-link" aria-label="Back to main page">
				<Wordmark color="#e24bff" />
			</a>
			<span class="header-badge">Transcripts</span>
		</div>

		<!-- CHATS LIST -->
		<div class="chats-section">
			<div class="section-heading">CHATS</div>
			<div class="chats-list">
				{#each chats as chat (chat.id)}
					<button
						type="button"
						class="chat-card"
						class:active={selectedChatId === chat.id}
						onclick={() => selectChat(chat.id)}
					>
						<div class="chat-title">{chat.title}</div>
						<div class="chat-id">{chat.id.slice(0, 16)}...</div>
						<div class="chat-meta">
							<span>{chat.turnsCount} turns</span>
							<span>{chat.toolCallsCount} tools</span>
						</div>
					</button>
				{/each}
			</div>
		</div>

		<!-- SUBAGENTS SHORTCUT -->
		{#if activeChat && activeChat.subagents && activeChat.subagents.length > 0}
			<div class="sidebar-subagents">
				<button
					type="button"
					class="toggle-btn"
					class:active={showSubagents}
					onclick={() => (showSubagents = !showSubagents)}
				>
					{showSubagents ? 'View Main Chat' : `View Subagents (${activeChat.subagents.length})`}
				</button>
			</div>
		{/if}
	</aside>

	<!-- MAIN CONTENT AREA -->
	<main class="main-content">
		{#if isLoading}
			<div class="status-msg">
				<p>Loading...</p>
			</div>
		{:else if errorMsg}
			<div class="status-msg">
				<p>{errorMsg}</p>
				<button type="button" class="btn-primary" onclick={loadManifest}>Retry</button>
			</div>
		{:else if activeChat}
			<!-- FLOATING ROUNDED TOP BAR (STAMP FLOATING HEADER STYLE) -->
			<header class="top-nav-bar">
				<div class="nav-left">
					<span class="active-chat-pill">{activeChat.title}</span>
				</div>

				<div class="nav-center">
					<input
						type="text"
						placeholder="Search messages..."
						bind:value={searchQuery}
						class="search-input-pill"
					/>
				</div>

				<div class="nav-right">
					<button
						type="button"
						class="tool-toggle-pill"
						class:active={!hideToolCalls}
						onclick={toggleToolCalls}
					>
						{hideToolCalls ? 'Show Tool Calls' : 'Hide Tool Calls'}
					</button>
				</div>
			</header>

			<!-- STREAM CONTENT -->
			<div class="stream-container">
				{#if showSubagents}
					<!-- SUBAGENTS VIEW -->
					<div class="subagents-list" class:hide-tools={hideToolCalls}>
						<h2 class="stream-section-title">Subagent Execution Traces</h2>

						{#each activeChat.subagents as subagent (subagent.id)}
							<div class="subagent-block">
								<div class="subagent-block-header">
									<div class="subagent-badge">{subagent.name}</div>
									<div class="subagent-title">{subagent.title}</div>
									<div class="subagent-id">{subagent.id}</div>
								</div>

								<div class="subagent-body">
									{#each subagent.items as item}
										{#if item.kind === 'thinking'}
											<div class="thinking-box">
												<details class="tool-details">
													<summary class="details-summary-pill thinking-summary">
														<svg class="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
															<polyline points="9 18 15 12 9 6"></polyline>
														</svg>
														<span>Thinking ({countLines(item.content)} lines)</span>
													</summary>
													<pre class="code-box">{item.content}</pre>
												</details>
											</div>
										{:else if item.kind === 'tool'}
											<div class="tool-box">
												<div class="tool-box-header">
													<div class="tool-header-left">
														<span class="tool-badge">{item.name.replace(/_/g, ' ')}</span>
														<span class="tool-summary">{item.summary}</span>
													</div>
													{#if item.stepIndex}
														<span class="step-badge">Step {item.stepIndex}</span>
													{/if}
												</div>
												<div class="tool-box-body">
													<pre class="code-box">{JSON.stringify(item.args, null, 2)}</pre>
													{#if item.output}
														<details class="tool-details">
															<summary class="details-summary-pill">
																<svg class="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
																	<polyline points="9 18 15 12 9 6"></polyline>
																</svg>
																<span>Output ({countLines(item.output)} lines)</span>
															</summary>
															<pre class="code-box output-box">{item.output}</pre>
														</details>
													{/if}
												</div>
											</div>
										{:else if item.kind === 'response'}
											<div class="subagent-msg">
												<div class="subagent-msg-tag">REPORT</div>
												<div class="prose">{@html renderMarkdown(item.content)}</div>
											</div>
										{/if}
									{/each}
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<!-- TURNS STREAM (Toggled with pure CSS class for 0ms lag) -->
					<div class="turns-stream" class:hide-tools={hideToolCalls}>
						{#each filteredTurns as turn (turn.turnNum)}
							<div class="turn-group" id="turn-{turn.turnNum}">
								<div class="turn-index-label">TURN {turn.turnNum} • {turn.timeStr}</div>

								<!-- USER MESSAGE (PRIMARY BG #e24bff, SECONDARY TEXT #240340) -->
								<div class="msg-row user-row">
									<div class="msg-bubble user-bubble">
										<div class="prose user-prose">
											{@html renderMarkdown(turn.userPrompt)}
										</div>
									</div>
								</div>

								<!-- ASSISTANT & TOOLS -->
								<div class="responses-flow">
									{#each turn.items as item}
										{#if item.kind === 'thinking'}
											<div class="thinking-box">
												<details class="tool-details">
													<summary class="details-summary-pill thinking-summary">
														<svg class="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
															<polyline points="9 18 15 12 9 6"></polyline>
														</svg>
														<span>Reasoning ({countLines(item.content)} lines)</span>
													</summary>
													<pre class="code-box">{item.content}</pre>
												</details>
											</div>
										{:else if item.kind === 'system'}
											<div class="system-box">
												<div class="tool-box-header">
													<div class="tool-header-left">
														<span class="tool-badge">{item.sender || 'System'}</span>
														<span class="tool-summary">System Notification</span>
													</div>
												</div>
												<div class="tool-box-body">
													<pre class="code-box">{item.content}</pre>
												</div>
											</div>
										{:else if item.kind === 'tool'}
											<!-- SLEEK INTEGRATED STAMP TOOL CARD -->
											<div class="tool-box">
												<div class="tool-box-header">
													<div class="tool-header-left">
														<span class="tool-badge">{item.name.replace(/_/g, ' ')}</span>
														<span class="tool-summary">{item.summary}</span>
													</div>
													{#if item.stepIndex}
														<span class="step-badge">Step {item.stepIndex}</span>
													{/if}
												</div>

												<div class="tool-box-body">
													{#if item.name === 'run_command'}
														{#if item.args.Cwd && item.args.Cwd !== '/'}
															<div class="tool-meta-row">
																<span class="meta-label">dir</span>
																<span class="meta-value">{item.args.Cwd}</span>
															</div>
														{/if}
														<div class="command-block">
															<span class="prompt-sym">$</span>
															<span class="cmd-text">{item.args.CommandLine}</span>
														</div>
													{:else if item.name === 'view_file'}
														<div class="tool-meta-row">
															<span class="meta-label">file</span>
															<span class="meta-value">{item.args.AbsolutePath}</span>
															{#if item.args.StartLine}
																<span class="meta-range">L{item.args.StartLine}–L{item.args.EndLine}</span>
															{/if}
														</div>
													{:else if item.name === 'write_to_file'}
														<div class="tool-meta-row">
															<span class="meta-label">target</span>
															<span class="meta-value">{item.args.TargetFile}</span>
														</div>
														{#if item.args.Description}
															<div class="tool-desc-line">{item.args.Description}</div>
														{/if}
														{#if item.args.CodeContent}
															<details class="tool-details">
																<summary class="details-summary-pill">
																	<svg class="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
																		<polyline points="9 18 15 12 9 6"></polyline>
																	</svg>
																	<span>Code Content ({countLines(item.args.CodeContent)} lines)</span>
																</summary>
																<pre class="code-box">{item.args.CodeContent}</pre>
															</details>
														{/if}
													{:else if item.name === 'replace_file_content'}
														<div class="tool-meta-row">
															<span class="meta-label">edit</span>
															<span class="meta-value">{item.args.TargetFile}</span>
														</div>
														{#if item.args.Instruction}
															<div class="tool-desc-line">{item.args.Instruction}</div>
														{/if}
														{#if item.args.ReplacementContent}
															<details class="tool-details">
																<summary class="details-summary-pill">
																	<svg class="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
																		<polyline points="9 18 15 12 9 6"></polyline>
																	</svg>
																	<span>Diff Content</span>
																</summary>
																<pre class="code-box">{item.args.ReplacementContent}</pre>
															</details>
														{/if}
													{:else}
														<pre class="code-box">{JSON.stringify(item.args, null, 2)}</pre>
													{/if}

													{#if item.output}
														<details class="tool-details">
															<summary class="details-summary-pill">
																<svg class="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
																	<polyline points="9 18 15 12 9 6"></polyline>
																</svg>
																<span>Tool Output ({countLines(item.output)} lines)</span>
															</summary>
															<pre class="code-box output-box">{item.output}</pre>
														</details>
													{/if}
												</div>
											</div>
										{:else if item.kind === 'response'}
											<!-- ASSISTANT MESSAGE (TERTIARY BG #3b0764, WHITE TEXT #ffffff) -->
											<div class="msg-row bot-row">
												<div class="bot-avatar">S</div>
												<div class="msg-bubble bot-bubble">
													<div class="prose bot-prose">
														{@html renderMarkdown(item.content)}
													</div>
												</div>
											</div>
										{/if}
									{/each}
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		{/if}
	</main>
</div>

<style>
	/* STRICT 3-COLOR SYSTEM + BLACK/WHITE (ZERO OUTLINES) */
	/* 1. Primary:   #e24bff (Electric Violet) */
	/* 2. Secondary: #240340 (Deep Night Ink) */
	/* 3. Tertiary:  #3b0764 (Deep Purple) */
	/* 4. White:     #ffffff */
	/* 5. Black:     #000000 */

	*, *::before, *::after {
		box-sizing: border-box;
		border: none;
		outline: none;
		margin: 0;
		padding: 0;
	}

	.stamp-transcript-app {
		display: flex;
		height: 100vh;
		width: 100vw;
		background: #240340;
		color: #ffffff;
		font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		overflow: hidden;
	}

	/* SIDEBAR (TERTIARY #3b0764, ROUNDED RIGHT EDGES) */
	.sidebar {
		width: 290px;
		min-width: 290px;
		background: #3b0764;
		height: 100vh;
		display: flex;
		flex-direction: column;
		padding: 24px 18px;
		gap: 20px;
		border-top-right-radius: 24px;
		border-bottom-right-radius: 24px;
		z-index: 20;
	}

	.sidebar-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	/* CLICKABLE WORDMARK BACK TO HOME WITH SPRING ANIMATION */
	.wordmark-link {
		display: inline-flex;
		align-items: center;
		width: 110px;
		height: 28px;
		color: #e24bff;
		text-decoration: none;
		cursor: pointer;
		user-select: none;
		transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	.wordmark-link:hover {
		transform: scale(1.08);
	}

	.wordmark-link:active {
		transform: scale(0.92);
	}

	.header-badge {
		background: #240340;
		color: #e24bff;
		font-size: 0.7rem;
		font-weight: 900;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		padding: 4px 10px;
		border-radius: 9999px;
	}

	/* CHATS LIST */
	.chats-section {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow-y: auto;
		gap: 10px;
	}

	.section-heading {
		font-size: 0.72rem;
		font-weight: 900;
		letter-spacing: 0.1em;
		color: #e24bff;
		padding-left: 4px;
	}

	.chats-list {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.chat-card {
		background: #240340;
		color: #ffffff;
		border-radius: 14px;
		padding: 12px 14px;
		text-align: left;
		cursor: pointer;
		display: flex;
		flex-direction: column;
		gap: 4px;
		user-select: none;
		transition:
			transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1),
			background-color 0.2s ease,
			color 0.2s ease;
	}

	.chat-card:hover {
		transform: translateX(4px) scale(1.02);
	}

	.chat-card:active {
		transform: scale(0.95);
	}

	.chat-card.active {
		background: #e24bff;
		color: #240340;
	}

	.chat-title {
		font-size: 0.88rem;
		font-weight: 800;
		line-height: 1.25;
	}

	.chat-id {
		font-family: monospace;
		font-size: 0.72rem;
		opacity: 0.8;
	}

	.chat-meta {
		display: flex;
		justify-content: space-between;
		font-size: 0.72rem;
		font-weight: 700;
		margin-top: 4px;
		opacity: 0.85;
	}

	.sidebar-subagents {
		display: flex;
		flex-direction: column;
	}

	.toggle-btn {
		width: 100%;
		background: #240340;
		color: #ffffff;
		font-weight: 800;
		font-size: 0.8rem;
		padding: 10px 14px;
		border-radius: 9999px;
		cursor: pointer;
		text-align: center;
		user-select: none;
		transition:
			transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1),
			background-color 0.2s ease,
			color 0.2s ease;
	}

	.toggle-btn:hover {
		transform: translateY(-2px) scale(1.03);
	}

	.toggle-btn:active {
		transform: scale(0.93);
	}

	.toggle-btn.active {
		background: #e24bff;
		color: #240340;
	}

	/* MAIN AREA */
	.main-content {
		flex: 1;
		height: 100vh;
		display: flex;
		flex-direction: column;
		background: #240340;
		overflow-y: auto;
		position: relative;
	}

	/* FLOATING TOP NAV BAR */
	.top-nav-bar {
		margin: 16px 28px;
		padding: 8px 16px;
		background: #3b0764;
		border-radius: 9999px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
		position: sticky;
		top: 16px;
		z-index: 30;
	}

	.nav-left {
		display: flex;
		align-items: center;
		flex: 1;
	}

	.active-chat-pill {
		font-size: 0.85rem;
		font-weight: 800;
		color: #ffffff;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		padding-left: 8px;
	}

	.nav-center {
		display: flex;
		justify-content: center;
		flex: 1.5;
	}

	.search-input-pill {
		background: #240340;
		color: #ffffff;
		padding: 9px 20px;
		border-radius: 9999px;
		font-size: 0.82rem;
		font-family: inherit;
		width: 100%;
		max-width: 380px;
		text-align: center;
		transition: max-width 0.2s, text-align 0.2s;
	}

	.search-input-pill:focus {
		max-width: 440px;
		text-align: left;
	}

	.search-input-pill::placeholder {
		color: rgba(255, 255, 255, 0.5);
	}

	.nav-right {
		display: flex;
		justify-content: flex-end;
		flex: 1;
	}

	/* SHOW/HIDE TOOL CALLS BUTTON WITH TACTILE SPRING ANIMATION */
	.tool-toggle-pill {
		background: #240340;
		color: #ffffff;
		padding: 9px 20px;
		border-radius: 9999px;
		font-size: 0.82rem;
		font-weight: 800;
		cursor: pointer;
		white-space: nowrap;
		user-select: none;
		transition:
			transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1),
			background-color 0.2s ease,
			color 0.2s ease;
	}

	.tool-toggle-pill:hover {
		transform: translateY(-2px) scale(1.04);
	}

	.tool-toggle-pill:active {
		transform: scale(0.92);
	}

	.tool-toggle-pill.active {
		background: #e24bff;
		color: #240340;
	}

	/* STREAM CONTENT */
	.stream-container {
		padding: 24px 36px 64px;
		max-width: 960px;
		width: 100%;
		margin: 0 auto;
	}

	.stream-section-title {
		font-size: 1.4rem;
		font-weight: 900;
		color: #e24bff;
		margin-bottom: 24px;
	}

	.turns-stream {
		display: flex;
		flex-direction: column;
		gap: 36px;
	}

	/* INSTANT CSS HIDING FOR MAXIMUM PERFORMANCE */
	.turns-stream.hide-tools .tool-box,
	.turns-stream.hide-tools .thinking-box,
	.turns-stream.hide-tools .system-box,
	.subagents-list.hide-tools .tool-box,
	.subagents-list.hide-tools .thinking-box {
		display: none !important;
	}

	.turn-group {
		display: flex;
		flex-direction: column;
		gap: 16px;
		content-visibility: auto;
		contain-intrinsic-size: 0 100px;
	}

	.turn-index-label {
		font-size: 0.72rem;
		font-weight: 900;
		letter-spacing: 0.1em;
		color: #e24bff;
		opacity: 0.9;
	}

	/* MESSAGES */
	.msg-row {
		display: flex;
		gap: 14px;
		margin: 4px 0;
	}

	.user-row {
		justify-content: flex-end;
	}

	.bot-row {
		justify-content: flex-start;
		align-items: flex-start;
	}

	.bot-avatar {
		width: 34px;
		height: 34px;
		border-radius: 50%;
		background: #e24bff;
		color: #240340;
		font-weight: 900;
		font-size: 0.95rem;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		margin-top: 4px;
	}

	.msg-bubble {
		max-width: 86%;
		padding: 1.15rem 1.45rem;
		border-radius: 18px;
		font-size: 0.95rem;
		line-height: 1.6;
	}

	.user-bubble {
		background: #e24bff;
		color: #240340;
		font-weight: 700;
		border-bottom-right-radius: 4px;
	}

	.bot-bubble {
		background: #3b0764;
		color: #ffffff;
		border-bottom-left-radius: 4px;
	}

	/* RESPONSES FLOW (DISTINCT SPACING BETWEEN ASSISTANT MESSAGES & CARDS) */
	.responses-flow {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	/* SLEEK STAMP TOOL SPEC CARD */
	.tool-box,
	.system-box {
		background: #3b0764;
		border-radius: 14px;
		padding: 14px 16px;
		display: flex;
		flex-direction: column;
		gap: 10px;
		content-visibility: auto;
		contain-intrinsic-size: 0 70px;
	}

	.tool-box-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
	}

	.tool-header-left {
		display: flex;
		align-items: center;
		gap: 10px;
		min-width: 0;
	}

	.tool-badge {
		background: #240340;
		color: #e24bff;
		font-size: 0.68rem;
		font-weight: 900;
		padding: 3px 10px;
		border-radius: 9999px;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		white-space: nowrap;
	}

	.tool-summary {
		font-size: 0.88rem;
		font-weight: 700;
		color: #ffffff;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.step-badge {
		font-size: 0.72rem;
		font-weight: 800;
		color: #e24bff;
		white-space: nowrap;
	}

	.tool-box-body {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.tool-meta-row {
		display: flex;
		align-items: center;
		gap: 8px;
		background: #240340;
		padding: 6px 12px;
		border-radius: 8px;
	}

	.meta-label {
		color: #e24bff;
		font-weight: 900;
		text-transform: uppercase;
		font-size: 0.68rem;
		letter-spacing: 0.05em;
	}

	.meta-value {
		color: #ffffff;
		font-family: monospace;
		font-size: 0.8rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.meta-range {
		margin-left: auto;
		color: #e24bff;
		font-size: 0.72rem;
		font-weight: 800;
	}

	.tool-desc-line {
		font-size: 0.82rem;
		font-style: italic;
		opacity: 0.9;
		padding: 2px 4px;
	}

	.command-block {
		background: #000000;
		color: #ffffff;
		padding: 9px 12px;
		border-radius: 8px;
		font-family: monospace;
		font-size: 0.82rem;
		display: flex;
		align-items: center;
		gap: 8px;
		overflow-x: auto;
	}

	.prompt-sym {
		color: #e24bff;
		font-weight: 900;
		user-select: none;
	}

	.cmd-text {
		white-space: pre-wrap;
		word-break: break-all;
	}

	/* CUSTOM ACCORDION / DETAILS TOGGLE */
	details {
		display: flex;
		flex-direction: column;
	}

	details > summary {
		list-style: none;
	}

	details > summary::-webkit-details-marker {
		display: none;
	}

	.details-summary-pill {
		display: inline-flex;
		align-items: center;
		gap: 7px;
		background: #240340;
		color: #e24bff;
		font-size: 0.78rem;
		font-weight: 800;
		padding: 5px 13px;
		border-radius: 9999px;
		cursor: pointer;
		user-select: none;
		align-self: flex-start;
		transition:
			transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1),
			background-color 0.2s ease,
			color 0.2s ease;
	}

	.details-summary-pill:hover {
		transform: scale(1.04);
	}

	.details-summary-pill:active {
		transform: scale(0.94);
	}

	.chevron-icon {
		width: 13px;
		height: 13px;
		transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	details[open] > summary .chevron-icon {
		transform: rotate(90deg);
	}

	.code-box {
		background: #000000;
		color: #ffffff;
		padding: 10px 14px;
		border-radius: 8px;
		font-family: monospace;
		font-size: 0.8rem;
		overflow-x: auto;
		line-height: 1.45;
		max-height: 380px;
		overflow-y: auto;
		margin-top: 8px;
	}

	/* THINKING PILL */
	.thinking-box {
		margin: 2px 0;
	}

	.thinking-summary {
		background: #240340;
		color: #e24bff;
	}

	/* SUBAGENTS */
	.subagents-list {
		display: flex;
		flex-direction: column;
		gap: 28px;
	}

	.subagent-block {
		background: #3b0764;
		border-radius: 18px;
		overflow: hidden;
	}

	.subagent-block-header {
		background: #240340;
		padding: 14px 20px;
		display: flex;
		align-items: center;
		gap: 12px;
	}

	.subagent-badge {
		background: #e24bff;
		color: #240340;
		font-size: 0.72rem;
		font-weight: 900;
		padding: 4px 12px;
		border-radius: 9999px;
		text-transform: uppercase;
		letter-spacing: 0.06em;
	}

	.subagent-title {
		font-size: 1rem;
		font-weight: 800;
		color: #ffffff;
	}

	.subagent-id {
		font-family: monospace;
		font-size: 0.75rem;
		color: #e24bff;
		margin-left: auto;
	}

	.subagent-body {
		padding: 20px;
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.subagent-msg {
		background: #240340;
		padding: 16px;
		border-radius: 14px;
	}

	.subagent-msg-tag {
		font-size: 0.7rem;
		font-weight: 900;
		letter-spacing: 0.08em;
		color: #e24bff;
		margin-bottom: 8px;
	}

	/* PROSE STYLING */
	.prose :global(p) {
		margin: 0 0 0.6rem 0;
	}
	.prose :global(p:last-child) {
		margin-bottom: 0;
	}
	.prose :global(ul), .prose :global(ol) {
		margin: 0.4rem 0 0.6rem 1.3rem;
	}
	.prose :global(li) {
		margin-bottom: 0.25rem;
	}
	.prose :global(strong) {
		font-weight: 900;
		color: inherit;
	}
	.prose :global(code) {
		background: #000000;
		color: #ffffff;
		padding: 2px 6px;
		border-radius: 4px;
		font-family: monospace;
		font-size: 0.88em;
	}
	.user-prose :global(code) {
		background: #240340;
		color: #e24bff;
	}
	.prose :global(pre) {
		background: #000000;
		color: #ffffff;
		padding: 12px;
		border-radius: 10px;
		overflow-x: auto;
		margin: 8px 0;
	}
	.prose :global(pre code) {
		background: transparent;
		padding: 0;
	}
	.prose :global(h1), .prose :global(h2), .prose :global(h3), .prose :global(h4) {
		font-weight: 800;
		margin: 0.8rem 0 0.4rem 0;
		color: inherit;
	}
	.prose :global(blockquote) {
		background: #240340;
		padding: 8px 12px;
		border-radius: 8px;
		margin: 8px 0;
	}

	.status-msg {
		padding: 60px 20px;
		text-align: center;
		font-size: 1.1rem;
	}

	.btn-primary {
		background: #e24bff;
		color: #240340;
		padding: 9px 22px;
		border-radius: 9999px;
		font-weight: 800;
		cursor: pointer;
		margin-top: 12px;
		user-select: none;
		transition:
			transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1),
			background-color 0.2s ease,
			color 0.2s ease;
	}

	.btn-primary:hover {
		transform: translateY(-2px) scale(1.04);
	}

	.btn-primary:active {
		transform: scale(0.93);
	}

	@media (max-width: 800px) {
		.stamp-transcript-app {
			flex-direction: column;
		}
		.sidebar {
			width: 100%;
			height: auto;
			border-radius: 0;
		}
		.main-content {
			height: auto;
		}
		.top-nav-bar {
			margin: 12px;
			flex-direction: column;
			border-radius: 16px;
		}
		.stream-container {
			padding: 16px;
		}
	}
</style>
