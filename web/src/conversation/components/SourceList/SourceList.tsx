import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

// components
import SourceLink from '../SourceLink';

// styles
import styles from './SourceList.module.css';

// types
import type { Props } from './types';

const SourceList: FC<Props> = ({ sources }) => {
  const { t } = useTranslation();

  if (sources.length <= 0) {
    return null;
  }

  return (
    <div className={styles.sourceList}>
      <p className={styles.heading}>{t('headings.sources')}</p>

      <ul className={styles.items}>
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
