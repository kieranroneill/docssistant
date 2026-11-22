interface ConversationSourceResponse {
  chunkIndex: number;
  documentId: string;
  id: string;
  pageNumber: number | null;
  reference: number;
  source: string;
}

export default ConversationSourceResponse;
