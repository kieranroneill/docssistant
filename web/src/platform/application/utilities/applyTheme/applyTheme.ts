// enums
import { ThemeEnum } from '@/platform/application/enums';

/**
 * Applies a theme preference to the document by toggling the "dark" class the stylesheet keys its dark variables off.
 * The system preference is resolved at the time of the call.
 * @param {ThemeEnum} theme - The theme preference to apply.
 */
export default function applyTheme(theme: ThemeEnum): void {
  const isDark =
    theme === ThemeEnum.Dark ||
    (theme === ThemeEnum.System && window.matchMedia('(prefers-color-scheme: dark)').matches);

  document.documentElement.classList.toggle('dark', isDark);
}
