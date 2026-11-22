// enums
import { ErrorCodeEnum } from '@/platform/application/enums';

// errors
import BaseError from '@/platform/defaults/errors/BaseError';

export default class ValidationError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.FieldRequiredError;
  public readonly displayName: string = 'ValidationError';
}
