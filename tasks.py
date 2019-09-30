import os
from termcolor import cprint
import tempfile
from shutil import which
from subprocess import call
from pathlib import Path

import semver

from invoke import run as invoke_run
from invoke import task

DASH_SPA_DIR = 'dash_spa'

VERSION_TEMPLATE = """__version__ = "{version_string}"
"""

RELEASE_NOTES_TEMPLATE = """# Write the release notes here
# Delete the version title to cancel
Version {version_string}
{underline}
"""

HERE = Path(__file__).parent

@task(help={"version": "Version number to release"})
def prerelease(_ctx, version):
    """
    Release a pre-release version
    Running this task will:
     - Bump the version number
     - Push a release to pypi
    """
    check_prerequisites()
    info(f"Releasing version {version} as prerelease")
    build_publish(version)


@task(help={"version": "Version number to release"})
def release(_ctx, version):
    """
    Release a new version
    Running this task will:
     - Prompt the user for a changelog and write it to
       the release notes
     - Commit the release notes
     - Bump the version number
     - Push a release to pypi
     - commit the version changes to source control
     - tag the commit
    """
    check_prerequisites()
    info(f"Releasing version {version} as full release")

    release_notes_lines = get_release_notes(version)

    if release_notes_lines is None:
        error("No release notes: exiting")
        exit()

    info("Writing release notes to changelog.tmp")
    with open("changelog.tmp", "w") as f:
        f.writelines(release_notes_lines)

    build_publish(version)

    info("Committing version changes")

    run(f"git checkout -b release-{version}")
    run(f"git add {DASH_SPA_DIR}/_version.py")
    run(f'git commit -m "Bump version to {version}"')

    info(f"Tagging version {version} and pushing to GitHub")

    run(f'git tag -a {version} -F changelog.tmp')
    run('call git checkout master')
    run(f'git merge release-{version}')
    run(f'git branch -D release-{version}')

    run(f"git push origin master --tags")


@task(help={
    "version": "Version number to finalize. Must be "
               "the same version number that was used in the release."})
def postrelease(_ctx, version):
    """
    Finalise the release
    Running this task will:
     - bump the version to the next dev version
     - push changes to master
    """
    new_version = semver.bump_patch(version) + "-dev"
    info(f"Bumping version numbers to {new_version} and committing")
    set_pyversion(new_version)
    run(f"git checkout -b postrelease-{version}")
    run(f"git add {DASH_SPA_DIR}/_version.py")
    run('git commit -m "Back to dev"')
    run(f"git push origin postrelease-{version}")


def get_release_notes(version):
    version = normalize_version(version)
    underline = "=" * len(f"Version {version}")
    initial_message = RELEASE_NOTES_TEMPLATE.format(
        version_string=version, underline=underline
    )
    lines = open_editor(initial_message)
    non_commented_lines = [line for line in lines if not line.startswith("#")]
    changelog = "".join(non_commented_lines)
    if version in changelog:
        if not non_commented_lines[-1].isspace():
            non_commented_lines.append("\n")
        return non_commented_lines
    else:
        return None

def open_editor(initial_message):
    editor = os.environ.get("EDITOR", "vim")

    tmp = tempfile.NamedTemporaryFile(suffix=".tmp")
    tmp.close()

    fname = tmp.name

    with open(fname, "w") as f:
        f.write(initial_message)
        f.flush()

    call([editor, fname], close_fds=True)

    with open(fname, "r") as f:
        lines = f.readlines()

    return lines

def build_publish(version):

    def clean():
        paths_to_clean = []
        for path in paths_to_clean:
            run(f"rm -rf {path}")

    def release_python_sdist():
        run("rm -f dist/*")
        run("python setup.py sdist")
        info("PyPI credentials:")
        invoke_run("twine upload dist/*", echo=True)


    info("Cleaning")
    clean()
    info("Updating versions")
    set_pyversion(version)
    info("Building and uploading Python source distribution")
    release_python_sdist()


def set_pyversion(version):

    version = normalize_version(version)
    version_path = HERE / DASH_SPA_DIR / "_version.py"
    with version_path.open("w") as f:
        f.write(VERSION_TEMPLATE.format(version_string=version))

def normalize_version(version):
    version_info = semver.parse_version_info(version)
    version_string = str(version_info)
    return version_string


def check_prerequisites():
    for executable in ["twine"]:
        if which(executable) is None:
            error(
                f"{executable} executable not found. "
                f"You must have {executable} to release "
                "test."
            )
            exit(127)

def run(command, **kwargs):
    print(f'{command}')
    result = invoke_run(command, hide=True, warn=True, **kwargs)
    if (result.exited is not None) and (result.exited != 0):
        error(f"Error running {command}")
        print(result.stdout)
        print()
        print(result.stderr)
        exit(result.exited)

def error(text):
    cprint(text, "red")

def info(text):
    print(text)
