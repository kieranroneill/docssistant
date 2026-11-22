import type { ComponentProps } from 'react';
import type Textarea from '@/platform/application/components/Textarea';

interface TextareaProps extends ComponentProps<typeof Textarea> {
  disableAutosize?: boolean;
}

export default TextareaProps;
