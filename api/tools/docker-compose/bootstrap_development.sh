#!/bin/bash
set +x

# Move to the source directory so we can bootstrap
if [ -f "/api_devel/manage.py" ]; then
    cd /api_devel
else
    echo "Failed to find api source tree, map your development tree volume"
fi

make api-link

# API bootstrapping
make version_file

if [[ -n "$RUN_MIGRATIONS" ]]; then
    # wait for postgres to be ready
    while ! nc -z postgres 5432; do
        echo "Waiting for postgres to be ready to accept connections"; sleep 1;
    done;
    make migrate
else
    wait-for-migrations
fi


# Make sure that the UI statifc file directory exists, if UI is not built yet put a placeholder file in it.
if [ ! -d "/api_devel/api/ui/build/api" ]; then
    mkdir -p /api_devel/api/ui/build/api
    cp /api_devel/api/ui/placeholder_index_api.html /api_devel/api/ui/build/api/index_api.html
fi

if output=$(DISTRONODE_REVERSE_RESOURCE_SYNC=false api-manage createsuperuser --noinput --username=admin --email=admin@localhost 2> /dev/null); then
    echo $output
fi
echo "Admin password: ${DJANGO_SUPERUSER_PASSWORD}"

DISTRONODE_REVERSE_RESOURCE_SYNC=false api-manage create_preload_data
api-manage register_default_execution_environments

api-manage provision_instance --hostname="$(hostname)" --node_type="$MAIN_NODE_TYPE"
api-manage add_receptor_address --instance="$(hostname)" --address="$(hostname)" --port=2222 --canonical

api-manage register_queue --queuename=controlplane --instance_percent=100
api-manage register_queue --queuename=default --instance_percent=100

if [[ -n "$RUN_MIGRATIONS" ]]; then
    for (( i=1; i<$CONTROL_PLANE_NODE_COUNT; i++ )); do
        for (( j=i + 1; j<=$CONTROL_PLANE_NODE_COUNT; j++ )); do
            api-manage register_peers "api-$i" --peers "api-$j"
        done
    done

    if [[ $EXECUTION_NODE_COUNT > 0 ]]; then
        api-manage provision_instance --hostname="receptor-hop" --node_type="hop"
        api-manage add_receptor_address --instance="receptor-hop" --address="receptor-hop" --port=5555 --canonical
        api-manage register_peers "receptor-hop" --peers "api-1"
        for (( e=1; e<=$EXECUTION_NODE_COUNT; e++ )); do
            api-manage provision_instance --hostname="receptor-$e" --node_type="execution"
            api-manage register_peers "receptor-$e" --peers "receptor-hop"
        done
    fi
fi

# Create resource entries when using Minikube
if [[ -n "$MINIKUBE_CONTAINER_GROUP" ]]; then
    api-manage shell < /api_devel/tools/docker-compose-minikube/_sources/bootstrap_minikube.py
fi
