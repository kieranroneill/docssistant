// types
import type { BaseError } from '@/platform/defaults/errors';
import type { ConversationResponse } from '@/conversation/types';

interface UseConversationsState {
  conversations: ConversationResponse[];
  error: BaseError | null;
  isLoading: boolean;
  reload: () => void;
}

export default UseConversationsState;
