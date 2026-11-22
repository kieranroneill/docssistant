// types
import type VersionModelResponse from './VersionModelResponse';

interface VersionResponse {
  description: string;
  environment: string;
  models: VersionModelResponse;
  title: string;
  version: string;
}

export default VersionResponse;
