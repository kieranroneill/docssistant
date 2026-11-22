import { type FC, useCallback, useState } from 'react';
import { useTranslation } from 'react-i18next';

// components
import ConversationSidebar from '@/conversation/components/ConversationSidebar';
import EmptyConversationState from '@/conversation/components/EmptyConversationState';
import ErrorBanner from '@/conversation/components/ErrorBanner';
import MessageComposer from '@/conversation/components/MessageComposer';
import MessageList from '@/conversation/components/MessageList';

// hooks
import useChat from '@/conversation/hooks/useChat';
import useConversations from '@/conversation/hooks/useConversations';

// styles
import styles from './ConversationContainer.module.css';

// types
import type { Props } from './types';

const ConversationContainer: FC<Props> = ({ logger }) => {
  const { t } = useTranslation();
  // states
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);
  // hooks
  const conversations = useConversations(logger);
  const chat = useChat({ logger, onSent: conversations.reload });
  // callbacks
  const handleSelect = useCallback(
    (id: string) => {
      chat.selectConversation(id);
      setIsSidebarOpen(false);
    },
    [chat]
  );
  const handleNewConversation = useCallback(() => {
    chat.selectConversation(null);
    setIsSidebarOpen(false);
  }, [chat]);
  const mobileTitle = chat.conversation?.title ?? t('headings.emptyConversation');

  return (
    <div className={styles.app}>
      <ConversationSidebar
        activeConversationId={chat.conversationId}
        conversations={conversations.conversations}
        error={conversations.error ? t('captions.conversationsLoadError') : null}
        isLoading={conversations.isLoading}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        onNewConversation={handleNewConversation}
        onReload={conversations.reload}
        onSelect={handleSelect}
      />

      <div className={styles.main}>
        <header className={styles.mobileHeader}>
          <button
            aria-controls="conversation-sidebar"
            aria-expanded={isSidebarOpen}
            className={styles.menuButton}
            onClick={() => setIsSidebarOpen(true)}
            type="button"
          >
            <span aria-hidden="true">☰</span>
            <span className={styles.srOnly}>{t('labels.openSidebar')}</span>
          </button>

          <h1 className={styles.mobileTitle}>{mobileTitle}</h1>
        </header>

        <div className={styles.panel}>
          {chat.isLoading && <p className={styles.status}>{t('labels.loadingConversation')}</p>}

          {!chat.isLoading && chat.error && (
            <div className={styles.panelError}>
              <ErrorBanner message={t('captions.conversationLoadError')} onRetry={chat.reloadConversation} />
            </div>
          )}

          {!chat.isLoading && !chat.error && !chat.conversation && !chat.pendingQuery && <EmptyConversationState />}

          {!chat.isLoading && !chat.error && (chat.conversation || chat.pendingQuery) && (
            <MessageList
              isSending={chat.isSending}
              messages={chat.conversation?.messages ?? []}
              pendingQuery={chat.pendingQuery}
            />
          )}
        </div>

        <MessageComposer
          disabled={chat.isSending}
          error={chat.sendError ? t('captions.composerSendError') : null}
          onChange={chat.setDraft}
          onClearError={chat.clearSendError}
          onSubmit={chat.sendMessage}
          value={chat.draft}
        />
      </div>
    </div>
  );
};

ConversationContainer.displayName = 'ConversationContainer';

export default ConversationContainer;
