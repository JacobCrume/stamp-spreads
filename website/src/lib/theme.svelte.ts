export type SectionTheme = 'hero' | 'steps' | 'butter' | 'raspberry' | 'yeast' | 'peanut' | 'mixed';

export interface ThemeColors {
	screenBg: string;
	headerBg: string;
	border: string;
	text: string;
	btnBg: string;
	btnText: string;
}

export const THEME_CONFIG: Record<SectionTheme, ThemeColors> = {
	hero: {
		screenBg: '#240340',
		headerBg: '#3b0764',
		border: '#e24bff',
		text: '#e24bff',
		btnBg: '#e24bff',
		btnText: '#240340'
	},
	steps: {
		screenBg: '#240340',
		headerBg: '#3b0764',
		border: '#e24bff',
		text: '#e24bff',
		btnBg: '#e24bff',
		btnText: '#240340'
	},
	butter: {
		screenBg: '#ffd640',
		headerBg: '#4a3000',
		border: '#4a3000',
		text: '#ffd640',
		btnBg: '#ffd640',
		btnText: '#4a3000'
	},
	raspberry: {
		screenBg: '#ff467a',
		headerBg: '#460820',
		border: '#460820',
		text: '#ff467a',
		btnBg: '#ff467a',
		btnText: '#460820'
	},
	yeast: {
		screenBg: '#e24bff',
		headerBg: '#3b0764',
		border: '#3b0764',
		text: '#e24bff',
		btnBg: '#e24bff',
		btnText: '#3b0764'
	},
	peanut: {
		screenBg: '#ff8c30',
		headerBg: '#4e2408',
		border: '#4e2408',
		text: '#ff8c30',
		btnBg: '#ff8c30',
		btnText: '#4e2408'
	},
	mixed: {
		screenBg: '#240340',
		headerBg: '#3b0764',
		border: '#e24bff',
		text: '#e24bff',
		btnBg: '#e24bff',
		btnText: '#240340'
	}
};

export const themeState = $state<{ active: SectionTheme }>({
	active: 'hero'
});

export function setSectionTheme(theme: SectionTheme) {
	if (themeState.active !== theme) {
		themeState.active = theme;
	}
}
