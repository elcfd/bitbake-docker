#!/bin/bash

# shellcheck disable=SC1091
. ./common.sh

[[ "$(ps -q 1 -o comm=)" == "dumb-init" ]] || failed "dumb-init check failed $(ps -q 1 -o comm=)"
