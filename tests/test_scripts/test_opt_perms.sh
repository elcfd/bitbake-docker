#!/bin/bash

# shellcheck disable=SC1091
. ./common.sh

touch /opt/test-file || failed "opt perms check failed"
