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
git template install [-h] [--branch BRANCH] [--user USER] [--token TOKEN] alias origin
```

Install a template from a remote git repository.

positional arguments:
- **alias**: the name you want to use locally to reference this template
- **origin**: url of the repository where target template is hosted

optional arguments:
- **--branch BRANCH**: branch of the repo containing the template (default: main)
- **--user USER**: username used to autenticate if required
- **--token TOKEN**: pass a token or password to authenticate if required

---

```
git template list [-h] [search]
```

List available templates.

positional arguments:
- **search**: (optional) python-style regex that can be used to filter output

---

```
git template update [-h] [-v] [templates [templates ...]]
```

Pull last version of the template from its git repository.

positional arguments:
- **templates**: (optional) if you pass a list of templates, only these templates will be updated...

optional arguments:
- **--verbose**: display additional informations concerning updated templates...

---

```
git template rm [-h] templates [templates ...]
```

Remove templates

positional arguments:
- **templates**: alias(es) of the template(s) to remove
---

```
git setup --template <template_alias> DIRECTORY
```

Initialize project structure.
- **template_alias**: alias of the template used to initialize project structure.
- **directory**: path to the folder where project must be initialized. (may be . for current folder)

---

```
git wip [category] [description]
```

Create a branch to work on something.
- Branch has a category that describe kind of work. (e.g. Feature, CI/CD, Documentation, ...)
- Description explain what happens on this branch. If not passed, it is prompted.

---

```
git done
```

Merge current branch in main branch.
- Update [unreleased] section of changelog to reflect changes from current branch
- Merge current branch into main in a single commit (contains description of squashed commits)

---

```
git cancel
```

- **Without arguments**: Delete current branch from local and remote.
- **With `-i` option**: Prompt names of multiple branches to delete

---

```bash
git release [--version VERSION | --patch | --minor | --major]
```

Deploy a new release for current project.
- Increment version in all files it is referenced (configure in setup.cfg)
- Replace [unreleased] section of changelog with new version.
- Create a file in `docs/releases` to document this release.

---

```bash
git unrelease [-i] [version]
```

Delete a release from GitHub.
- You can pass the version of the release to delete (or a coma separated list of versions)
- Otherwise, use `-i` option to be prompted for versions to delete.
- You can't pass both `version` and `-i` flag.

## :fire: RoadMap

**Must**

- :fire: Handle changelog/squash message generation when more than one section is changed
- :fire: Add roadmap/assign commands to avoid many people working on same feature
- Display a warning in save command if working on main branch
    - Propose to create a wip branch from current changes to avoid commiting directly...
    - Add an option to reset X last commits from main, put them on a branch, an perform magic merge.
- Add an empty github action that run on unrelease. (can be used to remove packages from registries when tag is deleted)

**Should**

- Study interesting uses cases of a rollback command that cancel changes introduced by a commit
- Improve save command by adding an interactive mode to select staged files
- Add a `--no-changelog` option to `done` command that indicates to not update changelog on merge.

**Could**

- Define a message syntax that indicates that a commit don't go in changelog (e.g prefix with ;)
- Require user to be logged into git using a token.
- Then retrieve author information from github to put in changelog
