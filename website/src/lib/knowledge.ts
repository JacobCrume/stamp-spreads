export interface BotResponse {
	topicId: string;
	topicTitle: string;
	answer: string;
	isRefusal?: boolean;
}

export interface Topic {
	id: string;
	title: string;
	keywords: string[];
	patterns: RegExp[];
	answer: string;
	isRefusal?: boolean;
}

export const TOPICS: Topic[] = [
	{
		id: 'medical_advice',
		title: 'Medical & Health Guidance',
		isRefusal: true,
		keywords: [
			'stomach',
			'cure',
			'health',
			'sick',
			'digestion',
			'remedy',
			'treat',
			'disease',
			'illness',
			'medical',
			'gut',
			'nausea',
			'pain',
			'heal',
			'doctor'
		],
		patterns: [
			/\b(stomach|tummy|gut|digest|digestive|health|healthy|medical|medicine|cure|treat|remedy|sick|pain)\b/i,
			/help (my|with|for) (stomach|health|digestion|gut)/i
		],
		answer:
			'Stamp is a food spread for toast, not a medical or therapeutic treatment. We do not provide health advice and make no therapeutic claims. Stamp does not prevent, treat, or cure any medical condition. If you have digestive or health concerns, please consult a qualified medical professional.'
	},
	{
		id: 'claim_bans',
		title: 'Dietary & Certification Claims',
		isRefusal: true,
		keywords: [
			'gluten-free',
			'gluten free',
			'celiac',
			'coeliac',
			'organic',
			'low-sugar',
			'low sugar',
			'sugar-free',
			'keto',
			'better for you',
			'diet'
		],
		patterns: [
			/\bgluten[-\s]?free\b/i,
			/\borganic\b/i,
			/\blow[-\s]?sugar\b/i,
			/\bsugar[-\s]?free\b/i,
			/\bbetter for you\b/i,
			/\b(diet|slimming|weight loss)\b/i,
			/\b(celiac|coeliac)\b/i
		],
		answer:
			"Stamp does not make organic, gluten-free, low-sugar, or 'better for you' claims. In fact, our Yeast extract flavour contains gluten from barley malt extract (15.5%), and all sheets are packed in a facility that handles milk, gluten, and peanuts. We never display unverified certification badges or health claims."
	},
	{
		id: 'crushed_sheet',
		title: 'Damaged or Crushed Delivery',
		keywords: [
			'crushed',
			'damaged',
			'broken',
			'squashed',
			'ruined',
			'bent',
			'torn',
			'complaint',
			'melted'
		],
		patterns: [
			/\b(crushed|damaged|broken|squashed|ruined|smashed|smashed|bent|torn|melted)\b/i,
			/arrived (crushed|damaged|broken|bad)/i
		],
		answer:
			'We are truly sorry your sheet arrived damaged. Please take a quick photo of the damaged card sheet showing the batch number printed on the back, and send it to support@stampbreakfast.nz. We will immediately dispatch a fresh replacement sheet free of charge or issue a full refund.'
	},
	{
		id: 'allergens_peanut',
		title: 'Allergens & Peanut Information',
		keywords: [
			'nut',
			'nuts',
			'peanut',
			'peanuts',
			'allergen',
			'allergens',
			'allergy',
			'dairy',
			'milk',
			'lactose',
			'barley'
		],
		patterns: [
			/\b(peanut|peanuts|nuts?|allergen|allergens|allergy|allergic|dairy|milk|lactose)\b/i,
			/contain (nuts?|peanuts?|dairy|milk|gluten)/i
		],
		answer:
			'Yes, the Peanut stamp contains peanuts (96% roasted peanuts and 1.7% salt). For our other flavours: Salted Butter contains dairy (milk), and Yeast extract contains gluten from barley. Raspberry has no major allergens in its recipe. Importantly, every sheet is produced in a facility that handles milk, gluten, and peanuts, and mixed sheets contain all three.'
	},
	{
		id: 'jar_comparison',
		title: 'Comparison with Traditional Jars',
		keywords: [
			'compare',
			'comparison',
			'jar',
			'jars',
			'versus',
			'vs',
			'fix & fogg',
			'pics',
			'nutella',
			'why not a jar',
			'expensive'
		],
		patterns: [
			/\b(jar|jars|versus|vs|compare|comparison)\b/i,
			/compare (with|to|against) (a )?jar/i,
			/better than (a )?jar/i,
			/why (not|buy) (a )?jar/i
		],
		answer:
			"Traditional supermarket jars (like Fix & Fogg at ~$1.60/100g or Pic's at ~$2.05/100g) are built for home cupboards where you have a table knife and a sink. Stamp is priced at $6.25/100g ($5.00 for an 80 g sheet) because you are paying for single-serve release film, exact 10 g portions, and pocketable card packaging. It is designed for flats, offices, halls, or bags where washing knives or carrying 750 g jars is inconvenient."
	},
	{
		id: 'price',
		title: 'Pricing & Sheet Sizing',
		keywords: [
			'price',
			'pricing',
			'cost',
			'how much',
			'expensive',
			'dollar',
			'dollars',
			'nzd',
			'$',
			'cents',
			'pack size',
			'weight'
		],
		patterns: [
			/\b(price|pricing|cost|costs|expensive|nzd|\$)\b/i,
			/how much (is|does|are|for)/i,
			/what (is|are) the price/i
		],
		answer:
			'Every Stamp sheet is $5.00 NZD. A sheet contains 8 individual 10 g stamps (80 g total net weight), which equals $6.25 NZD per 100 g (or roughly $0.63 NZD per portion). Both single-flavour sheets and our 4-flavour mixed sheet are sold at the same $5.00 NZD price.'
	},
	{
		id: 'where_to_buy',
		title: 'Where to Buy & Availability',
		keywords: [
			'where to buy',
			'where can i buy',
			'purchase',
			'store',
			'stores',
			'supermarket',
			'supermarkets',
			'shop',
			'shops',
			'order',
			'online',
			'stockist',
			'stockists',
			'retail',
			'new world',
			'countdown',
			'paknsave',
			'woolworths'
		],
		patterns: [
			/where (can i|to|do i) (buy|get|purchase|find|order)/i,
			/\b(supermarket|supermarkets|stockist|stockists|stores?|shops?|retailers?)\b/i,
			/available (at|in)/i
		],
		answer:
			'Stamp is currently launching directly to consumers via our online website during our initial production run and making trial. We are not yet stocked on retail supermarket shelves (such as New World or Woolworths). You can explore the range and place direct trial orders right here through our website.'
	},
	{
		id: 'how_to_use',
		title: 'How to Use Stamp',
		keywords: [
			'how to use',
			'how do i use',
			'instructions',
			'apply',
			'application',
			'peel',
			'press',
			'toast',
			'steps',
			'directions',
			'knife'
		],
		patterns: [
			/how (do i|to|can i) (use|apply|put|eat)/i,
			/\b(instructions|directions|how does it work|how it works)\b/i,
			/\b(peel|press|application)\b/i
		],
		answer:
			'Using a Stamp is simple: 1. Keep the card sheet in your pantry. 2. Peel one 10 g stamp disc off the release film. 3. Press it directly onto freshly toasted, hot toast. 4. Wait a few seconds—the residual heat softens the spread into an even layer. No knife needed, and no washing up!'
	},
	{
		id: 'flavours',
		title: 'Flavour Lineup',
		keywords: [
			'flavour',
			'flavours',
			'flavor',
			'flavors',
			'varieties',
			'range',
			'butter',
			'raspberry',
			'yeast',
			'jam',
			'options'
		],
		patterns: [
			/\b(flavours?|flavors?|varieties|range|options|tastes?)\b/i,
			/what (flavours?|flavors?)/i,
			/which (flavours?|flavors?)/i
		],
		answer:
			'Stamp launches with four distinct flavours: 1. Salted Butter (shelf-stable cultured butterfat spread with salt). 2. Raspberry (cooked fruit paste with lemon and sugar). 3. Yeast extract (rich savoury spread with 80% yeast extract and 15.5% barley malt). 4. Peanut (96% roasted peanuts and salt). You can buy an 8-stamp single-flavour sheet or a mixed sheet with two of each.'
	},
	{
		id: 'what_is_stamp',
		title: 'What is Stamp',
		keywords: [
			'what is a stamp',
			'what is stamp',
			'what are stamps',
			'concept',
			'explain',
			'product',
			'sticker',
			'tell me about',
			'who is it for'
		],
		patterns: [
			/what (is|are) (a )?stamp/i,
			/tell me (about )?stamp/i,
			/explain stamp/i,
			/\b(concept|idea)\b/i
		],
		answer:
			'Stamp is a peel-and-press spread portion for toast. Each stamp is a thin 10 g disc of real spread on a food-safe release film, nested in a printed card sheet. You peel it off and press it onto hot toast—the heat softens it into an even spread. It gives you an exact single portion with no knife and no open jar to carry.'
	}
];

