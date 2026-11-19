#!/usr/bin/env bash

source /_set_vars.sh
source /_cleanup.bash

# Public: Starts Ollama, ensures the configured model is present, then runs the server in the foreground.
#
# Environment Variables
#
# OLLAMA_CHAT_MODEL - The Ollama chat model to pull and serve, defaults to "qwen3:4b".
# OLLAMA_EMBEDDING_MODEL - The Ollama document embedding model to pull and serve, defaults to "nomic-embed-text".
#
# Examples
#   ./entrypoint.bash
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
