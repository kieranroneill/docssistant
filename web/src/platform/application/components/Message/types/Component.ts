import type { FC } from 'react';

// types
import type ActionProps from './ActionProps';
import type ActionsProps from './ActionsProps';
import type AvatarProps from './AvatarProps';
import type ContentProps from './ContentProps';

interface Component<Props> extends FC<Props> {
  Action: FC<ActionProps>;
  Actions: FC<ActionsProps>;
  Avatar: FC<AvatarProps>;
  Content: FC<ContentProps>;
}

export default Component;
