import type { FC } from 'react';

// types
import type ContentProps from './ContentProps';
import type ProviderProps from './ProviderProps';
import type TriggerProps from './TriggerProps';

interface Component<Props> extends FC<Props> {
  Content: FC<ContentProps>;
  Provider: FC<ProviderProps>;
  Trigger: FC<TriggerProps>;
}

export default Component;
