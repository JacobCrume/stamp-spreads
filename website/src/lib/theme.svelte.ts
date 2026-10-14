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
		primary: '#ffd640',    // Electric Butter Gold (wordmark on header, button accents, pack front)
		secondary: '#4a3000',  // Roasted Caramel Brown screen background
		tertiary: '#2d1d00'    // Deep Umber (header background, pack back, elevated surfaces)
	},
	raspberry: {
		primary: '#ff467a',    // Neon Wild Raspberry (wordmark on header, button accents, pack front)
		secondary: '#460820',  // Rich Berry screen background
		tertiary: '#2d0414'    // Dark Berry Maroon (header background, pack back, elevated surfaces)
	},
	yeast: {
		primary: '#e24bff',    // Electric Violet (wordmark on header, button accents, pack front)
		secondary: '#240340',  // Deep Night Ink screen background
		tertiary: '#18012b'    // Deepest Midnight Purple (header background, pack back, elevated surfaces)
	},
	peanut: {
		primary: '#ff8c30',    // Roasted Peanut Ochre (wordmark on header, button accents, pack front)
		secondary: '#4e2408',  // Deep Peanut Umber screen background
		tertiary: '#2d1403'    // Dark Roasted Nut Brown (header background, pack back, elevated surfaces)
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

