// types
import type { Logger } from '@/platform/logging/utilities/createLogger';

interface Props {
  disabled?: boolean;
  error?: string | null;
  logger: Logger;
  onChange: (value: string) => void;
  onClearError?: () => void;
  onSubmit: () => void;
  value: string;
}

export default Props;
