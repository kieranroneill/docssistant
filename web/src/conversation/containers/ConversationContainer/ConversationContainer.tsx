import { type FC, useCallback, useState } from 'react';
import { useTranslation } from 'react-i18next';

// components
import ConversationHeader from '@/conversation/components/ConversationHeader';
import ConversationSidebar from '@/conversation/components/ConversationSidebar';
import EmptyConversationState from '@/conversation/components/EmptyConversationState';
import ErrorBanner from '@/conversation/components/ErrorBanner';
import MessageComposer from '@/conversation/components/MessageComposer';
import MessageList from '@/conversation/components/MessageList';

// hooks
import useChat from '@/conversation/hooks/useChat';
import useConversations from '@/conversation/hooks/useConversations';

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
  const title = chat.conversation?.title ?? t('headings.emptyConversation');

  return (
    <div className="flex h-full overflow-hidden">
      <ConversationSidebar
        activeConversationId={chat.conversationId}
        conversations={conversations.conversations}
        error={conversations.error ? t('captions.conversationsLoadError') : null}
        isLoading={conversations.isLoading}
        isOpen={isSidebarOpen}
        logger={logger}
        onClose={() => setIsSidebarOpen(false)}
        onNewConversation={handleNewConversation}
        onReload={conversations.reload}
        onSelect={handleSelect}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <ConversationHeader isSidebarOpen={isSidebarOpen} onOpenSidebar={() => setIsSidebarOpen(true)} title={title} />

        <div className="flex min-h-0 flex-1 flex-col">
          {chat.isLoading && (
            <p className="flex flex-1 items-center justify-center text-muted-foreground">
              {t('labels.loadingConversation')}
            </p>
          )}

          {!chat.isLoading && chat.error && (
            <div className="p-4">
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
          logger={logger}
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
