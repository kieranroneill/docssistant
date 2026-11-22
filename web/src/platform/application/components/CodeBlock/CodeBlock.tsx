// components
import { Code, Group } from './components';

// types
import type { Component, Props } from './types';

// utilities
import cn from '@/platform/application/utilities/cn';

const CodeBlock: Component<Props> = ({ children, className, ...props }) => {
  return (
    <div
      className={cn(
        'not-prose flex w-full flex-col overflow-clip border',
        'border-border bg-card text-card-foreground rounded-xl',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

CodeBlock.Code = Code;
CodeBlock.Group = Group;

export default CodeBlock;
