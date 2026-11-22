# Seconds to wait on Ollama before giving up. Both are overridable with the matching
# OLLAMA_CHAT_TIMEOUT and OLLAMA_EMBEDDING_TIMEOUT environment variables, because the right
# value depends on the hardware: generation that takes seconds on a GPU takes minutes without
# one, and a timeout tuned for the former would make the CPU-only setup unusable.
DEFAULT_CHAT_TIMEOUT = 180.0
DEFAULT_EMBEDDING_TIMEOUT = 60.0
