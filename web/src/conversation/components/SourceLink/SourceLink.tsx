import { type FC } from 'react';

// types
import type { Props } from './types';

// utilities
import { formatSourceLabel } from './utilities';

const classNames =
  'inline-flex items-baseline gap-1 rounded-md bg-muted px-2 py-1 text-xs text-muted-foreground no-underline break-words';

const SourceLink: FC<Props> = ({ source }) => {
  const label = formatSourceLabel(source);
  const isUrl = /^https?:\/\//i.test(source.source);
  const content = (
    <>
      <span className="font-semibold text-foreground">[{source.reference}]</span> {label}
    </>
  );

  if (isUrl) {
    return (
      <a
        className={`${classNames} hover:text-primary focus-visible:text-primary`}
        href={source.source}
        rel="noreferrer"
        target="_blank"
      >
        {content}
      </a>
    );
  }

  return <span className={classNames}>{content}</span>;
};

SourceLink.displayName = 'SourceLink';

export default SourceLink;
