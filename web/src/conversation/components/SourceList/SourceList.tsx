import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

// components
import SourceLink from '../SourceLink';

// types
import type { Props } from './types';

const SourceList: FC<Props> = ({ sources }) => {
  const { t } = useTranslation();

  if (sources.length <= 0) {
    return null;
  }

  return (
    <div>
      <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
        {t('headings.sources')}
      </p>

      <ul className="m-0 flex list-none flex-wrap gap-1 p-0">
        {sources.map((source) => (
          <li key={source.id}>
            <SourceLink source={source} />
          </li>
        ))}
      </ul>
    </div>
  );
};

SourceList.displayName = 'SourceList';

export default SourceList;
