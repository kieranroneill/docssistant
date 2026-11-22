import type { HTMLAttributes, RefObject } from 'react';

interface ScrollAnchorProps extends HTMLAttributes<HTMLDivElement> {
  className?: string;
  ref?: RefObject<HTMLDivElement>;
}

export default ScrollAnchorProps;
