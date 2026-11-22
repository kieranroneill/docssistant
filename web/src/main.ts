import I18next, { type i18n as I18n } from 'i18next';
import { createElement } from 'react';
import { initReactI18next } from 'react-i18next';
import { createRoot } from 'react-dom/client';

import '@/platform/styles/global.css';

// components
import App from '@/platform/application/containers/App';

// enums
import { LogLevelEnum } from '@/platform/logging/utilities/createLogger';

// translations
import { en } from '@/platform/translations';

// utilities
import createLogger from '@/platform/logging/utilities/createLogger';

export async function onDOMContentLoaded(): Promise<void> {
  const logger = createLogger((import.meta.env.VITE_LOG_LEVEL as LogLevelEnum) ?? LogLevelEnum.Error);
  const rootElement = document.getElementById('root');
  let i18n: I18n;

  if (!rootElement) {
    logger.error(`failed to find "root" element to render react app`);

    return;
  }

  i18n = I18next.use(initReactI18next);

  await i18n.init({
    fallbackLng: 'en',
    debug: true,
    interpolation: {
      escapeValue: false,
    },
    resources: {
      en: {
        translation: en,
      },
    },
  });

  createRoot(rootElement).render(
    createElement(App, {
      i18n,
      logger,
    })
  );
}

window.addEventListener('DOMContentLoaded', onDOMContentLoaded);
