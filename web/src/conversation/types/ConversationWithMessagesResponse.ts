// types
import type ConversationMessageResponse from './ConversationMessageResponse';
import type ConversationResponse from './ConversationResponse';

interface ConversationWithMessagesResponse extends ConversationResponse {
  messages: ConversationMessageResponse[];
}

export default ConversationWithMessagesResponse;
