import type { HTMLProps, ReactNode } from 'react';
import type { Props as MarkdownProps } from '@/platform/application/components/Markdown';

interface ContentProps extends Omit<MarkdownProps, 'children'>, HTMLProps<HTMLDivElement> {
  children: ReactNode;
  markdown?: boolean;
  className?: string;
}

export default ContentProps;
