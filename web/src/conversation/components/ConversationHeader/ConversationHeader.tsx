import { type FC } from 'react';
import { useTranslation } from 'react-i18next';
import { Menu } from 'lucide-react';

// ui
import Button from '@/platform/application/components/Button';
import ThemeToggle from '@/platform/application/components/ThemeToggle';

// types
import type { Props } from './types';

const ConversationHeader: FC<Props> = ({ isSidebarOpen, onOpenSidebar, title }) => {
  const { t } = useTranslation();

  return (
    <header className="flex items-center gap-2 border-b border-border p-2">
      <Button
        aria-controls="conversation-sidebar"
        aria-expanded={isSidebarOpen}
        className="shrink-0 md:hidden"
        onClick={onOpenSidebar}
        size="icon"
        type="button"
        variant="ghost"
      >
        <Menu aria-hidden="true" className="h-5 w-5" />
        <span className="sr-only">{t('labels.openSidebar')}</span>
      </Button>

      <h1 className="m-0 min-w-0 flex-1 truncate px-1 text-sm font-semibold" title={title}>
        {title}
      </h1>

      <ThemeToggle className="shrink-0" />
    </header>
  );
};

ConversationHeader.displayName = 'ConversationHeader';

export default ConversationHeader;
