// enums
import { ErrorCodeEnum } from '@/platform/application/enums';

// errors
import BaseError from '@/platform/defaults/errors/BaseError';

export default class ConversationNotFoundError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.ConversationNotFoundError;
  public readonly displayName: string = 'ConversationNotFoundError';
}
