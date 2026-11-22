const DAY_IN_MS = 24 * 60 * 60 * 1000;

/**
 * Formats an ISO date string for the sidebar: a time for today, otherwise a short date.
 * @param {string} isoDate - The date to format.
 * @returns {string} The formatted date.
 */
export default function formatRelativeDate(isoDate: string): string {
  const date = new Date(isoDate);
  const now = new Date();
  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const startOfDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  const isToday = startOfToday.getTime() - startOfDate.getTime() < DAY_IN_MS;

  if (isToday) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  return date.toLocaleDateString([], { day: 'numeric', month: 'short' });
}
