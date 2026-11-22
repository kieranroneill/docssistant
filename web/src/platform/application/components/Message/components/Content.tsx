// components
import Markdown from '@/platform/application/components/Markdown';

// types
import type { ContentProps as Props } from '../types';

// utilities
import cn from '@/platform/application/utilities/cn';

function Content({ children, markdown = false, className, ...props }: Props) {
  const classNames = cn('rounded-lg p-2 text-foreground bg-secondary prose break-words whitespace-normal', className);

  return markdown ? (
    <Markdown className={classNames} {...props}>
      {children as string}
    </Markdown>
  ) : (
    <div className={classNames} {...props}>
      {children}
    </div>
  );
}

export default Content;
