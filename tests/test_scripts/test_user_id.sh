#!/bin/bash

# shellcheck disable=SC1091
. ./common.sh

uid=$1
shift
gid=$1


[[ $(id -u) -eq "$uid" ]] || failed "UID check failed $(id -u) $uid"
[[ $(id -g) -eq "$gid" ]] || failed "GID check failed $(id -g) $gid"
