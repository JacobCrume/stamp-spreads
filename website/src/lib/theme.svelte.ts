export type SectionTheme = 'hero' | 'steps' | 'butter' | 'raspberry' | 'yeast' | 'peanut' | 'mixed';

export const themeState = $state<{ active: SectionTheme }>({
	active: 'hero'
});

export function setSectionTheme(theme: SectionTheme) {
	themeState.active = theme;
}
