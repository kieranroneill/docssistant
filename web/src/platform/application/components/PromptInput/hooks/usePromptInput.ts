import { createContext, createRef, useContext } from 'react';

// types
import type { ContextType } from '../types';

export const PromptInputContext = createContext<ContextType>({
  isLoading: false,
  value: '',
  setValue: () => {},
  maxHeight: 240,
  onSubmit: undefined,
  disabled: false,
  textareaRef: createRef<HTMLTextAreaElement>(),
});

/**
 * Reads the active PromptInput's shared state. Must be used within a PromptInput.
 * @returns {ContextType} The active PromptInput's shared state.
 */
export default function usePromptInput(): ContextType {
  return useContext(PromptInputContext);
}
