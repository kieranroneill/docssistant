interface ValidationErrorBody {
  detail: {
    loc: (string | number)[];
    msg: string;
    type: string;
  }[];
}

export default ValidationErrorBody;
