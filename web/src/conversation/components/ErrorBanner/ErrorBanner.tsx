import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

// styles
import styles from './ErrorBanner.module.css';

// types
import type { Props } from './types';

const ErrorBanner: FC<Props> = ({ message, onDismiss, onRetry }) => {
  const { t } = useTranslation();

  return (
    <div className={styles.banner} role="alert">
      <p className={styles.message}>{message}</p>

      {(onRetry || onDismiss) && (
        <div className={styles.actions}>
          {onRetry && (
            <button className={styles.button} onClick={onRetry} type="button">
              {t('labels.retry')}
            </button>
          )}

          {onDismiss && (
            <button className={styles.button} onClick={onDismiss} type="button">
              {t('labels.dismiss')}
            </button>
          )}
        </div>
      )}
    </div>
  );
};

ErrorBanner.displayName = 'ErrorBanner';

export default ErrorBanner;
