import { type MouseEventHandler, useRef, useState } from 'react';

// components
import { Action, Actions, Textarea } from './components';

// components (primitives)
import Tooltip from '@/platform/application/components/Tooltip';

// hooks
import { PromptInputContext } from './hooks';

// types
import type { Component, Props } from './types';

// utilities
import cn from '@/platform/application/utilities/cn';

const PromptInput: Component<Props> = ({
  className,
  isLoading = false,
  maxHeight = 240,
  value,
  onValueChange,
  onSubmit,
  children,
  disabled = false,
  onClick,
  ...props
}) => {
  const [internalValue, setInternalValue] = useState(value || '');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleChange = (newValue: string) => {
    setInternalValue(newValue);
    onValueChange?.(newValue);
  };

  const handleClick: MouseEventHandler<HTMLDivElement> = (e) => {
    if (!disabled) textareaRef.current?.focus();
    onClick?.(e);
  };

  return (
    <Tooltip.Provider>
      <PromptInputContext.Provider
        value={{
          isLoading,
          value: value ?? internalValue,
          setValue: onValueChange ?? handleChange,
          maxHeight,
          onSubmit,
          disabled,
          textareaRef,
        }}
      >
        <div
          onClick={handleClick}
          className={cn(
            'border-input bg-background cursor-text rounded-3xl border p-2 shadow-xs',
            disabled && 'cursor-not-allowed opacity-60',
            className
          )}
          {...props}
        >
          {children}
        </div>
      </PromptInputContext.Provider>
    </Tooltip.Provider>
  );
};

PromptInput.Action = Action;
PromptInput.Actions = Actions;
PromptInput.Textarea = Textarea;

export default PromptInput;
