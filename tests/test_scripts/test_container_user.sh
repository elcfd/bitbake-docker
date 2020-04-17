#!/bin/bash

# shellcheck disable=SC1091
. ./common.sh

user=$1

[[ $(whoami) == "$user" ]] || failed "User comparision failed $(whoami) $user"
