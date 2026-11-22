import type { ComponentProps, ReactNode } from 'react';

interface Props extends ComponentProps<'div'> {
  isLoading?: boolean;
  value?: string;
  onValueChange?: (value: string) => void;
  maxHeight?: number | string;
  onSubmit?: () => void;
  children: ReactNode;
  className?: string;
  disabled?: boolean;
}

export default Props;
