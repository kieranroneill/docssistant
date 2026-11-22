#!/usr/bin/env bash

source /_set_vars.sh
source /_cleanup.bash

#######################################
# Starts Ollama, ensures the configured models are present, then runs the server in the foreground.
# Globals:
#   OLLAMA_CHAT_MODEL - the Ollama chat model to pull and serve, defaults to "qwen3:4b".
#   OLLAMA_EMBEDDING_MODEL - the Ollama document embedding model to pull and serve, defaults to
#     "nomic-embed-text".
#   OLLAMA_HOST - the address Ollama binds to, defaults to "0.0.0.0:11434". Exported for the server.
#   OLLAMA_PID - set to the process ID of the background Ollama server.
#   ERROR_PREFIX, INFO_PREFIX - read for logging.
# Outputs:
#   Writes progress to stdout, and readiness failures to stderr.
# Returns:
#   1 if the Ollama API does not become ready in time, otherwise does not return — the server
#   replaces the script.
# Examples:
#   ./entrypoint.bash
#######################################
function main() {
  local attempt
  local chat_model
  local embedding_model
  local tags_url
  local host
  local ready

  _set_vars

  chat_model="${OLLAMA_CHAT_MODEL:-qwen3:4b}"
  embedding_model="${OLLAMA_EMBEDDING_MODEL:-nomic-embed-text}"
  host="${OLLAMA_HOST:-0.0.0.0:11434}"
  tags_url="http://127.0.0.1:11434/api/tags"
  ready=0

  printf "starting ollama on \"%s\"...\n" "${host}"
  export OLLAMA_HOST="${host}"
  /bin/ollama serve &
  OLLAMA_PID=$!

  trap cleanup EXIT

  printf "%b waiting for ollama api...\n" "${INFO_PREFIX}"
  for attempt in $(seq 1 60); do
    if curl -fsS "${tags_url}" >/dev/null; then
      ready=1
      break
    fi

    sleep 1
  done

  if [[ "${ready}" -ne 1 ]]; then
    printf "%b ollama api did not become ready in time.\n" "${ERROR_PREFIX}" >&2
    exit 1
  fi

  # pull the models
  for model in "${chat_model}" "${embedding_model}"; do
    if ! curl -fsS "${tags_url}" | jq -e --arg model "${model}" '.models[] | select(.name == $model)' >/dev/null; then
      printf "%b pulling model \"%s\"\n" "${INFO_PREFIX}" "${model}"
      /bin/ollama pull "${model}"
    else
      printf "%b model \"%s\" already present \n" "${INFO_PREFIX}" "${model}"
    fi
  done

  printf "%b restarting ollama in foreground...\n" "${INFO_PREFIX}"
  _cleanup
  trap - EXIT
  exec /bin/ollama serve
}

# and so, it begins...
main
