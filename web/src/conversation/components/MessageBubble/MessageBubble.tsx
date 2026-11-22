import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

// components
import SourceList from '../SourceList';

// enums
import { MessageRoleEnum } from '@/conversation/enums';

// styles
import styles from './MessageBubble.module.css';

// types
import type { Props } from './types';

const MessageBubble: FC<Props> = ({ content, model, role, sources = [] }) => {
  const { t } = useTranslation();
  const isUser = role === MessageRoleEnum.User;
  const senderLabel = isUser ? t('labels.you') : t('labels.assistant');

  return (
    <div className={`${styles.row} ${isUser ? styles.user : styles.assistant}`}>
      <div>
        <p className={styles.bubble}>
          <span className={styles.srOnly}>{senderLabel}: </span>
          {content}
        </p>

        {!isUser && sources.length > 0 && <SourceList sources={sources} />}

        {!isUser && model && <p className={styles.meta}>{model}</p>}
      </div>
    </div>
  );
};

MessageBubble.displayName = 'MessageBubble';

export default MessageBubble;
