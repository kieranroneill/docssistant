import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';

// types
import type { Props } from './types';

// utilities
import { buttonVariants } from './utilities';
import cn from '@/platform/application/utilities/cn';

const Button = React.forwardRef<HTMLButtonElement, Props>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';

    return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />;
  }
);

Button.displayName = 'Button';

export default Button;
