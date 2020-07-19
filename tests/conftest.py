
import pytest
import os
import subprocess
import shutil
import json
import sys


TEST_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))


def load_manifest_from_file():

    manifest_folder_path = os.path.split(TEST_FOLDER_PATH)[0]
    manifest_file_path = os.path.join(manifest_folder_path, "manifest.json")
    try:
        with open(manifest_file_path, "rb") as f:
            manifest = json.load(f)
    except OSError as e:
        sys.exit("Error loading manifest file: {}".format(e))

    return manifest


def filter_images_to_test(image_names):

    manifest = load_manifest_from_file()

    images_to_test = []
    for manifest_image in manifest["images"]:
        if isinstance(image_names, str) and image_names.lower() == "all" or manifest_image["name"] in image_names:
            image_name = "{}/{}:{}".format(
                manifest["docker_hub_username"], manifest["repository"], manifest_image["name"]
            )
            images_to_test.append(image_name)

    return images_to_test


def pytest_addoption(parser):

    parser.addoption("--image_names", action="store")


def pytest_generate_tests(metafunc):

    image_names = metafunc.config.getoption("--image_names")
    if image_names.lower() != "all":
        image_names = image_names.split(",")
    images = filter_images_to_test(image_names)

    if not images:
        sys.exit("No images were selected for testing")

    metafunc.parametrize("image_name", images, ids=images)


@pytest.fixture(scope="function")
def setup_testdir(tmpdir_factory):
    src = os.path.join(TEST_FOLDER_PATH, "test_scripts")
    test_path = tmpdir_factory.mktemp("scripts", numbered=True)
    files_to_copy = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
    for f in files_to_copy:
        shutil.copy(os.path.join(src, f), test_path)
    return test_path


@pytest.fixture(scope="function")
def run_command():
    def _run(command):
        proc = subprocess.Popen(command.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr
    return _run
