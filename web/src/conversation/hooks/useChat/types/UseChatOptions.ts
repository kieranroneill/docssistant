// types
import type { Logger } from '@/platform/logging/utilities/createLogger';

interface UseChatOptions {
  logger: Logger;
  onSent?: () => void;
}

export default UseChatOptions;
