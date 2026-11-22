// enums
import { ErrorCodeEnum } from '@/platform/application/enums';

// errors
import BaseError from '@/platform/defaults/errors/BaseError';

export default class InternalServerError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.InternalServerError;
  public readonly displayName: string = 'InternalServerError';
}
