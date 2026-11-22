import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

// ui
import Loader from '@/platform/application/components/Loader';
import Message from '@/platform/application/components/Message';

const TypingIndicator: FC = () => {
  const { t } = useTranslation();

  return (
    <Message aria-live="polite" role="status">
      <Message.Avatar alt={t('labels.assistant')} delayMs={0} fallback="AI" src="" />

      <Message.Content className="bg-transparent p-0">
        <span className="sr-only">
          {t('labels.assistant')}: {t('labels.sending')}
        </span>
        <Loader aria-hidden="true" variant="typing" />
      </Message.Content>
    </Message>
  );
};

TypingIndicator.displayName = 'TypingIndicator';

export default TypingIndicator;
