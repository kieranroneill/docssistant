import { type FC, useEffect, useMemo, useState } from 'react';

// enums
import { ThemeEnum } from '@/platform/application/enums';

// hooks
import { ThemeContext } from '@/platform/application/hooks/useTheme';

// types
import type { ThemeContextValue } from '@/platform/application/types';
import type { Props } from './types';

// utilities
import applyTheme from '@/platform/application/utilities/applyTheme';
import readStoredTheme from '@/platform/application/utilities/readStoredTheme';
import storeTheme from '@/platform/application/utilities/storeTheme';

const ThemeProvider: FC<Props> = ({ children }) => {
  // states
  const [theme, setTheme] = useState<ThemeEnum>(readStoredTheme);
  // memos
  const value = useMemo<ThemeContextValue>(
    () => ({
      setTheme: (value) => {
        setTheme(value);
        storeTheme(value);
      },
      theme,
    }),
    [theme]
  );
  // effects
  useEffect(() => {
    applyTheme(theme);

    // when following the system, the document must be updated as the system preference changes
    if (theme !== ThemeEnum.System) {
      return;
    }

    const query = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (): void => applyTheme(ThemeEnum.System);

    query.addEventListener('change', handleChange);

    return () => query.removeEventListener('change', handleChange);
  }, [theme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};

ThemeProvider.displayName = 'ThemeProvider';

export default ThemeProvider;
