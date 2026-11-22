// services
import BaseAPIService from '@/platform/defaults/services/BaseAPIService';

// types
import type { RequestOptions } from '@/platform/defaults/services/BaseAPIService';
import type { VersionResponse } from '@/platform/application/types';

export default class VersionsService extends BaseAPIService {
  /**
   * Gets information about the API, including the chat model currently in use.
   * @param {RequestOptions} options - Options for the request.
   * @returns {Promise<VersionResponse>} A promise that resolves to the version information.
   */
  public async get(options: RequestOptions = {}): Promise<VersionResponse> {
    let response: Response;

    try {
      response = await fetch('/api/versions', { method: 'GET', signal: options.signal });
    } catch (error) {
      throw this._parseError(error as Error, { logPrefix: 'VersionsService#get' });
    }

    if (!response.ok) {
      throw this._parseError(new Error(`request failed with status ${response.status}`), {
        logPrefix: 'VersionsService#get',
      });
    }

    try {
      return (await response.json()) as VersionResponse;
    } catch (error) {
      throw this._parseError(error as Error, { logPrefix: 'VersionsService#get' });
    }
  }
}
