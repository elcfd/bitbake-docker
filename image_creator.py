
import logging
import argparse
import json
import sys
import time
import subprocess


LOG = logging.getLogger("image-creator")
MANIFEST = "manifest.json"


logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG
)


def read_manifest_file():

    try:
        with open(MANIFEST, "rb") as fh:
            manifest = json.load(fh)
    except OSError as e:
        sys.exit("Error loading manifest file: {}".format(e))
    
    return manifest


def generate_cmds(manifest, names, action):

    cmds = []
    username = manifest["docker_hub_username"]
    repository = manifest["repository"]
    for manifest_image in manifest["images"]:
        if isinstance(names, str) and names.lower() == "all" or manifest_image["name"] in names:
            image_name = "{}/{}:{}".format(username, repository, manifest_image["name"])
            if action == "build":
                cmds.append("docker build -t {} -f {} .".format(
                    image_name, manifest_image["dockerfile"]
                )
                )
            elif action == "release":
                cmds.append("docker image push {}".format(image_name))
                datestamp_tag = "{}-{}".format(image_name, time.strftime("%Y_%m_%d-%H_%M_%S"))
                cmds.append("docker image tag {} {}".format(image_name, datestamp_tag))
                cmds.append("docker image push {}".format(datestamp_tag))

    return cmds


def run_system_cmd(cmd):

    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    
    while True:
        output = proc.stdout.readline()
        if output == b'' and proc.poll() is not None:
            break
        if output:
            LOG.info("{}".format(output.strip().decode()))
    
    rc = proc.poll()

    if rc != 0:
        e = "Error running command \"{}\"".format(cmd)
        LOG.error(e)
        raise RuntimeError(e)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["build", "release"], help="action to perform")
    parser.add_argument("names", help="images to perform action on")
    args = parser.parse_args()

    if args.names.lower() != "all":
        args.names = args.names.split(",")

    manifest = read_manifest_file()
    cmds = generate_cmds(manifest, args.names, args.action)

    for cmd in cmds:
        run_system_cmd(cmd)


if __name__ == "__main__":
    main()
