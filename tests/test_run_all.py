
import pytest
import os


def test_container_user(setup_testdir, run_command, image_name):
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_container_user.sh bbuser".format(setup_testdir, image_name))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


def test_root_workdir(run_command, image_name):
    assert run_command("docker container run --rm -v /mnt:/workdir {}".format(image_name))[0] == 1


def test_valid_standard_workdir(setup_testdir, run_command, image_name):
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_valid_workdir.sh /workdir".format(setup_testdir, image_name))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


def test_valid_non_standard_workdir(setup_testdir, run_command, image_name):
    ret = run_command("docker container run --rm -v {}:/portal {} --workdir=portal /portal/test_valid_workdir.sh /portal".format(setup_testdir, image_name))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


def test_user_id(setup_testdir, run_command, image_name):
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_user_id.sh {} {}".format(setup_testdir, image_name, os.getuid(), os.getgid()))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


def test_dumb_init(setup_testdir, run_command, image_name):
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_dumb_init.sh".format(setup_testdir, image_name))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


# chown the host folder to simulate different user
def test_user_2_id(setup_testdir, run_command, image_name):
    uid, gid = (1003, 1003)
    os.system("sudo /bin/chown {}:{} {}".format(uid, gid, setup_testdir))
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_user_id.sh {} {}".format(setup_testdir, image_name, uid, gid))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


# the yoctouser has ownership of /opt for sdk purposes
def test_opt_perms(setup_testdir, run_command, image_name):
    ret = run_command("docker container run --rm -v {}:/workdir {} /workdir/test_opt_perms.sh".format(setup_testdir, image_name))
    assert ret[0] == 0, "STDOUT: {} STDERR: {}".format(ret[1], ret[2])


def test_incorrect_mount_path(run_command, image_name):
    assert run_command("docker container run --rm -v /workdir:/bad {}".format(image_name))[0] == 1


def test_mount_not_set(run_command, image_name):
    assert run_command("docker container run --rm {}".format(image_name))[0] == 1
