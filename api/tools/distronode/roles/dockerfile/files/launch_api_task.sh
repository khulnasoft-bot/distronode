#!/usr/bin/env bash
if [ `id -u` -ge 500 ]; then
    echo "api:x:`id -u`:`id -g`:,,,:/var/lib/api:/bin/bash" >> /tmp/passwd
    cat /tmp/passwd > /etc/passwd
    rm /tmp/passwd
fi

if [ -n "${API_KUBE_DEVEL}" ]; then
    pushd /api_devel
    make api-link
    popd

    export SDB_NOTIFY_HOST=$MY_POD_IP
fi

set -e

wait-for-migrations

api-manage provision_instance

exec supervisord -c /etc/supervisord_task.conf
