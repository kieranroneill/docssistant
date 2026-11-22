import { type FC } from 'react';

// styles
import styles from './SourceLink.module.css';

// types
import type { Props } from './types';

// utilities
import { formatSourceLabel } from './utilities';

const SourceLink: FC<Props> = ({ source }) => {
  const label = formatSourceLabel(source);
  const isUrl = /^https?:\/\//i.test(source.source);
  const content = (
    <>
      <span className={styles.reference}>[{source.reference}]</span> {label}
    </>
  );

  if (isUrl) {
    return (
      <a className={styles.sourceLink} href={source.source} rel="noreferrer" target="_blank">
        {content}
      </a>
    );
  }

  return <span className={styles.sourceLink}>{content}</span>;
};

SourceLink.displayName = 'SourceLink';

export default SourceLink;
