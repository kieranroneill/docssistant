enum ErrorCodeEnum {
  // chat
  ChatUserCancelledError = 2000,
  ConversationNotFoundError = 2004,
  // http
  FieldRequiredError = 4007,
  // internal
  InternalServerError = 5000,
  ParsingError = 5004,
  // documents
  DocumentPathDoesNotExistError = 7000,
}

export default ErrorCodeEnum;
