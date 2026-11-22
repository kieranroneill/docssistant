import { type ChangeEvent, type KeyboardEvent, useLayoutEffect } from 'react';

// components
import Textarea from '@/platform/application/components/Textarea';

// hooks
import { usePromptInput } from '../hooks';

// types
import type { TextareaProps as Props } from '../types';

// utilities
import cn from '@/platform/application/utilities/cn';

function PromptInputTextarea({ className, onKeyDown, disableAutosize = false, ...props }: Props) {
  const { value, setValue, maxHeight, onSubmit, disabled, textareaRef } = usePromptInput();

  const adjustHeight = (el: HTMLTextAreaElement | null) => {
    if (!el || disableAutosize) return;

    el.style.height = 'auto';

    if (typeof maxHeight === 'number') {
      el.style.height = `${Math.min(el.scrollHeight, maxHeight)}px`;
    } else {
      el.style.height = `min(${el.scrollHeight}px, ${maxHeight})`;
    }
  };

  const handleRef = (el: HTMLTextAreaElement | null) => {
    textareaRef.current = el;
    adjustHeight(el);
  };

  useLayoutEffect(() => {
    if (!textareaRef.current || disableAutosize) return;

    const el = textareaRef.current;
    el.style.height = 'auto';

    if (typeof maxHeight === 'number') {
      el.style.height = `${Math.min(el.scrollHeight, maxHeight)}px`;
    } else {
      el.style.height = `min(${el.scrollHeight}px, ${maxHeight})`;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value, maxHeight, disableAutosize]);

  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    adjustHeight(e.target);
    setValue(e.target.value);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSubmit?.();
    }
    onKeyDown?.(e);
  };

  return (
    <Textarea
      ref={handleRef}
      value={value}
      onChange={handleChange}
      onKeyDown={handleKeyDown}
      className={cn(
        'text-primary min-h-[44px] w-full resize-none border-none bg-transparent shadow-none outline-none focus-visible:ring-0 focus-visible:ring-offset-0',
        className
      )}
      rows={1}
      disabled={disabled}
      {...props}
    />
  );
}

export default PromptInputTextarea;
