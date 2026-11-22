// enums
import { ErrorCodeEnum } from '@/platform/application/enums';

// errors
import BaseError from '@/platform/defaults/errors/BaseError';

export default class ParsingError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.ParsingError;
  public readonly displayName: string = 'ParsingError';
}
