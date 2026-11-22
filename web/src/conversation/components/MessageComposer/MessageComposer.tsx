import { type FC } from 'react';
import { useTranslation } from 'react-i18next';
import { ArrowUp, FileText } from 'lucide-react';

// components
import ErrorBanner from '../ErrorBanner';

// hooks
import useVersion from '@/platform/application/hooks/useVersion';

// ui
import Button from '@/platform/application/components/Button';
import PromptInput from '@/platform/application/components/PromptInput';

// types
import type { Props } from './types';

const MessageComposer: FC<Props> = ({ disabled = false, error, logger, onChange, onClearError, onSubmit, value }) => {
  const { t } = useTranslation();
  // hooks
  const { version } = useVersion(logger);
  // memos
  const canSubmit = !disabled && value.trim().length > 0;

  return (
    <div className="border-t border-border bg-background p-4">
      {error && (
        <div className="mb-2">
          <ErrorBanner message={error} onDismiss={onClearError} />
        </div>
      )}

      <PromptInput disabled={disabled} onSubmit={onSubmit} onValueChange={onChange} value={value}>
        <label className="sr-only" htmlFor="message-composer-input">
          {t('labels.composerPlaceholder')}
        </label>

        <PromptInput.Textarea id="message-composer-input" placeholder={t('labels.composerPlaceholder')} />

        <PromptInput.Actions className="w-full items-center justify-between pt-2">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-secondary px-3 py-1 text-xs font-medium text-secondary-foreground">
            <FileText className="h-3.5 w-3.5" />
            {t('labels.documentsMode')}
          </span>

          <div className="flex items-center gap-2">
            {version && <span className="hidden text-xs text-muted-foreground sm:inline">{version.models.chat}</span>}

            <PromptInput.Action tooltip={t('labels.send')}>
              <Button
                aria-label={t('labels.send')}
                className="rounded-full"
                disabled={!canSubmit}
                onClick={onSubmit}
                size="icon"
                type="button"
              >
                <ArrowUp className="h-4 w-4" />
              </Button>
            </PromptInput.Action>
          </div>
        </PromptInput.Actions>
      </PromptInput>
    </div>
  );
};

MessageComposer.displayName = 'MessageComposer';

export default MessageComposer;
