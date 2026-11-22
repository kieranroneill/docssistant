import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

// errors
import { ChatUserCancelledError } from '@/conversation/errors';

// services
import ConversationsService from '@/conversation/services/ConversationsService';

// types
import type { BaseError } from '@/platform/defaults/errors';
import type { ConversationWithMessagesResponse } from '@/conversation/types';
import type { UseChatOptions, UseChatState } from './types';

/**
 * Manages the active conversation: loading an existing conversation's messages, and sending new
 * queries to start or continue a conversation.
 * @param {UseChatOptions} options - The logger and a callback fired after a message is sent successfully.
 * @returns {UseChatState} The active conversation and its loading, sending and error state.
 */
export default function useChat({ logger, onSent }: UseChatOptions): UseChatState {
  // memos
  const service = useMemo<ConversationsService>(() => new ConversationsService({ logger }), [logger]);
  // refs
  const loadAbortControllerRef = useRef<AbortController | null>(null);
  const sendAbortControllerRef = useRef<AbortController | null>(null);
  const skipNextLoadRef = useRef<boolean>(false);
  // states
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [conversation, setConversation] = useState<ConversationWithMessagesResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<BaseError | null>(null);
  const [draft, setDraft] = useState<string>('');
  const [isSending, setIsSending] = useState<boolean>(false);
  const [pendingQuery, setPendingQuery] = useState<string | null>(null);
  const [sendError, setSendError] = useState<BaseError | null>(null);
  // callbacks
  const loadConversation = useCallback(
    async (id: string) => {
      loadAbortControllerRef.current?.abort();

      const controller = new AbortController();

      loadAbortControllerRef.current = controller;

      setIsLoading(true);
      setError(null);

      try {
        const response = await service.getById(id, { signal: controller.signal });

        setConversation(response);
        setIsLoading(false);
      } catch (_error) {
        if (_error instanceof ChatUserCancelledError) {
          return;
        }

        logger.error('useChat#loadConversation:', _error);

        setError(_error as BaseError);
        setIsLoading(false);
      }
    },
    [logger, service]
  );
  const selectConversation = useCallback((id: string | null) => {
    sendAbortControllerRef.current?.abort();

    setIsSending(false);
    setPendingQuery(null);
    setSendError(null);
    setDraft('');
    setConversation(null);
    setError(null);
    setConversationId(id);
  }, []);
  const sendMessage = useCallback(() => {
    const query = draft.trim();

    if (!query || isSending) {
      return;
    }

    sendAbortControllerRef.current?.abort();

    const controller = new AbortController();

    sendAbortControllerRef.current = controller;

    const targetConversationId = conversationId;

    setIsSending(true);
    setPendingQuery(query);
    setSendError(null);
    setDraft('');

    (async () => {
      try {
        const response = targetConversationId
          ? await service.sendMessage(targetConversationId, query, { signal: controller.signal })
          : await service.startConversation(query, { signal: controller.signal });

        setConversation(response);
        setPendingQuery(null);
        setIsSending(false);

        if (!targetConversationId) {
          skipNextLoadRef.current = true;
          setConversationId(response.id);
        }

        onSent?.();
      } catch (_error) {
        if (_error instanceof ChatUserCancelledError) {
          return;
        }

        logger.error('useChat#sendMessage:', _error);

        setSendError(_error as BaseError);
        setPendingQuery(null);
        setIsSending(false);
        setDraft(query);
      }
    })();
  }, [conversationId, draft, isSending, logger, onSent, service]);
  // effects
  useEffect(() => {
    if (!conversationId) {
      setIsLoading(false);

      return;
    }

    if (skipNextLoadRef.current) {
      skipNextLoadRef.current = false;

      return;
    }

    loadConversation(conversationId);
  }, [conversationId, loadConversation]);
  useEffect(
    () => () => {
      loadAbortControllerRef.current?.abort();
      sendAbortControllerRef.current?.abort();
    },
    []
  );

  return {
    clearSendError: () => setSendError(null),
    conversation,
    conversationId,
    draft,
    error,
    isLoading,
    isSending,
    pendingQuery,
    reloadConversation: () => conversationId && loadConversation(conversationId),
    selectConversation,
    sendError,
    sendMessage,
    setDraft,
  };
}
