// constants
import { THEME_STORAGE_KEY } from '@/platform/application/constants';

// enums
import { ThemeEnum } from '@/platform/application/enums';

/**
 * Reads the stored theme preference. Storage can be unavailable, such as when the browser blocks it, so an unreadable
 * or unrecognised value falls back to following the system preference.
 * @returns {ThemeEnum} The stored theme preference.
 */
export default function readStoredTheme(): ThemeEnum {
  let value: string | null;

  try {
    value = window.localStorage.getItem(THEME_STORAGE_KEY);
  } catch {
    return ThemeEnum.System;
  }

  if (!Object.values<string>(ThemeEnum).includes(value ?? '')) {
    return ThemeEnum.System;
  }

  return value as ThemeEnum;
}
