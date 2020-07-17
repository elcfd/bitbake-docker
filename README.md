# Bitbake Docker

[![Build Status](https://travis-ci.com/elcfd/bitbake-docker.svg?branch=master)](https://travis-ci.com/elcfd/bitbake-docker)

This project creates docker images which can be used as a containerized build environment for the [Yocto project](https://www.yoctoproject.org/docs/latest/mega-manual/mega-manual.html).

## Features
* Containerized build environment without user permission issues
* The required [package dependencies](https://www.yoctoproject.org/docs/latest/mega-manual/mega-manual.html#required-packages-for-the-build-host) are installed for building with the current Poky release [Dunfell](https://git.yoctoproject.org/cgit/cgit.cgi/poky/log/?h=dunfell)
* The **ncurses** dev package is installed allowing **menuconfig** to be used inside the container
* [Dumb init](https://github.com/Yelp/dumb-init) is used to make sure that the build processes receive the correct signal to terminate

## Running in docker

Choose one of the following:

| Docker Images |
| ---- |
| [elcfd/bitbake:ubuntu-16.04](https://hub.docker.com/r/elcfd/bitbake/tags)   |
| [elcfd/bitbake:ubuntu-18.04](https://hub.docker.com/r/elcfd/bitbake/tags)   |
| [elcfd/bitbake:fedora-29](https://hub.docker.com/r/elcfd/bitbake/tags)      |
| [elcfd/bitbake:fedora-30](https://hub.docker.com/r/elcfd/bitbake/tags)      |

Pull the image from docker hub:

```bash
docker image pull <image_name>
```

To run the container:

```bash
docker container run -it --rm -v /workdir:/workdir <image_name>
```

Where **/workdir** is the location on the host PC that is going to be mounted into the build container.

**NB.** The workdir passed into the container, can be any valid path on the host but must not be owned by the root user.

If the previous command was successful the shell will now be inside the container:

```bash
bbuser@b4e96c8d231c:/workdir$
```

### Workdir Options

To run the container with a different **workdir** inside the container:

```bash
docker container run -it --rm -v /yocto-dev:/yocto-dev <image_name> --workdir=/yocto-dev
```

**NB.** On most images the default user inside a docker container is root. This causes permission issues when mounting a folder from the host to inside a container. These images are built
so that when the container is started the ownership permissions on the folder being passed into the container are reflected inside the container. This means that switching between the folder
on the host and inside the container is seamless.

## Workflow

The suggested workflow is to use the host PC for project version control and editing files with the container used as the build environment. Follow the instructions [here](https://www.yoctoproject.org/docs/current/brief-yoctoprojectqs/brief-yoctoprojectqs.html#brief-use-git-to-clone-poky) but run bitbake from inside the container.


## Development

The following dependencies are required for development:
* docker
* jq
* [task](https://taskfile.dev/#/installation?id=install-script)
* python3
* pytest

### Building the Images

The build process is specified using the [manifest](manifest.json) so if required edit this.

The command to build is:

```bash
task build
```

### Running the Unit Tests

The command to run the unit tests is:

```bash
task tests
```

**NB.** The unit test **test_user_2_id** requires **sudo** to run so will prompt for the **sudo** password.

### Pushing the Built Images to Docker Hub

The command to push the built images is:

```bash
task release
```

## Credits

This work is based on  [crops/yocto-dockerfiles](https://github.com/crops/yocto-dockerfiles) and  [crops/poky-container](https://github.com/crops/poky-container) - thanks is given.
