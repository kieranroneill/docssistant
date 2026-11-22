interface DSErrorBody {
  detail: {
    __isDSError: true;
    code: number;
    displayName: string;
    message: string;
  };
}

export default DSErrorBody;
