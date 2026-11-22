import { StickToBottom } from 'use-stick-to-bottom';

// types
import type { ContentProps as Props } from '../types';

// utilities
import cn from '@/platform/application/utilities/cn';

function Content({ children, className, ...props }: Props) {
  return (
    <StickToBottom.Content className={cn('flex w-full flex-col', className)} {...props}>
      {children}
    </StickToBottom.Content>
  );
}

export default Content;
