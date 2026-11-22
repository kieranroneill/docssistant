// types
import type { ScrollAnchorProps as Props } from '../types';

// utilities
import cn from '@/platform/application/utilities/cn';

function ScrollAnchor({ className, ...props }: Props) {
  return <div className={cn('h-px w-full shrink-0 scroll-mt-4', className)} aria-hidden="true" {...props} />;
}

export default ScrollAnchor;
