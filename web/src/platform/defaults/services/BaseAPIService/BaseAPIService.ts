// enums
import { LogLevelEnum } from '@/platform/logging/utilities/createLogger';

// errors
import { BaseError } from '@/platform/defaults/errors';
import { InternalServerError, ParsingError } from '@/platform/http/errors';

// types
import type { BaseAPIServiceOptions, ParseErrorOptions } from './types';
import type { Logger } from '@/platform/logging/utilities/createLogger';

// utilities
import createLogger from '@/platform/logging/utilities/createLogger';

export default abstract class BaseAPIService {
  // protected
  protected _logger: Logger;

  public constructor({ logger }: BaseAPIServiceOptions = {}) {
    this._logger = logger ?? createLogger((process.env.NEXT_PUBLIC_LOG_LEVEL as LogLevelEnum) ?? LogLevelEnum.Error);
  }

  protected _parseError(error: Error, { logPrefix }: ParseErrorOptions): BaseError {
    if (error instanceof BaseError) {
      return error;
    }

    this._logger.error(`${logPrefix}:`, error);

    if (error instanceof TypeError || error instanceof SyntaxError) {
      return new ParsingError(`failed to parse response`);
    }

    return new InternalServerError(error.message);
  }
}
