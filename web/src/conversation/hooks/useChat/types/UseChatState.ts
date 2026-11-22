// types
import type { BaseError } from '@/platform/defaults/errors';
import type { ConversationWithMessagesResponse } from '@/conversation/types';

interface UseChatState {
  clearSendError: () => void;
  conversation: ConversationWithMessagesResponse | null;
  conversationId: string | null;
  draft: string;
  error: BaseError | null;
  isLoading: boolean;
  isSending: boolean;
  pendingQuery: string | null;
  reloadConversation: () => void;
  selectConversation: (id: string | null) => void;
  sendError: BaseError | null;
  sendMessage: () => void;
  setDraft: (value: string) => void;
}

export default UseChatState;
