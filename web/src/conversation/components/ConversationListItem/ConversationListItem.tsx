import { type FC } from 'react';

// styles
import styles from './ConversationListItem.module.css';

// types
import type { Props } from './types';

// utilities
import { formatRelativeDate } from './utilities';

const ConversationListItem: FC<Props> = ({ conversation, isActive, onSelect }) => (
  <button
    aria-current={isActive ? 'true' : undefined}
    className={`${styles.item} ${isActive ? styles.active : ''}`}
    onClick={() => onSelect(conversation.id)}
    type="button"
  >
    <span className={styles.title}>{conversation.title}</span>
    <span className={styles.date}>{formatRelativeDate(conversation.updatedAt)}</span>
  </button>
);

ConversationListItem.displayName = 'ConversationListItem';

export default ConversationListItem;
