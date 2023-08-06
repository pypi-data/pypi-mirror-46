from setuptools import setup, find_packages
from sys import exit
from os.path import isdir, exists

setup_options = {
    "name": "wwa_app_test",
    "description": "example library",
    "entry_points": {
        'console_scripts': ['wwa_devops=wwa_app_example.main:run']
    }
}


##
## You should not need to touch anything bellow!
##
setup_options["packages"] = find_packages()
# Check if version.txt exists, else abort as it is not a valid project
if exists('version.txt'):
    with open('version.txt') as ver_fd:
        version = ver_fd.readlines()[0].rstrip()
        setup_options["version"] = version
else:
    print("No version.txt file found, aborting.")
    exit(1)

if exists('requirements.txt'):
    with open('requirements.txt') as req_fd:
        requirements = [line for line in req_fd.readlines() if not line.rstrip().startswith("#")] # ignore line comments
        setup_options["install_requires"] = requirements
else:
    print("No requirements.txt file found, no dependencies added.")

if exists('tests_requirements.txt'):
    with open('tests_requirements.txt') as req_fd:
        tests_requirements = [line for line in req_fd.readlines() if not line.rstrip().startswith("#")] # ignore line comments
        setup_options["tests_require"] = tests_requirements,
else:
    print("No tests_requirements.txt file found, no test dependencies added.")
    setup_options["tests_require"] = []

setup_options["test_suite"] = "tests" if isdir("tests") else None

setup(**setup_options)