export const FALLBACK_RESPONSE: BotResponse = {
	topicId: 'unknown',
	topicTitle: 'Support Guide',
	answer:
		"I'm here to help with all questions about Stamp! You can ask about:\n\n• What Stamp is and how the peel-and-press system works\n• How to use it on hot toast\n• Our four launch flavours (Salted Butter, Raspberry, Yeast extract, Peanut)\n• Allergens, nutrition, and ingredient disclosures\n• Pricing ($5.00 NZD per 8-stamp sheet / $6.25 per 100 g)\n• Where to buy and availability\n• Replacements for damaged or crushed sheets\n• How Stamp compares to supermarket jars\n\nWhat would you like to know?"
};

export function matchQuestion(input: string): BotResponse {
	const text = input.trim();
	if (!text) {
		return FALLBACK_RESPONSE;
	}

	const lower = text.toLowerCase();

	// 1. Check high-priority refusals and specific triggers first
	// Medical advice
	if (
		/\b(stomach|tummy|gut|digest|digestive|health|healthy|medical|medicine|cure|treat|remedy|sick|illness|disease|nausea|doctor)\b/i.test(
			lower
		)
	) {
		const topic = TOPICS.find((t) => t.id === 'medical_advice')!;
		return { topicId: topic.id, topicTitle: topic.title, answer: topic.answer, isRefusal: true };
	}

	// Claim bans (gluten-free, organic, low sugar, etc.)
	if (
		/\b(gluten[-\s]?free|celiac|coeliac|organic|low[-\s]?sugar|sugar[-\s]?free|better for you|diet)\b/i.test(
			lower
		)
	) {
		const topic = TOPICS.find((t) => t.id === 'claim_bans')!;
		return { topicId: topic.id, topicTitle: topic.title, answer: topic.answer, isRefusal: true };
	}

	// Crushed / damaged
	if (/\b(crushed|damaged|broken|squashed|ruined|torn|melted|complaint)\b/i.test(lower)) {
		const topic = TOPICS.find((t) => t.id === 'crushed_sheet')!;
		return { topicId: topic.id, topicTitle: topic.title, answer: topic.answer };
	}

	// Jar comparison
	if (
		/\b(jar|jars|versus|vs|fix & fogg|pics|nutella)\b/i.test(lower) &&
		/\b(compare|comparison|versus|vs|than|why|expensive|different|difference)\b/i.test(lower)
	) {
		const topic = TOPICS.find((t) => t.id === 'jar_comparison')!;
		return { topicId: topic.id, topicTitle: topic.title, answer: topic.answer };
	}

	// Nut / peanut / allergen
	if (
		/\b(peanuts?|nuts?|allergen|allergens|allergy|allergic|dairy|milk|lactose)\b/i.test(lower) &&
		!/flavour|flavor|range|varieties/i.test(lower)
	) {
		const topic = TOPICS.find((t) => t.id === 'allergens_peanut')!;
		return { topicId: topic.id, topicTitle: topic.title, answer: topic.answer };
	}

	// How to use
	if (
		/how (do i|to|can i) (use|apply|put|eat)/i.test(lower) ||
		/\b(instructions|directions|how does it work)\b/i.test(lower) ||
		(lower.includes('how') && lower.includes('use'))
	) {
		const topic = TOPICS.find((t) => t.id === 'how_to_use')!;
		return { topicId: topic.id, topicTitle: topic.title, answer: topic.answer };
	}

	// Price / cost
	if (
		/\b(price|pricing|cost|costs|expensive|nzd|\$|dollars?|cents?)\b/i.test(lower) ||
		/how much/i.test(lower)
	) {
		const topic = TOPICS.find((t) => t.id === 'price')!;
		return { topicId: topic.id, topicTitle: topic.title, answer: topic.answer };
	}

	// Where to buy
	if (
		/where (can i|to|do i) (buy|get|purchase|find|order)/i.test(lower) ||
		/\b(supermarket|supermarkets|stockist|stockists|stores?|shops?|retailers?|where to buy)\b/i.test(
			lower
		) ||
		(lower.includes('where') && (lower.includes('buy') || lower.includes('purchase')))
	) {
		const topic = TOPICS.find((t) => t.id === 'where_to_buy')!;
		return { topicId: topic.id, topicTitle: topic.title, answer: topic.answer };
	}

	// Flavours
	if (
		/\b(flavours?|flavors?|varieties|tastes?)\b/i.test(lower) ||
		(/what/i.test(lower) && /flavour|flavor/i.test(lower))
	) {
		const topic = TOPICS.find((t) => t.id === 'flavours')!;
		return { topicId: topic.id, topicTitle: topic.title, answer: topic.answer };
	}

	// What is a Stamp
	if (
		/what (is|are) (a )?stamp/i.test(lower) ||
		/tell me (about )?stamp/i.test(lower) ||
		/what('s| is) this/i.test(lower) ||
		(lower.includes('what') && lower.includes('stamp'))
	) {
		const topic = TOPICS.find((t) => t.id === 'what_is_stamp')!;
		return { topicId: topic.id, topicTitle: topic.title, answer: topic.answer };
	}

	// Scoring fallback across remaining topics
	let bestTopic: Topic | null = null;
	let bestScore = 0;

	for (const topic of TOPICS) {
		let score = 0;
		for (const pat of topic.patterns) {
			if (pat.test(lower)) score += 3;
		}
		for (const kw of topic.keywords) {
			if (lower.includes(kw.toLowerCase())) score += 1;
		}
		if (score > bestScore) {
			bestScore = score;
			bestTopic = topic;
		}
	}

	if (bestTopic && bestScore >= 2) {
		return {
			topicId: bestTopic.id,
			topicTitle: bestTopic.title,
			answer: bestTopic.answer,
			isRefusal: bestTopic.isRefusal
		};
	}

	return FALLBACK_RESPONSE;
}
