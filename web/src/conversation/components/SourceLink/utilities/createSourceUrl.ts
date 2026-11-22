// types
import type { ConversationSourceResponse } from '@/conversation/types';

/**
 * Creates the URL that opens a source's document. Paged documents, such as PDFs, carry a fragment that tells the
 * browser's viewer which page to open at. Documents without pages, such as text and markdown, open at the top.
 * @param {ConversationSourceResponse} source - The source to create the URL for.
 * @returns {string} The URL that opens the source's document.
 */
export default function createSourceUrl(source: ConversationSourceResponse): string {
  const url = `/api/documents/${source.documentId}`;

  return source.pageNumber === null ? url : `${url}#page=${source.pageNumber}`;
}
