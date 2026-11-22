'use client';

import * as TooltipPrimitive from '@radix-ui/react-tooltip';

// components
import { Content, Provider, Trigger } from './components';

// types
import type { Component, Props } from './types';

const Tooltip = TooltipPrimitive.Root as Component<Props>;

Tooltip.Content = Content;
Tooltip.Provider = Provider;
Tooltip.Trigger = Trigger;

export default Tooltip;
