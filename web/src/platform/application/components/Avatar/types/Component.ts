import type { FC } from 'react';

// types
import type FallbackProps from './FallbackProps';
import type ImageProps from './ImageProps';

interface Component<Props> extends FC<Props> {
  Fallback: FC<FallbackProps>;
  Image: FC<ImageProps>;
}

export default Component;
