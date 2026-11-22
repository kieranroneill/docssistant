import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

// ui
import Button from '@/platform/application/components/Button';

// types
import type { Props } from './types';

const ErrorBanner: FC<Props> = ({ message, onDismiss, onRetry }) => {
  const { t } = useTranslation();

  return (
    <div className="flex items-center gap-2 rounded-md bg-destructive/10 px-4 py-2 text-destructive" role="alert">
      <p className="flex-1 text-sm first-letter:uppercase">{message}</p>

      {(onRetry || onDismiss) && (
        <div className="flex shrink-0 gap-1">
          {onRetry && (
            <Button onClick={onRetry} size="sm" type="button" variant="outline">
              {t('labels.retry')}
            </Button>
          )}

          {onDismiss && (
            <Button onClick={onDismiss} size="sm" type="button" variant="ghost">
              {t('labels.dismiss')}
            </Button>
          )}
        </div>
      )}
    </div>
  );
};

ErrorBanner.displayName = 'ErrorBanner';

export default ErrorBanner;
