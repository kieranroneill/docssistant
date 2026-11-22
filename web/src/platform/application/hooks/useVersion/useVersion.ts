import { useEffect, useMemo, useState } from 'react';

// services
import VersionsService from '@/platform/application/services/VersionsService';

// types
import type { Logger } from '@/platform/logging/utilities/createLogger';
import type { VersionResponse } from '@/platform/application/types';
import type { UseVersionState } from './types';

/**
 * Fetches information about the API, including the chat model currently in use.
 * Fails silently: this is decorative, so a failed fetch just leaves `version` null.
 * @param {Logger} logger - A logger instance.
 * @returns {UseVersionState} The version information and its loading state.
 */
export default function useVersion(logger: Logger): UseVersionState {
  // memos
  const service = useMemo<VersionsService>(() => new VersionsService({ logger }), [logger]);
  // states
  const [version, setVersion] = useState<VersionResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  // effects
  useEffect(() => {
    const controller = new AbortController();

    (async () => {
      try {
        setVersion(await service.get({ signal: controller.signal }));
      } catch (error) {
        if (!controller.signal.aborted) {
          logger.warn('useVersion:', error);
        }
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      }
    })();

    return () => controller.abort();
  }, [logger, service]);

  return { isLoading, version };
}
