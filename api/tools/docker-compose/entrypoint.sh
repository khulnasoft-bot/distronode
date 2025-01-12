#!/bin/bash

if [ `id -u` -ge 500 ] || [ -z "${CURRENT_UID}" ]; then

cat << EOF > /etc/passwd
root:x:0:0:root:/root:/bin/bash
api:x:`id -u`:`id -g`:,,,:/var/lib/api:/bin/bash
nginx:x:`id -u nginx`:`id -g nginx`:Nginx web server:/var/lib/nginx:/sbin/nologin
EOF

cat <<EOF >> /etc/group
api:x:`id -u`:api
EOF

cat <<EOF > /etc/subuid
api:100000:50001
EOF

cat <<EOF > /etc/subgid
api:100000:50001
EOF

fi

# Required to get rootless podman working after
# writing out the sub*id files above
podman system migrate

if [[ "$OS" ==  *"Docker Desktop"* ]]; then
    export SDB_NOTIFY_HOST='docker.for.mac.host.internal'
else
    export SDB_NOTIFY_HOST=$(ip route | head -n1 | awk '{print $3}')
fi

exec $@
