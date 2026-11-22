import { type FC } from 'react';
import { ChevronDown } from 'lucide-react';
import { useStickToBottomContext } from 'use-stick-to-bottom';

// components
import Button from '@/platform/application/components/Button';

// types
import type { Props } from './types';

// utilities
import cn from '@/platform/application/utilities/cn';

const ScrollButton: FC<Props> = ({ className, variant = 'outline', size = 'sm', ...props }) => {
  const { isAtBottom, scrollToBottom } = useStickToBottomContext();

  return (
    <Button
      variant={variant}
      size={size}
      className={cn(
        'h-10 w-10 rounded-full transition-all duration-150 ease-out',
        !isAtBottom ? 'translate-y-0 scale-100 opacity-100' : 'pointer-events-none translate-y-4 scale-95 opacity-0',
        className
      )}
      onClick={() => scrollToBottom()}
      {...props}
    >
      <ChevronDown className="h-5 w-5" />
    </Button>
  );
};

ScrollButton.displayName = 'ScrollButton';

export default ScrollButton;
