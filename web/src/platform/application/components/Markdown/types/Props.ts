import type { Components } from 'react-markdown';

interface Props {
  children: string;
  id?: string;
  className?: string;
  components?: Partial<Components>;
}

export default Props;
