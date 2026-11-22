import type { HTMLProps } from 'react';

interface CodeProps extends HTMLProps<HTMLDivElement> {
  code: string;
  // kept for API compatibility with callers that still pass a detected language
  language?: string;
  className?: string;
}

export default CodeProps;
