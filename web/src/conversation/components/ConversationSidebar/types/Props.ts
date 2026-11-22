// types
import type { ConversationResponse } from '@/conversation/types';
import type { Logger } from '@/platform/logging/utilities/createLogger';

interface Props {
  activeConversationId: string | null;
  conversations: ConversationResponse[];
  error?: string | null;
  isLoading: boolean;
  isOpen: boolean;
  logger: Logger;
  onClose: () => void;
  onNewConversation: () => void;
  onReload: () => void;
  onSelect: (id: string) => void;
}

export default Props;
