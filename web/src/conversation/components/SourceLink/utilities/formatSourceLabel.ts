// types
import type { ConversationSourceResponse } from '@/conversation/types';

/**
 * Formats a source into a short, human-readable citation label.
 * @param {ConversationSourceResponse} source - The source to format.
 * @returns {string} The source's document location, with its page number appended when available.
 */
export default function formatSourceLabel(source: ConversationSourceResponse): string {
  return source.pageNumber === null ? source.source : `${source.source} · page ${source.pageNumber}`;
}
