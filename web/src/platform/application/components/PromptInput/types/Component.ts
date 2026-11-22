import type { FC } from 'react';

// types
import type ActionProps from './ActionProps';
import type ActionsProps from './ActionsProps';
import type TextareaProps from './TextareaProps';

interface Component<Props> extends FC<Props> {
  Action: FC<ActionProps>;
  Actions: FC<ActionsProps>;
  Textarea: FC<TextareaProps>;
}

export default Component;
