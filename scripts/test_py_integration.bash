#!/usr/bin/env bash

__DOCKER_PROJECT__=docssistant-test
SCRIPT_DIR=$(dirname "${0}")

source "${SCRIPT_DIR}/utilities/_set_vars.sh"

# Private: Stops the docker services.
function _cleanup() {
  local exit_code=$?

  trap - EXIT

  printf "%b stopping docker services... \n" "${INFO_PREFIX}"
  docker compose \
    -f deployments/compose.test.yml \
    -p "${__DOCKER_PROJECT__}" \
    down \
    --volumes || true

  exit "${exit_code}"
}

# Starts the necessary Docker services and runs integration tests.
#
# Examples
#   ./test_py_integration.bash
function main {
  _set_vars

  trap _cleanup EXIT

  # start the services
  printf "%b starting docker services... \n" "${INFO_PREFIX}"
  docker compose \
	 	-f ./deployments/compose.test.yml \
	 	-p "${__DOCKER_PROJECT__}" \
	 	--env-file ./.env.test \
		up \
		--build \
		-d \
		--wait chroma postgres

  # run tests
  printf "%b running integration tests... \n" "${INFO_PREFIX}"
  python3 -m pytest test/integration
}

# and so, it begins...
main
