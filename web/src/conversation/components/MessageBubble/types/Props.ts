// types
import type { ConversationSourceResponse } from '@/conversation/types';

interface Props {
  content: string;
  model?: string | null;
  role: string;
  sources?: ConversationSourceResponse[];
}

export default Props;
