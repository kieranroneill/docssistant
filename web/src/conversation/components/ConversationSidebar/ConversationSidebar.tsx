import { type FC, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

// components
import ConversationListItem from '../ConversationListItem';
import ErrorBanner from '../ErrorBanner';

// styles
import styles from './ConversationSidebar.module.css';

// types
import type { Props } from './types';

const ConversationSidebar: FC<Props> = ({
  activeConversationId,
  conversations,
  error,
  isLoading,
  isOpen,
  onClose,
  onNewConversation,
  onReload,
  onSelect,
}) => {
  const { t } = useTranslation();
  // effects
  useEffect(() => {
    if (!isOpen) {
      return;
    }

    const handleKeyDown = (event: KeyboardEvent): void => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  return (
    <>
      {isOpen && <div className={styles.backdrop} onClick={onClose} />}

      <nav
        aria-label={t('headings.conversations')}
        className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}
        id="conversation-sidebar"
      >
        <div className={styles.header}>
          <h2 className={styles.heading}>{t('headings.conversations')}</h2>

          <div className={styles.headerActions}>
            <button className={styles.newButton} onClick={onNewConversation} type="button">
              {t('labels.newConversation')}
            </button>

            <button aria-label={t('labels.closeSidebar')} className={styles.iconButton} onClick={onClose} type="button">
              ✕
            </button>
          </div>
        </div>

        <div className={styles.body}>
          {isLoading && <p className={styles.status}>{t('labels.loadingConversations')}</p>}

          {!isLoading && error && <ErrorBanner message={error} onRetry={onReload} />}

          {!isLoading && !error && conversations.length <= 0 && (
            <p className={styles.status}>{t('captions.noConversations')}</p>
          )}

          {!isLoading && !error && conversations.length > 0 && (
            <ul className={styles.list}>
              {conversations.map((conversation) => (
                <li key={conversation.id}>
                  <ConversationListItem
                    conversation={conversation}
                    isActive={conversation.id === activeConversationId}
                    onSelect={onSelect}
                  />
                </li>
              ))}
            </ul>
          )}
        </div>
      </nav>
    </>
  );
};

ConversationSidebar.displayName = 'ConversationSidebar';

export default ConversationSidebar;
