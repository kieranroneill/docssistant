import * as React from 'react';
import * as AvatarPrimitive from '@radix-ui/react-avatar';

// components
import { Fallback, Image } from './components';

// types
import type { Component, Props } from './types';

// utilities
import cn from '@/platform/application/utilities/cn';

const Avatar = React.forwardRef<React.ElementRef<typeof AvatarPrimitive.Root>, Props>(
  ({ className, ...props }, ref) => (
    <AvatarPrimitive.Root
      ref={ref}
      className={cn('relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full', className)}
      {...props}
    />
  )
) as unknown as Component<Props>;

Avatar.displayName = 'Avatar';
Avatar.Fallback = Fallback;
Avatar.Image = Image;

export default Avatar;
