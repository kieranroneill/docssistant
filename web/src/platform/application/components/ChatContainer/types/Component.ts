import type { FC } from 'react';

// types
import type ContentProps from './ContentProps';
import type ScrollAnchorProps from './ScrollAnchorProps';

interface Component<Props> extends FC<Props> {
  Content: FC<ContentProps>;
  ScrollAnchor: FC<ScrollAnchorProps>;
}

export default Component;
