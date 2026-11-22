import * as React from 'react';
import * as AvatarPrimitive from '@radix-ui/react-avatar';

// types
import type { FallbackProps as Props } from '../types';

// utilities
import cn from '@/platform/application/utilities/cn';

const Fallback = React.forwardRef<React.ElementRef<typeof AvatarPrimitive.Fallback>, Props>(
  ({ className, ...props }, ref) => (
    <AvatarPrimitive.Fallback
      ref={ref}
      className={cn('flex h-full w-full items-center justify-center rounded-full bg-muted', className)}
      {...props}
    />
  )
);

Fallback.displayName = 'AvatarFallback';

export default Fallback;
