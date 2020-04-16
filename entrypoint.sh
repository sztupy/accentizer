#!/usr/bin/env bash
set -e

case "$1" in
"server")
  shift
  cd server
  bundle exec rackup "$@"
  ;;
"convert")
  shift
  fontforge accentizer.py "$@"
  ;;
*)
  exec "$@"
  ;;
esac
