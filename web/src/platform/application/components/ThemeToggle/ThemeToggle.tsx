import { type FC } from 'react';
import { useTranslation } from 'react-i18next';
import { Monitor, Moon, Sun, type LucideIcon } from 'lucide-react';

// components
import Button from '@/platform/application/components/Button';
import Tooltip from '@/platform/application/components/Tooltip';

// enums
import { ThemeEnum } from '@/platform/application/enums';

// hooks
import useTheme from '@/platform/application/hooks/useTheme';

// types
import type { Props } from './types';

const SEQUENCE: ThemeEnum[] = [ThemeEnum.Light, ThemeEnum.Dark, ThemeEnum.System];
const ICONS: Record<ThemeEnum, LucideIcon> = {
  [ThemeEnum.Dark]: Moon,
  [ThemeEnum.Light]: Sun,
  [ThemeEnum.System]: Monitor,
};
const LABELS: Record<ThemeEnum, string> = {
  [ThemeEnum.Dark]: 'labels.themeDark',
  [ThemeEnum.Light]: 'labels.themeLight',
  [ThemeEnum.System]: 'labels.themeSystem',
};

const ThemeToggle: FC<Props> = ({ className }) => {
  const { t } = useTranslation();
  // hooks
  const { setTheme, theme } = useTheme();
  // memos
  const Icon = ICONS[theme];
  const label = t(LABELS[theme]);

  return (
    <Tooltip.Provider>
      <Tooltip>
        <Tooltip.Trigger asChild>
          <Button
            aria-label={t('labels.changeTheme', { theme: label })}
            className={className}
            onClick={() => setTheme(SEQUENCE[(SEQUENCE.indexOf(theme) + 1) % SEQUENCE.length])}
            size="icon"
            type="button"
            variant="ghost"
          >
            <Icon aria-hidden="true" className="h-4 w-4" />
          </Button>
        </Tooltip.Trigger>

        <Tooltip.Content>{label}</Tooltip.Content>
      </Tooltip>
    </Tooltip.Provider>
  );
};

ThemeToggle.displayName = 'ThemeToggle';

export default ThemeToggle;
