// types
import type { GroupProps as Props } from '../types';

// utilities
import cn from '@/platform/application/utilities/cn';

function Group({ children, className, ...props }: Props) {
  return (
    <div className={cn('flex items-center justify-between', className)} {...props}>
      {children}
    </div>
  );
}

export default Group;
