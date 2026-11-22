import type { HTMLAttributes, ReactNode } from 'react';

interface ContentProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  className?: string;
}

export default ContentProps;
