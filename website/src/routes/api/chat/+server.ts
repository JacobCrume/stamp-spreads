import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { askOpenRouter, getOpenRouterConfig, type ChatMessage } from '../../../lib/server/openrouter';
import { matchQuestion } from '../../../lib/knowledge';

export const GET: RequestHandler = async () => {
	const config = getOpenRouterConfig();
	return json({
		status: 'ok',
		openrouterConfigured: !!config.apiKey,
		model: config.model,
		fallbackAvailable: true
	});
};

export const POST: RequestHandler = async ({ request }) => {
	try {
		const body = await request.json();
		const message = typeof body?.message === 'string' ? body.message.trim() : '';
		const rawHistory = Array.isArray(body?.history) ? body.history : [];

		if (!message) {
			return json({ error: 'Message is required and cannot be empty.' }, { status: 400 });
		}

		interface HistoryInput {
			role: string;
			content: string;
		}

		// Filter and sanitize chat history
		const history: ChatMessage[] = rawHistory
			.filter(
				(item: unknown): item is HistoryInput =>
					typeof item === 'object' &&
					item !== null &&
					'role' in item &&
					'content' in item &&
					typeof (item as Record<string, unknown>).role === 'string' &&
					typeof (item as Record<string, unknown>).content === 'string'
			)
			.map((item: HistoryInput) => ({
				role: (['user', 'assistant', 'system'].includes(item.role)
					? item.role
					: 'user') as ChatMessage['role'],
				content: item.content.slice(0, 1000)
			}));

		// 1. Attempt OpenRouter AI completion
		const openRouterRes = await askOpenRouter(message, history);

		if (openRouterRes.success && openRouterRes.answer) {
			// Check if LLM output reflects a regulatory refusal response
			const lowerAns = openRouterRes.answer.toLowerCase();
			const refusalPatterns = [
				/not a medical/i,
				/no therapeutic/i,
				/not therapeutic/i,
				/health advice/i,
				/consult a (qualified )?(doctor|medical|physician)/i,
				/not prevent,? treat,? or cure/i,
				/not gluten[-\s]?free/i,
				/does not make organic/i,
				/does not claim to be organic/i,
				/not certified organic/i
			];
			const isRefusal = refusalPatterns.some((p) => p.test(lowerAns));

			const topicTitle = isRefusal
				? (lowerAns.includes('gluten') || lowerAns.includes('organic')
					? 'Dietary & Certification Refusal'
					: 'Medical & Therapeutic Refusal')
				: `OpenRouter · ${openRouterRes.model || 'AI'}`;

			return json({
				answer: openRouterRes.answer,
				source: 'openrouter',
				model: openRouterRes.model,
				topicTitle,
				isRefusal,
				timestamp: new Date().toISOString()
			});
		}

		// 2. Fallback cleanly to our deterministic locked spec engine
		const deterministic = matchQuestion(message);

		return json({
			answer: deterministic.answer,
			source: 'fallback_deterministic',
			topicTitle: deterministic.topicTitle,
			isRefusal: deterministic.isRefusal,
			fallbackReason: openRouterRes.fallbackReason || 'DETERMINISTIC_FALLBACK',
			model: openRouterRes.model,
			timestamp: new Date().toISOString()
		});
	} catch (err: unknown) {
		const errorMsg = err instanceof Error ? err.message : String(err);
		console.error('Chat endpoint error:', errorMsg);

		// Even on JSON parse or unexpected error, serve fallback
		return json(
			{
				answer:
					"I encountered a temporary processing issue. Here is Stamp's standard guide: Stamp is a 10 g peel-and-press toast spread ($5.00 NZD / sheet of 8). Available in Salted Butter, Raspberry, Yeast extract, and Peanut. For support questions email support@stampbreakfast.nz.",
				source: 'fallback_deterministic',
				topicTitle: 'Error Fallback',
				error: errorMsg
			},
			{ status: 200 }
		);
	}
};
