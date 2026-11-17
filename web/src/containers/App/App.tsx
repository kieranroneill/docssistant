import { type FC } from 'react';
import { I18nextProvider } from 'react-i18next';

// types
import type { Props } from './types';

const App: FC<Props> = ({ i18n }) => {
  return (
    <>
      <meta name="description" content={i18n.t('captions.longDescription')} />

      <I18nextProvider i18n={i18n}>
        <div>Hello humie!!</div>
      </I18nextProvider>
    </>
  );
};

App.displayName = 'App';

export default App;
