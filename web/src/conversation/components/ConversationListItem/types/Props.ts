// types
import type { ConversationResponse } from '@/conversation/types';

interface Props {
  conversation: ConversationResponse;
  isActive: boolean;
  onSelect: (id: string) => void;
}

export default Props;
