#!/usr/bin/env python

__version__ = '0.0.1'


import argparse
import subprocess
import os
import sys
import grp
import pwd


parser = argparse.ArgumentParser()

parser.add_argument("--workdir", default="/workdir",
                    # help="Directory to base the uid on")
                    # TODO - improve wording
                    help="Directory the the volume is mounted in the container")

# All positional arguments are passed to args.cmd when it is ran
parser.add_argument("args", default="", nargs=argparse.REMAINDER)

args = parser.parse_args()

username ="pokyuser"

st = os.stat(args.workdir)
uid, gid = st.st_uid, st.st_gid

if uid == 0 or gid ==0:
    # TODO - improve wording
    print("The host workdir can\'t be owned by root")
    sys.exit(1)

try:
    grp.getgrgid(gid)
except KeyError:
    cmd = "sudo groupadd -o -g {} {}".format(gid, username)
    subprocess.check_call(cmd.split(), stdout=sys.stdout, stderr=sys.stderr)

try:
    pwd.getpwuid(uid)
except KeyError:
    cmd = "sudo useradd -g {} -m -o -u {} {}".format(gid, uid, username)
    subprocess.check_call(cmd.split(), stdout=sys.stdout, stderr=sys.stderr)

# Let /opt be owned by pokyuser for sdk purposes
subprocess.check_call("sudo chown -R pokyuser:pokyuser /opt".split())

assert username == "pokyuser", "Sudoers file expects username to be pokyuser"

cmd = "sudo -E -H -u {} ".format(username)
cmd = cmd.split() + ["poky-launch.sh"] + [args.workdir] + args.args
os.execvp(cmd[0], cmd)
