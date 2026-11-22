import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

// types
import type { Props } from './types';

// utilities
import { createSourceUrl, formatSourceLabel } from './utilities';

const SourceLink: FC<Props> = ({ source }) => {
  const { t } = useTranslation();
  // memos
  const label = formatSourceLabel(source);

  return (
    <a
      aria-label={t('labels.openSource', { source: label })}
      className="inline-flex items-baseline gap-1 rounded-md bg-muted px-2 py-1 text-xs text-muted-foreground no-underline break-words hover:text-primary focus-visible:text-primary"
      href={createSourceUrl(source)}
      rel="noreferrer"
      target="_blank"
    >
      <span className="font-semibold text-foreground">[{source.reference}]</span> {label}
    </a>
  );
};

SourceLink.displayName = 'SourceLink';

export default SourceLink;
