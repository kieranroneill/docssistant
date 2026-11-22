import * as React from 'react';
import * as AvatarPrimitive from '@radix-ui/react-avatar';

// types
import type { ImageProps as Props } from '../types';

// utilities
import cn from '@/platform/application/utilities/cn';

const Image = React.forwardRef<React.ElementRef<typeof AvatarPrimitive.Image>, Props>(
  ({ className, ...props }, ref) => (
    <AvatarPrimitive.Image ref={ref} className={cn('aspect-square h-full w-full', className)} {...props} />
  )
);

Image.displayName = 'AvatarImage';

export default Image;
