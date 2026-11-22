import type { HTMLProps, ReactNode } from 'react';

interface ActionsProps extends HTMLProps<HTMLDivElement> {
  children: ReactNode;
  className?: string;
}

export default ActionsProps;
