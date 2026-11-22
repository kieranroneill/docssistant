// types
import type { ConversationResponse } from '@/conversation/types';

interface Props {
  activeConversationId: string | null;
  conversations: ConversationResponse[];
  error?: string | null;
  isLoading: boolean;
  isOpen: boolean;
  onClose: () => void;
  onNewConversation: () => void;
  onReload: () => void;
  onSelect: (id: string) => void;
}

export default Props;
