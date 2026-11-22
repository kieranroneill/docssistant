// components
import Tooltip from '@/platform/application/components/Tooltip';

// types
import type { ActionProps as Props } from '../types';

function Action({ tooltip, children, className, side = 'top', ...props }: Props) {
  return (
    <Tooltip.Provider>
      <Tooltip {...props}>
        <Tooltip.Trigger asChild>{children}</Tooltip.Trigger>
        <Tooltip.Content side={side} className={className}>
          {tooltip}
        </Tooltip.Content>
      </Tooltip>
    </Tooltip.Provider>
  );
}

export default Action;
