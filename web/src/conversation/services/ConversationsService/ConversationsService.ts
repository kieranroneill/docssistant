// enums
import { ErrorCodeEnum } from '@/platform/application/enums';

// errors
import { ChatUserCancelledError, ConversationNotFoundError } from '@/conversation/errors';
import { InternalServerError, ValidationError } from '@/platform/http/errors';

// services
import BaseAPIService from '@/platform/defaults/services/BaseAPIService';

// types
import type { DSErrorBody, ValidationErrorBody } from './types';
import type { RequestOptions } from '@/platform/defaults/services/BaseAPIService';
import type { ChatRequest, ConversationResponse, ConversationWithMessagesResponse } from '@/conversation/types';

export default class ConversationsService extends BaseAPIService {
  // private
  private readonly _baseUrl: string = '/api/conversations';

  private async _handleErrorResponse(response: Response): Promise<never> {
    let body: unknown;

    try {
      body = await response.json();
    } catch (error) {
      throw this._parseError(error as Error, { logPrefix: 'ConversationsService#_handleErrorResponse' });
    }

    if (Array.isArray((body as ValidationErrorBody)?.detail)) {
      const message = (body as ValidationErrorBody).detail.map(({ msg }) => msg).join('; ');

      throw new ValidationError(message || 'validation failed');
    }

    const detail = (body as DSErrorBody)?.detail;

    if (detail?.__isDSError) {
      if (detail.code === ErrorCodeEnum.ConversationNotFoundError) {
        throw new ConversationNotFoundError(detail.message);
      }

      throw new InternalServerError(detail.message);
    }

    throw new InternalServerError(`request failed with status ${response.status}`);
  }

  private async _request<T>(path: string, init: RequestInit, { signal }: RequestOptions = {}): Promise<T> {
    let response: Response;

    try {
      response = await fetch(`${this._baseUrl}${path}`, {
        ...init,
        headers: {
          'Content-Type': 'application/json',
          ...init.headers,
        },
        signal,
      });
    } catch (error) {
      if (error instanceof DOMException && error.name === 'AbortError') {
        throw new ChatUserCancelledError(error.message || 'the request was cancelled');
      }

      throw this._parseError(error as Error, { logPrefix: 'ConversationsService#_request' });
    }

    if (!response.ok) {
      return this._handleErrorResponse(response);
    }

    try {
      return (await response.json()) as T;
    } catch (error) {
      throw this._parseError(error as Error, { logPrefix: 'ConversationsService#_request' });
    }
  }

  /**
   * Gets the list of conversations.
   * @param {RequestOptions} options - Options for the request.
   * @returns {Promise<ConversationResponse[]>} A promise that resolves to the list of conversations.
   */
  public async list(options?: RequestOptions): Promise<ConversationResponse[]> {
    return this._request<ConversationResponse[]>('', { method: 'GET' }, options);
  }

  /**
   * Gets a conversation, with its messages, by its ID.
   * @param {string} id - The ID of the conversation.
   * @param {RequestOptions} options - Options for the request.
   * @returns {Promise<ConversationWithMessagesResponse>} A promise that resolves to the conversation.
   */
  public async getById(id: string, options?: RequestOptions): Promise<ConversationWithMessagesResponse> {
    return this._request<ConversationWithMessagesResponse>(`/${id}`, { method: 'GET' }, options);
  }

  /**
   * Starts a new conversation with an initial query.
   * @param {string} query - The query to send.
   * @param {RequestOptions} options - Options for the request.
   * @returns {Promise<ConversationWithMessagesResponse>} A promise that resolves to the new conversation.
   */
  public async startConversation(query: string, options?: RequestOptions): Promise<ConversationWithMessagesResponse> {
    const payload: ChatRequest = { query };

    return this._request<ConversationWithMessagesResponse>(
      '/chat',
      { method: 'POST', body: JSON.stringify(payload) },
      options
    );
  }

  /**
   * Sends a new query to an existing conversation.
   * @param {string} conversationId - The ID of the conversation to send the query to.
   * @param {string} query - The query to send.
   * @param {RequestOptions} options - Options for the request.
   * @returns {Promise<ConversationWithMessagesResponse>} A promise that resolves to the updated conversation.
   */
  public async sendMessage(
    conversationId: string,
    query: string,
    options?: RequestOptions
  ): Promise<ConversationWithMessagesResponse> {
    const payload: ChatRequest = { query };

    return this._request<ConversationWithMessagesResponse>(
      `/${conversationId}/chat`,
      { method: 'POST', body: JSON.stringify(payload) },
      options
    );
  }
}
