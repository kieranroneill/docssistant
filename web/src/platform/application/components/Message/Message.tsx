// components
import { Action, Actions, Avatar, Content } from './components';

// types
import type { Component, Props } from './types';

// utilities
import cn from '@/platform/application/utilities/cn';

const Message: Component<Props> = ({ children, className, ...props }) => (
  <div className={cn('flex gap-3', className)} {...props}>
    {children}
  </div>
);

Message.Action = Action;
Message.Actions = Actions;
Message.Avatar = Avatar;
Message.Content = Content;

export default Message;
