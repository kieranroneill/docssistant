import { createContext, useContext } from 'react';

// enums
import { ThemeEnum } from '@/platform/application/enums';

// types
import type { ThemeContextValue } from '@/platform/application/types';

export const ThemeContext = createContext<ThemeContextValue>({
  setTheme: () => {},
  theme: ThemeEnum.System,
});

/**
 * Reads the active theme preference and a setter to change it. Must be used within a ThemeProvider.
 * @returns {ThemeContextValue} The active theme preference and its setter.
 */
export default function useTheme(): ThemeContextValue {
  return useContext(ThemeContext);
}
