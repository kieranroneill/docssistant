import type { FC } from 'react';

// types
import type CodeProps from './CodeProps';
import type GroupProps from './GroupProps';

interface Component<Props> extends FC<Props> {
  Code: FC<CodeProps>;
  Group: FC<GroupProps>;
}

export default Component;
