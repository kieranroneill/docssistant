// types
import type { CodeProps as Props } from '../types';

// utilities
import cn from '@/platform/application/utilities/cn';

// No syntax highlighter: shiki's language grammars would otherwise ship as 150+ extra
// build chunks for a document-QA app that only occasionally shows a code excerpt.
function Code({ code, className, ...props }: Props) {
  return (
    <div className={cn('w-full overflow-x-auto text-[13px] [&>pre]:px-4 [&>pre]:py-4', className)} {...props}>
      <pre>
        <code>{code}</code>
      </pre>
    </div>
  );
}

export default Code;
