import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

// components
import SourceList from '../SourceList';

// enums
import { MessageRoleEnum } from '@/conversation/enums';

// ui
import Message from '@/platform/application/components/Message';

// types
import type { Props } from './types';

const MessageBubble: FC<Props> = ({ content, model, role, sources = [] }) => {
  const { t } = useTranslation();
  const isUser = role === MessageRoleEnum.User;

  if (isUser) {
    return (
      <Message className="justify-end">
        <Message.Content>
          <span className="sr-only">{t('labels.you')}: </span>
          {content}
        </Message.Content>
      </Message>
    );
  }

  return (
    <Message className="justify-start">
      <Message.Avatar alt={t('labels.assistant')} delayMs={0} fallback="AI" src="" />

      <div className="flex min-w-0 flex-1 flex-col gap-2">
        <Message.Content className="bg-transparent p-0" markdown>
          {content}
        </Message.Content>

        {sources.length > 0 && <SourceList sources={sources} />}

        {model && <p className="text-xs text-muted-foreground">{model}</p>}
      </div>
    </Message>
  );
};

MessageBubble.displayName = 'MessageBubble';

export default MessageBubble;
