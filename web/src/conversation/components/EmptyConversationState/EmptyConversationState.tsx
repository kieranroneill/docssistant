import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

// styles
import styles from './EmptyConversationState.module.css';

const EmptyConversationState: FC = () => {
  const { t } = useTranslation();

  return (
    <div className={styles.container}>
      <p className={styles.heading}>{t('headings.emptyConversation')}</p>
      <p className={styles.caption}>{t('captions.emptyConversation')}</p>
    </div>
  );
};

EmptyConversationState.displayName = 'EmptyConversationState';

export default EmptyConversationState;
