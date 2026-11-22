import { type FC } from 'react';

// types
import type { Props } from './types';

// utilities
import { formatRelativeDate } from './utilities';

const ConversationListItem: FC<Props> = ({ conversation, isActive, onSelect }) => (
  <button
    aria-current={isActive ? 'true' : undefined}
    className={`flex w-full flex-col items-start gap-0.5 rounded-md px-3 py-2 text-left hover:bg-accent ${
      isActive ? 'bg-accent font-semibold' : ''
    }`}
    onClick={() => onSelect(conversation.id)}
    type="button"
  >
    <span className="w-full truncate text-sm">{conversation.title}</span>
    <span className="text-xs text-muted-foreground">{formatRelativeDate(conversation.updatedAt)}</span>
  </button>
);

ConversationListItem.displayName = 'ConversationListItem';

export default ConversationListItem;
