import type { i18n as I18n } from 'i18next';

// types
import type { Logger } from '@/platform/logging/utilities/createLogger';

interface Props {
  i18n: I18n;
  logger: Logger;
}

export default Props;
