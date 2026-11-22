import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

// styles
import styles from './TypingIndicator.module.css';

const TypingIndicator: FC = () => {
  const { t } = useTranslation();

  return (
    <div aria-live="polite" className={styles.row} role="status">
      <span className={styles.srOnly}>
        {t('labels.assistant')}: {t('labels.sending')}
      </span>

      <div aria-hidden="true" className={styles.bubble}>
        <span className={styles.dot} />
        <span className={styles.dot} />
        <span className={styles.dot} />
      </div>
    </div>
  );
};

TypingIndicator.displayName = 'TypingIndicator';

export default TypingIndicator;
