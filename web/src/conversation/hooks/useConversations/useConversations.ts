import { useCallback, useEffect, useMemo, useState } from 'react';

// errors
import { ChatUserCancelledError } from '@/conversation/errors';

// services
import ConversationsService from '@/conversation/services/ConversationsService';

// types
import type { BaseError } from '@/platform/defaults/errors';
import type { Logger } from '@/platform/logging/utilities/createLogger';
import type { ConversationResponse } from '@/conversation/types';
import type { UseConversationsState } from './types';

/**
 * Fetches and holds the list of conversations for the sidebar.
 * @param {Logger} logger - A logger instance.
 * @returns {UseConversationsState} The list of conversations and its loading/error state.
 */
export default function useConversations(logger: Logger): UseConversationsState {
  // memos
  const service = useMemo<ConversationsService>(() => new ConversationsService({ logger }), [logger]);
  // states
  const [conversations, setConversations] = useState<ConversationResponse[]>([]);
  const [error, setError] = useState<BaseError | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  // callbacks
  const load = useCallback(
    async (signal?: AbortSignal) => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await service.list({ signal });

        setConversations(
          [...response].sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
        );
        setIsLoading(false);
      } catch (_error) {
        if (_error instanceof ChatUserCancelledError) {
          return;
        }

        logger.error('useConversations#load:', _error);

        setError(_error as BaseError);
        setIsLoading(false);
      }
    },
    [logger, service]
  );
  // effects
  useEffect(() => {
    const controller = new AbortController();

    load(controller.signal);

    return () => controller.abort();
  }, [load]);

  return {
    conversations,
    error,
    isLoading,
    reload: () => load(),
  };
}
