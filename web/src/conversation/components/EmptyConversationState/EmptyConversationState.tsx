import { type FC } from 'react';
import { useTranslation } from 'react-i18next';

const EmptyConversationState: FC = () => {
  const { t } = useTranslation();

  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-1 p-6 text-center text-muted-foreground">
      <p className="text-base font-medium text-foreground">{t('headings.emptyConversation')}</p>
      <p className="max-w-[40ch]">{t('captions.emptyConversation')}</p>
    </div>
  );
};

EmptyConversationState.displayName = 'EmptyConversationState';

export default EmptyConversationState;
