export interface ColorScheme {
	primary: string;
	secondary: string;
	tertiary: string;
}

export type SectionTheme = 'hero' | 'steps' | 'butter' | 'raspberry' | 'yeast' | 'peanut' | 'mixed';

export const THEME_PALETTES: Record<SectionTheme, ColorScheme> = {
	hero: {
		primary: '#e24bff',    // Wordmark, primary actions, highlights
		secondary: '#240340',  // Screen background
		tertiary: '#3b0764'    // Header background, cards, solid badges
	},
	steps: {
		primary: '#e24bff',
		secondary: '#240340',
		tertiary: '#3b0764'
	},
	butter: {
		primary: '#ffd640',    // Electric Butter Gold
		secondary: '#4a3000',  // Roasted Caramel Brown (screen background)
		tertiary: '#2d1d00'    // Deep Roast Umber (header & cards)
	},
	raspberry: {
		primary: '#ff467a',    // Neon Wild Raspberry
		secondary: '#460820',  // Dark Berry Maroon (screen background)
		tertiary: '#2d0414'    // Deepest Maroon (header & cards)
	},
	yeast: {
		primary: '#e24bff',    // Electric Violet
		secondary: '#240340',  // Deep Night Ink (screen background)
		tertiary: '#18012b'    // Deepest Violet (header & cards)
	},
	peanut: {
		primary: '#ff8c30',    // Roasted Peanut Ochre
		secondary: '#4e2408',  // Deep Peanut Umber (screen background)
		tertiary: '#2d1403'    // Dark Roast Peanut (header & cards)
	},
	mixed: {
		primary: '#e24bff',
		secondary: '#240340',
		tertiary: '#3b0764'
	}
};

// THE SINGLE COLORSCHEME OBJECT THAT ALL ELEMENTS REFER TO
export const colorScheme = $state<ColorScheme>({
	primary: '#e24bff',
	secondary: '#240340',
	tertiary: '#3b0764'
});

let activeSection: SectionTheme = 'hero';

export function getSectionTheme(): SectionTheme {
	return activeSection;
}

export function setSectionTheme(theme: SectionTheme) {
	if (activeSection === theme) return;
	activeSection = theme;
	const palette = THEME_PALETTES[theme] || THEME_PALETTES.hero;
	colorScheme.primary = palette.primary;
	colorScheme.secondary = palette.secondary;
	colorScheme.tertiary = palette.tertiary;
}

