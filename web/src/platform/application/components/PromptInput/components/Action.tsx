// components
import Tooltip from '@/platform/application/components/Tooltip';

// hooks
import { usePromptInput } from '../hooks';

// types
import type { ActionProps as Props } from '../types';

function Action({ tooltip, children, className, side = 'top', ...props }: Props) {
  const { disabled } = usePromptInput();

  return (
    <Tooltip {...props}>
      <Tooltip.Trigger asChild disabled={disabled} onClick={(event) => event.stopPropagation()}>
        {children}
      </Tooltip.Trigger>
      <Tooltip.Content side={side} className={className}>
        {tooltip}
      </Tooltip.Content>
    </Tooltip>
  );
}

export default Action;
