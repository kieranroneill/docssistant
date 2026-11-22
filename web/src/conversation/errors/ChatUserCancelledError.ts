// enums
import { ErrorCodeEnum } from '@/platform/application/enums';

// errors
import BaseError from '@/platform/defaults/errors/BaseError';

export default class ChatUserCancelledError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.ChatUserCancelledError;
  public readonly displayName: string = 'ChatUserCancelledError';
}
