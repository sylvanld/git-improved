# Git Improved

> Python package to add helpful git commands.

## :package: Installation

This package is available from [PyPI](https://pypi.org/project/git-improved/)

It can be installed using

```
pip install git-improved
```

## :star: Additional commands

```
git setup
```

Initialize devops configuration.
- Create a setup.cfg containing current version, and versioning config.
- Create a github action to document releases based on changelog.
- Create `docs/changelog.md`, and `docs/releases/`


```
git done
```

Merge current branch in main branch.
- Update [unreleased] section of changelog to reflect changes from current branch
- Merge current branch into main in a single commit (contains description of squashed commits)


```bash
git release [--version VERSION | --patch | --minor | --major]
```

Deploy a new release for current project.
- Increment version in all files it is referenced (configure in setup.cfg)
- Replace [unreleased] section of changelog with new version.
- Create a file in `docs/releases` to document this release.


## :fire: RoadMap

- Improve save command by adding an interactive mode to select staged files
- Define a message syntax that indicates that a commit don't go in changelog (e.g prefix with ;)
- Add an empty github action that run on unrelease. (can be used to remove packages from registries when tag is deleted)
- Add a `--no-changelog` option to `done` command that indicates to not update changelog on merge.
- Require user to be logged into git using a token.
- Then retrieve author information from github to put in changelog
- Study interesting uses cases of a rollback command that cancel changes introduced by a commit
