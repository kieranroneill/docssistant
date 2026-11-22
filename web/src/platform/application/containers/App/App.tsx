import { type FC } from 'react';
import { I18nextProvider } from 'react-i18next';

// components
import ThemeProvider from '@/platform/application/components/ThemeProvider';

// containers
import ConversationContainer from '@/conversation/containers/ConversationContainer';

// types
import type { Props } from './types';

const App: FC<Props> = ({ i18n, logger }) => {
  return (
    <>
      <meta name="description" content={i18n.t('captions.longDescription')} />

      <I18nextProvider i18n={i18n}>
        <ThemeProvider>
          <ConversationContainer logger={logger} />
        </ThemeProvider>
      </I18nextProvider>
    </>
  );
};

App.displayName = 'App';

export default App;
