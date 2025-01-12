#!/bin/bash
set +x

cd /api_devel
make clean
make api-link

if [[ ! $@ ]]; then
    make test
else
    make $@
fi
