// components
import PlatformAvatar from '@/platform/application/components/Avatar';

// types
import type { AvatarProps as Props } from '../types';

// utilities
import cn from '@/platform/application/utilities/cn';

function Avatar({ src, alt, fallback, delayMs, className }: Props) {
  return (
    <PlatformAvatar className={cn('h-8 w-8 shrink-0', className)}>
      <PlatformAvatar.Image src={src} alt={alt} />
      {fallback && <PlatformAvatar.Fallback delayMs={delayMs}>{fallback}</PlatformAvatar.Fallback>}
    </PlatformAvatar>
  );
}

export default Avatar;
