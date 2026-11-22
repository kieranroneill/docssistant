#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "${0}")

source "${SCRIPT_DIR}/utilities/_set_vars.sh"

#######################################
# Starts the production stack, in the background. Configuration is read from ".env" when that file
# exists, and from the environment otherwise.
# Globals:
#   GPU - when set to 1, layers the GPU compose file over the base one to reserve an NVIDIA GPU for
#     Ollama. The stack runs on the CPU otherwise.
#   INFO_PREFIX - read for logging.
# Outputs:
#   Writes the chosen configuration to stdout, then the Docker Compose output.
# Examples:
#   ./start.bash
#   GPU=1 ./start.bash
#######################################
function main {
  local compose_args

  _set_vars

  compose_args=('-f' './deployments/compose.yml')

  if [ "${GPU}" = '1' ]; then
    printf "%b GPU requested, reserving an NVIDIA GPU for ollama... \n" "${INFO_PREFIX}"
    compose_args+=('-f' './deployments/compose.gpu.yml')
  else
    printf "%b no GPU requested, running on the CPU — expect slower answers. \n" "${INFO_PREFIX}"
  fi

  # optional, as the configuration can equally come from the environment
  if [ -f ./.env ]; then
    printf "%b using configuration from \".env\"... \n" "${INFO_PREFIX}"
    compose_args+=('--env-file' './.env')
  fi

  printf "%b starting docker services... \n" "${INFO_PREFIX}"
  exec docker compose \
    "${compose_args[@]}" \
    -p docssistant \
    up \
    --build \
    --detach
}

# and so, it begins...
main
