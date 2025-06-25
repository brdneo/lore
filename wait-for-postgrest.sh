#!/bin/sh
# wait-for-postgrest.sh - v2

set -e

host="$1"
shift
cmd="$@"

until curl -sSf "$host" > /dev/null; do
  >&2 echo "PostgREST is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgREST is up - executing command"
# A linha abaixo foi corrigida para ser compatível com sh/dash.
exec "$@"
