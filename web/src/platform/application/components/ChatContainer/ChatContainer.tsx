import { StickToBottom } from 'use-stick-to-bottom';

// components
import { Content, ScrollAnchor } from './components';

// types
import type { Component, Props } from './types';

// utilities
import cn from '@/platform/application/utilities/cn';

const ChatContainer: Component<Props> = ({ children, className, ...props }) => {
  return (
    <StickToBottom
      className={cn('flex overflow-y-auto', className)}
      resize="smooth"
      initial="instant"
      role="log"
      {...props}
    >
      {children}
    </StickToBottom>
  );
};

ChatContainer.Content = Content;
ChatContainer.ScrollAnchor = ScrollAnchor;

export default ChatContainer;
