# The longest query a caller may submit, in characters.
#
# This is a question, not a document: the generous end of a reasonable question, not a bound
# anyone should meet in normal use. Without it an arbitrarily large body is embedded and then
# pushed into the context window on the request path.
MAX_QUERY_LENGTH = 2000

# The most prior messages replayed when continuing a conversation.
#
# A conversation's history is re-sent with every turn, so an unbounded one eventually exceeds the
# model's context window - and the failure arrives mid-conversation, long after the session that
# caused it. Truncating to the most recent turns bounds the request instead. It is a blunt
# strategy: older turns are forgotten rather than summarised.
MAX_HISTORY_MESSAGES = 20

# The most document excerpt text included in a single prompt, in characters.
#
# Chunk size and the retrieval limit already bound this, so it is a backstop rather than the
# primary control: it keeps the prompt bounded if either is retuned later.
MAX_CONTEXT_CHARACTERS = 12000
