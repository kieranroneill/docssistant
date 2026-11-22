import { type FC } from 'react';
import { I18nextProvider } from 'react-i18next';

// containers
import ConversationContainer from '@/conversation/containers/ConversationContainer';

// types
import type { Props } from './types';

const App: FC<Props> = ({ i18n, logger }) => {
  return (
    <>
      <meta name="description" content={i18n.t('captions.longDescription')} />

      <I18nextProvider i18n={i18n}>
        <ConversationContainer logger={logger} />
      </I18nextProvider>
    </>
  );
};

App.displayName = 'App';

export default App;
