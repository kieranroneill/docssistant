// enums
import { ErrorCodeEnum } from '@/platform/application/enums';

export default abstract class BaseError extends Error {
  // private
  private readonly __isDSError = true;
  // public
  public readonly code: ErrorCodeEnum;
  public readonly displayName: string;
  public message: string;

  public constructor(message: string) {
    super(message.toLowerCase());
  }

  public isDSError(): boolean {
    return this.__isDSError;
  }
}
