// types
import type ConversationSourceResponse from './ConversationSourceResponse';
import type UsageResponse from './UsageResponse';

interface ConversationMessageResponse {
  content: string;
  conversationId: string;
  createdAt: string;
  id: string;
  model: string | null;
  role: string;
  sequenceNumber: number;
  sources: ConversationSourceResponse[];
  usage: UsageResponse | null;
}

export default ConversationMessageResponse;
