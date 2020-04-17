#!/bin/bash

# shellcheck disable=SC1091
. ./common.sh

workdir=$1

[[ $(pwd) == "$workdir" ]] || failed "Directory comparision failed $(pwd) $workdir"
