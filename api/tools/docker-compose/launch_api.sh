#!/bin/bash
set +x

bootstrap_development.sh

cd /api_devel

# Run the given command, usually supervisord
exec "$@"
