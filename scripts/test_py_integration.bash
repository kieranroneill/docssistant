#!/usr/bin/env bash

__DOCKER_PROJECT__=docssistant-test
SCRIPT_DIR=$(dirname "${0}")

source "${SCRIPT_DIR}/utilities/_set_vars.sh"

#######################################
# Stops the docker services. Intended to run from an EXIT trap, so it preserves the exit code of
# the command that triggered it.
# Globals:
#   INFO_PREFIX - read for logging.
#   __DOCKER_PROJECT__ - the Docker Compose project to tear down.
# Outputs:
#   Writes progress to stdout.
# Returns:
#   The exit code the script was already exiting with.
#######################################
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

#######################################
# Starts the necessary Docker services and runs integration tests.
# Globals:
#   INFO_PREFIX - read for logging.
#   __DOCKER_PROJECT__ - the Docker Compose project to start.
# Outputs:
#   Writes progress to stdout, then the pytest output.
# Returns:
#   The pytest exit code.
# Examples:
#   ./test_py_integration.bash
#######################################
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
