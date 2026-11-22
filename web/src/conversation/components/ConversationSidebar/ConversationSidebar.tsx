import { type FC, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Plus, X } from 'lucide-react';

// components
import ConversationListItem from '../ConversationListItem';
import ErrorBanner from '../ErrorBanner';

// hooks
import useVersion from '@/platform/application/hooks/useVersion';

// ui
import Button from '@/platform/application/components/Button';

// types
import type { Props } from './types';

const ConversationSidebar: FC<Props> = ({
  activeConversationId,
  conversations,
  error,
  isLoading,
  isOpen,
  logger,
  onClose,
  onNewConversation,
  onReload,
  onSelect,
}) => {
  const { t } = useTranslation();
  // hooks
  const { version } = useVersion(logger);
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
      {isOpen && <div className="fixed inset-0 z-20 bg-black/40 md:hidden" onClick={onClose} />}

      <nav
        aria-label={t('headings.conversations')}
        className={`fixed inset-y-0 left-0 z-30 flex w-[var(--sidebar-width)] flex-col border-r border-border bg-background transition-transform duration-200 md:static md:z-auto md:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        id="conversation-sidebar"
      >
        <div className="border-b border-border p-4">
          <h1 className="m-0 truncate text-lg font-semibold">{t('titles.app')}</h1>
          {version && (
            <p className="m-0 mt-0.5 truncate text-xs text-muted-foreground">
              {t('labels.version', { version: version.version })}
            </p>
          )}
        </div>

        <div className="flex min-w-0 items-center justify-between gap-2 border-b border-border p-4">
          <h2 className="m-0 min-w-0 truncate text-base font-semibold">{t('headings.conversations')}</h2>

          <div className="flex shrink-0 items-center gap-1">
            <Button
              aria-label={t('labels.newConversation')}
              onClick={onNewConversation}
              size="icon"
              type="button"
              variant="outline"
            >
              <Plus className="h-4 w-4" />
            </Button>

            <Button
              aria-label={t('labels.closeSidebar')}
              className="md:hidden"
              onClick={onClose}
              size="icon"
              type="button"
              variant="ghost"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-2">
          {isLoading && (
            <p className="p-4 text-center text-sm text-muted-foreground">{t('labels.loadingConversations')}</p>
          )}

          {!isLoading && error && <ErrorBanner message={error} onRetry={onReload} />}

          {!isLoading && !error && conversations.length <= 0 && (
            <p className="p-4 text-center text-sm text-muted-foreground">{t('captions.noConversations')}</p>
          )}

          {!isLoading && !error && conversations.length > 0 && (
            <ul className="m-0 flex list-none flex-col gap-0.5 p-0">
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
