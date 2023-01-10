export type ThemeType = 'onLight' | 'onDark';

export const storeThemeValue = (value: ThemeType) => {
  localStorage.setItem('theme', value);
};

export const getThemeValue = (): boolean => {
  const theme = localStorage.getItem('theme');
  return translateTheme(theme) as boolean;
};

export const getThemeString = (): ThemeType => translateTheme(getThemeValue()) as ThemeType;

export const translateTheme = <T extends boolean | string | null>(theme: T): T extends boolean ? ThemeType : boolean => {
  if (typeof theme === 'string') {
    return (theme === 'onDark') as T extends boolean ? ThemeType : boolean;
  }
  return (theme ? 'onDark' : 'onLight') as T extends boolean ? ThemeType : boolean;
};
