# Bitbake Docker

[![bitbake docker ci](https://github.com/elcfd/bitbake-docker/actions/workflows/ci-workflow.yml/badge.svg?branch=master)](https://github.com/elcfd/bitbake-docker/actions/workflows/ci-workflow.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/elcfd/bitbake)](https://hub.docker.com/r/elcfd/bitbake)

This project creates docker images which can be used as a containerized build environment for the [Yocto project](https://www.yoctoproject.org/docs/latest/mega-manual/mega-manual.html).

## Features
* Containerized build environment without user permission issues
* The required [package dependencies](https://www.yoctoproject.org/docs/latest/mega-manual/mega-manual.html#required-packages-for-the-build-host) are installed for building with the current Poky release [Hardknott](https://git.yoctoproject.org/cgit/cgit.cgi/poky/log/?h=hardknott)
* The **ncurses** dev package is installed allowing **menuconfig** to be used inside the container
* [Dumb init](https://github.com/Yelp/dumb-init) is used to make sure that the build processes receive the correct signal to terminate

## Running in docker

Choose one of the following:

| Docker Images |
| ---- |
| [elcfd/bitbake:ubuntu-16.04](https://hub.docker.com/r/elcfd/bitbake/tags)   |
| [elcfd/bitbake:ubuntu-18.04](https://hub.docker.com/r/elcfd/bitbake/tags)   |
| [elcfd/bitbake:ubuntu-20.04](https://hub.docker.com/r/elcfd/bitbake/tags)   |

Pull the image from docker hub:

```
docker image pull <image_name>
```

To run the container:

```
docker container run -it --rm -v /workdir:/workdir <image_name>
```

Where **/workdir** is the location on the host PC that is going to be mounted into the build container.

**NB.** The workdir passed into the container, can be any valid path on the host but must not be owned by the root user.

If the previous command was successful the shell will now be inside the container:

```
bbuser@b4e96c8d231c:/workdir$
```

### Workdir Options

To run the container with a different **workdir** inside the container:

```
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
* [task](https://taskfile.dev/#/installation?id=install-script)
* python3
* pytest

### Building the Images

The build process is specified using the [manifest](manifest.json) so if required edit this.

The command to build is:

```
task build
```

### Running the Unit Tests

The command to run the unit tests is:

```
task test
```

**NB.** The unit test **test_user_2_id** requires **sudo** to run so will prompt for the **sudo** password.

### Pushing the Built Images to Docker Hub

The command to push the built images is:

```
task release
```

**NB.** Successful authentication with Dockerhub must have been completed before running this command.

### Specifying an Image

For the three commands; build, test and release the default target is all. This means that all of the images specified in the [manifest](manifest.json) will be used. However,
this can be overridden for example:

* To only build the `ubuntu-16.04` and `ubuntu-18.04` images:

```
task IMAGES=ubuntu-16.04,ubuntu-18.04 build
```

* To only test the `ubuntu-20.04` image:

```
task IMAGES=ubuntu-20.04 test
```

* To build, test and release only the `ubuntu-20.04` image:

```
task IMAGES=ubuntu-20.04
```

## Credits

This work is based on  [crops/yocto-dockerfiles](https://github.com/crops/yocto-dockerfiles) and  [crops/poky-container](https://github.com/crops/poky-container) - thanks is given.
