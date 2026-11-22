import { type FC, type FormEvent, type KeyboardEvent, useRef } from 'react';
import { useTranslation } from 'react-i18next';

// components
import ErrorBanner from '../ErrorBanner';

// styles
import styles from './MessageComposer.module.css';

// types
import type { Props } from './types';

const MessageComposer: FC<Props> = ({ disabled = false, error, onChange, onClearError, onSubmit, value }) => {
  const { t } = useTranslation();
  // refs
  const formRef = useRef<HTMLFormElement | null>(null);
  // callbacks
  const handleSubmit = (event: FormEvent<HTMLFormElement>): void => {
    event.preventDefault();

    if (disabled || value.trim().length <= 0) {
      return;
    }

    onSubmit();
  };
  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>): void => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      formRef.current?.requestSubmit();
    }
  };

  return (
    <div className={styles.container}>
      {error && (
        <div className={styles.banner}>
          <ErrorBanner message={error} onDismiss={onClearError} />
        </div>
      )}

      <form className={styles.form} onSubmit={handleSubmit} ref={formRef}>
        <label className={styles.srOnly} htmlFor="message-composer-input">
          {t('labels.composerPlaceholder')}
        </label>

        <textarea
          className={styles.textarea}
          disabled={disabled}
          id="message-composer-input"
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={t('labels.composerPlaceholder')}
          rows={1}
          value={value}
        />

        <button className={styles.send} disabled={disabled || value.trim().length <= 0} type="submit">
          {t('labels.send')}
        </button>
      </form>
    </div>
  );
};

MessageComposer.displayName = 'MessageComposer';

export default MessageComposer;
