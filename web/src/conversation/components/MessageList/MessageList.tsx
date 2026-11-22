import { type FC, useEffect, useRef } from 'react';

// components
import MessageBubble from '../MessageBubble';
import TypingIndicator from '../TypingIndicator';

// enums
import { MessageRoleEnum } from '@/conversation/enums';

// styles
import styles from './MessageList.module.css';

// types
import type { Props } from './types';

const MessageList: FC<Props> = ({ isSending, messages, pendingQuery }) => {
  // refs
  const bottomRef = useRef<HTMLDivElement | null>(null);
  // effects
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ block: 'end' });
  }, [messages.length, pendingQuery, isSending]);

  return (
    <div className={styles.list}>
      {messages.map((message) => (
        <MessageBubble
          content={message.content}
          key={message.id}
          model={message.model}
          role={message.role}
          sources={message.sources}
        />
      ))}

      {pendingQuery && <MessageBubble content={pendingQuery} role={MessageRoleEnum.User} />}

      {isSending && <TypingIndicator />}

      <div ref={bottomRef} />
    </div>
  );
};

MessageList.displayName = 'MessageList';

export default MessageList;
