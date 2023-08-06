#!/bin/bash -x

cd $(dirname $0)
curl -o LbPlatformUtils/platforms-list.json \
    $(python -c 'from LbPlatformUtils.describe import BINARY_TAGS_URL; print(BINARY_TAGS_URL)')
git add LbPlatformUtils/platforms-list.json
git commit -m 'Update platforms list' LbPlatformUtils/platforms-list.json
