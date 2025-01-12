#!/bin/bash

# Extract Strings from API & UI
make docker-compose-sources
docker-compose -f tools/docker-compose/_sources/docker-compose.yml run api_1 make api-link migrate po messages

# Move extracted Strings to Translation Directory
mv api/locale/en-us/LC_MESSAGES/django.po translations/
