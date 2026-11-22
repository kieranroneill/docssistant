interface Props {
  disabled?: boolean;
  error?: string | null;
  onChange: (value: string) => void;
  onClearError?: () => void;
  onSubmit: () => void;
  value: string;
}

export default Props;
