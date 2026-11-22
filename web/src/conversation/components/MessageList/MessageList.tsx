import { type FC } from 'react';

// components
import MessageBubble from '../MessageBubble';
import TypingIndicator from '../TypingIndicator';

// enums
import { MessageRoleEnum } from '@/conversation/enums';

// ui
import ChatContainer from '@/platform/application/components/ChatContainer';
import ScrollButton from '@/platform/application/components/ScrollButton';

// types
import type { Props } from './types';

const MessageList: FC<Props> = ({ isSending, messages, pendingQuery }) => {
  return (
    <div className="relative min-h-0 flex-1">
      <ChatContainer className="h-full flex-col">
        <ChatContainer.Content className="gap-4 p-4">
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
        </ChatContainer.Content>

        <ChatContainer.ScrollAnchor />

        <div className="absolute bottom-4 right-4">
          <ScrollButton />
        </div>
      </ChatContainer>
    </div>
  );
};

MessageList.displayName = 'MessageList';

export default MessageList;
