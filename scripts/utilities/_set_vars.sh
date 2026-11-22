#!/bin/sh

#######################################
# Exports some common environment variables.
# Globals:
#   ERROR_PREFIX - set to a red "[ERROR]" label.
#   INFO_PREFIX - set to a yellow "[INFO]" label.
#######################################
_set_vars() {
  export ERROR_PREFIX="\033[0;31m[ERROR]\033[0m"
  export INFO_PREFIX="\033[1;33m[INFO]\033[0m"
}
