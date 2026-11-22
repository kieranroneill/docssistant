// types
import type { ConversationMessageResponse } from '@/conversation/types';

interface Props {
  isSending: boolean;
  messages: ConversationMessageResponse[];
  pendingQuery: string | null;
}

export default Props;
