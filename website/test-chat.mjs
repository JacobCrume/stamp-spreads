// Comprehensive test suite for Stamp Chatbot & OpenRouter Architecture
import { matchQuestion } from './src/lib/knowledge.ts';
import { askOpenRouter, getOpenRouterConfig, STAMP_SYSTEM_PROMPT } from './src/lib/server/openrouter.ts';

let allPassed = true;

function assert(condition, description) {
	if (condition) {
		console.log(`[PASS] ${description}`);
	} else {
		console.error(`[FAIL] ${description}`);
		allPassed = false;
	}
}

console.log('=== TEST SUITE 1: Spec Engine Knowledge Matching ===');
const testCases = [
	{
		query: 'What is a Stamp?',
		expectedSnippet: 'peel-and-press',
		shouldRefuse: false
	},
	{
		query: 'How do I use it?',
		expectedSnippet: 'residual heat',
		shouldRefuse: false
	},
	{
		query: 'What flavours are there?',
		expectedSnippet: 'Salted Butter',
		shouldRefuse: false
	},
	{
		query: 'Does Peanut stamp contain nuts?',
		expectedSnippet: 'peanuts',
		shouldRefuse: false
	},
	{
		query: 'Is Stamp gluten free?',
		expectedSnippet: 'does not make organic, gluten-free',
		shouldRefuse: true
	},
	{
		query: 'Can Stamp heal my stomach ulcers?',
		expectedSnippet: 'not a medical or therapeutic treatment',
		shouldRefuse: true
	},
	{
		query: 'My card sheet arrived crushed and melted',
		expectedSnippet: 'support@stampbreakfast.nz',
		shouldRefuse: false
	},
	{
		query: 'Why should I pay $5 when a jar is cheaper?',
		expectedSnippet: 'Traditional supermarket jars',
		shouldRefuse: false
	}
];

for (const tc of testCases) {
	const res = matchQuestion(tc.query);
	const snippetMatched = res.answer.toLowerCase().includes(tc.expectedSnippet.toLowerCase());
	const refusalMatched = !tc.shouldRefuse || !!res.isRefusal;
	assert(
		snippetMatched && refusalMatched,
		`Question "${tc.query}" -> topic: ${res.topicId} (refusal: ${res.isRefusal || false})`
	);
}

console.log('\n=== TEST SUITE 2: System Prompt Adherence & Guardrails ===');
assert(
	STAMP_SYSTEM_PROMPT.includes('peel-and-press spread disc for toast'),
	'System prompt defines peel-and-press format'
);
assert(
	STAMP_SYSTEM_PROMPT.includes('$5.00 NZD retail'),
	'System prompt locks $5.00 retail price'
);
assert(
	STAMP_SYSTEM_PROMPT.includes('80%') && STAMP_SYSTEM_PROMPT.includes('15.5%'),
	'System prompt specifies exact industrial recipe for Yeast extract'
);
assert(
	STAMP_SYSTEM_PROMPT.includes('NO Medical or Therapeutic Claims'),
	'System prompt enforces strict FSANZ medical refusal'
);
assert(
	STAMP_SYSTEM_PROMPT.includes('NO Unbacked Dietary or Certification Claims'),
	'System prompt bans unbacked organic and gluten-free badges'
);

console.log('\n=== TEST SUITE 3: OpenRouter Configuration & Clean Fallback ===');
const initialConfig = getOpenRouterConfig();
assert(
	initialConfig.model === 'openai/gpt-4o-mini',
	`Default model is low-latency 'openai/gpt-4o-mini' (got: ${initialConfig.model})`
);

// Verify askOpenRouter fallback when no API key is provided
const fallbackRes = await askOpenRouter('What is a Stamp?');
assert(
	fallbackRes.success === false && fallbackRes.source === 'fallback_deterministic',
	'askOpenRouter falls back cleanly when OPENROUTER_API_KEY is not set'
);
assert(
	fallbackRes.fallbackReason === 'NO_API_KEY',
	`Fallback reason is NO_API_KEY (got: ${fallbackRes.fallbackReason})`
);

console.log('\n=== TEST SUITE 4: LLM Refusal Pattern Detection Regex ===');
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

const sampleRefusals = [
	'Stamp is a food spread and is not a medical product.',
	'We make no therapeutic claims for toast spreads. Consult a medical professional.',
	'Stamp is not gluten-free as it contains barley malt extract.',
	'Stamp does not make organic claims or hold certifications.'
];

for (const sample of sampleRefusals) {
	const matched = refusalPatterns.some((p) => p.test(sample));
	assert(matched, `Refusal regex accurately matches LLM response: "${sample}"`);
}

if (!allPassed) {
	console.error('\n❌ One or more tests failed!');
	process.exit(1);
} else {
	console.log('\n✅ All test suites passed successfully!');
}
