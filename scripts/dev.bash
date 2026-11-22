#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "${0}")

source "${SCRIPT_DIR}/utilities/_set_vars.sh"

#######################################
# Starts the development stack.
# Globals:
#   GPU - when set to 1, layers the GPU compose file over the base one to reserve an NVIDIA GPU for
#     Ollama. The stack runs on the CPU otherwise.
#   INFO_PREFIX - read for logging.
# Outputs:
#   Writes the chosen configuration to stdout, then the Docker Compose output.
# Examples:
#   ./dev.bash
#   GPU=1 ./dev.bash
#######################################
function main {
  local compose_files

  _set_vars

  compose_files=('-f' './deployments/compose.development.yml')

  if [ "${GPU}" = '1' ]; then
    printf "%b GPU requested, reserving an NVIDIA GPU for ollama... \n" "${INFO_PREFIX}"
    compose_files+=('-f' './deployments/compose.development.gpu.yml')
  else
    printf "%b no GPU requested, running on the CPU — expect slower answers. \n" "${INFO_PREFIX}"
  fi

  printf "%b starting docker services... \n" "${INFO_PREFIX}"
  exec docker compose \
    "${compose_files[@]}" \
    --env-file ./.env.dev \
    -p docssistant-dev \
    up \
    --build
}

# and so, it begins...
main
