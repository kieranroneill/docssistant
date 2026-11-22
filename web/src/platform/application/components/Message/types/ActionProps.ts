import type { ComponentProps, ReactNode } from 'react';
import type Tooltip from '@/platform/application/components/Tooltip';

interface ActionProps extends ComponentProps<typeof Tooltip> {
  className?: string;
  tooltip: ReactNode;
  children: ReactNode;
  side?: 'top' | 'bottom' | 'left' | 'right';
}

export default ActionProps;
