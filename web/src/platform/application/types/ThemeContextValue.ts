// enums
import type { ThemeEnum } from '@/platform/application/enums';

interface ThemeContextValue {
  setTheme: (theme: ThemeEnum) => void;
  theme: ThemeEnum;
}

export default ThemeContextValue;
