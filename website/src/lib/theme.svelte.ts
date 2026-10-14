export interface ColorScheme {
	primary: string;
	secondary: string;
	tertiary: string;
}

export type SectionTheme = 'hero' | 'steps' | 'butter' | 'raspberry' | 'yeast' | 'peanut' | 'mixed';

export const THEME_PALETTES: Record<SectionTheme, ColorScheme> = {
	hero: {
		primary: '#e24bff',    // Wordmark, primary actions, highlights
		secondary: '#240340',  // Screen background (Deep Night Ink)
		tertiary: '#3b0764'    // Header background, cards, solid badges
	},
	steps: {
		primary: '#e24bff',
		secondary: '#240340',
		tertiary: '#3b0764'
	},
	butter: {
		primary: '#ffd640',    // Electric Butter Gold (wordmark on header, button accents)
		secondary: '#ffd640',  // Bright Electric Butter Gold screen background (as before)
		tertiary: '#4a3000'    // Roasted Caramel Brown (header bg, cards, text contrast)
	},
	raspberry: {
		primary: '#ff467a',    // Neon Wild Raspberry (wordmark on header, button accents)
		secondary: '#ff467a',  // Bright Neon Wild Raspberry screen background (as before)
		tertiary: '#460820'    // Dark Berry Maroon (header bg, cards, text contrast)
	},
	yeast: {
		primary: '#e24bff',    // Electric Violet (wordmark on header, button accents)
		secondary: '#e24bff',  // Bright Electric Violet screen background (as before)
		tertiary: '#240340'    // Deep Night Ink (header bg, cards, text contrast)
	},
	peanut: {
		primary: '#ff8c30',    // Roasted Peanut Ochre (wordmark on header, button accents)
		secondary: '#ff8c30',  // Bright Roasted Peanut Ochre screen background (as before)
		tertiary: '#4e2408'    // Deep Peanut Umber (header bg, cards, text contrast)
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

