// constants
import { THEME_STORAGE_KEY } from '@/platform/application/constants';

// types
import type { ThemeEnum } from '@/platform/application/enums';

/**
 * Stores the theme preference. Storage can be unavailable, such as when the browser blocks it, in which case the
 * preference simply does not persist between sessions.
 * @param {ThemeEnum} theme - The theme preference to store.
 */
export default function storeTheme(theme: ThemeEnum): void {
  try {
    window.localStorage.setItem(THEME_STORAGE_KEY, theme);
  } catch {
    // storage is unavailable, the preference only lasts for this session
  }
}
