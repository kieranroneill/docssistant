// types
import type { ActionsProps as Props } from '../types';

// utilities
import cn from '@/platform/application/utilities/cn';

function Actions({ children, className, ...props }: Props) {
  return (
    <div className={cn('flex items-center gap-2', className)} {...props}>
      {children}
    </div>
  );
}

export default Actions;
