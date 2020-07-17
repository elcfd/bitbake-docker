import pytest
import os
import subprocess
import shutil
import json
import sys


test_folder_path = os.path.dirname(os.path.realpath(__file__))


def load_manifest_from_file():

    manifest_folder_path = os.path.split(test_folder_path)[0]
    manifest_file_path = os.path.join(manifest_folder_path, "manifest.json")
    try:
        with open(manifest_file_path, "rb") as f:
            manifest = json.load(f)
    except OSError as e:
        sys.exit("Error loading manifest file: {}".format(e))

    return manifest


def get_manifest():

    manifest = load_manifest_from_file()

    images = []
    for image in manifest["images"]:
        image_info = {
            "image_name": "{}/{}:{}".format(manifest["docker_hub_username"], manifest["image_name"], image["name"])
        }
        images.append(image_info)

    return images


def generate_test_names():

    images = get_manifest()

    return [image["image_name"] for image in images]


images = get_manifest()
test_names = generate_test_names()


@pytest.fixture(scope="function")
def run_command():
    def _run(command):
        proc = subprocess.Popen(command.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr
    return _run


@pytest.fixture(scope="function")
def setup_testdir(tmpdir_factory):
    src = os.path.join(test_folder_path, "test_scripts")
    test_path = tmpdir_factory.mktemp("scripts", numbered=True)
    files_to_copy = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
    for f in files_to_copy:
        shutil.copy(os.path.join(src, f), test_path)
    return test_path


@pytest.mark.parametrize("images", images, ids=test_names)
def test_container_user(setup_testdir, run_command, images):
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_container_user.sh bbuser".format(setup_testdir, images["image_name"]))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


@pytest.mark.parametrize("images", images, ids=test_names)
def test_root_workdir(run_command, images):
    assert run_command("docker container run --rm -v /mnt:/workdir {}".format(images["image_name"]))[0] == 1


@pytest.mark.parametrize("images", images, ids=test_names)
def test_valid_standard_workdir(setup_testdir, run_command, images):
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_valid_workdir.sh /workdir".format(setup_testdir, images["image_name"]))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


@pytest.mark.parametrize("images", images, ids=test_names)
def test_valid_non_standard_workdir(setup_testdir, run_command, images):
    ret = run_command("docker container run --rm -v {}:/portal {} --workdir=portal /portal/test_valid_workdir.sh /portal".format(setup_testdir, images["image_name"]))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


@pytest.mark.parametrize("images", images, ids=test_names)
def test_user_id(setup_testdir, run_command, images):
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_user_id.sh {} {}".format(setup_testdir, images["image_name"], os.getuid(), os.getgid()))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


@pytest.mark.parametrize("images", images, ids=test_names)
def test_dumb_init(setup_testdir, run_command, images):
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_dumb_init.sh".format(setup_testdir, images["image_name"]))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


# chown the host folder to simulate different user
@pytest.mark.parametrize("images", images, ids=test_names)
def test_user_2_id(setup_testdir, run_command, images):
    uid, gid = (1003, 1003)
    os.system("sudo /bin/chown {}:{} {}".format(uid, gid, setup_testdir))
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_user_id.sh {} {}".format(setup_testdir, images["image_name"], uid, gid))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


# the yoctouser has ownership of /opt for sdk purposes
@pytest.mark.parametrize("images", images, ids=test_names)
def test_opt_perms(setup_testdir, run_command, images):
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_opt_perms.sh".format(setup_testdir, images["image_name"]))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


@pytest.mark.parametrize("images", images, ids=test_names)
def test_incorrect_mount_path(run_command, images):
    assert run_command("docker container run --rm -v /workdir:/bad {}".format(images["image_name"]))[0] == 1


@pytest.mark.parametrize("images", images, ids=test_names)
def test_mount_not_set(run_command, images):
    assert run_command("docker container run --rm {}".format(images["image_name"]))[0] == 1
