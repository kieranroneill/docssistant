// types
import type { VersionResponse } from '@/platform/application/types';

interface UseVersionState {
  isLoading: boolean;
  version: VersionResponse | null;
}

export default UseVersionState;
