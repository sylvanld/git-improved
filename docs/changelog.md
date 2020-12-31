# Changelog

## [0.0.2] - 2020-12-29

**Structure**

- Initialize project
	- Initialize devops configuration files
	- Remove package name in import
	- Add branch types shortcuts (doc, fix)
	- Rename package
	- Remove package name from imports

**Documentation**

- Add installation instruction (from PyPI)
- Document commands in README: setup, done, release

**Devops**

- Setup automatic publication
	- Create publish-package.yml
	- Add 'devops' branch type

## [0.0.3] - 2020-12-29

**Feature**

- Create normalized branches
	- Add 'cancel' command to delete current branch
	- Add 'wip' command to create typed branches

## [0.0.4] - 2020-12-29

**Bugfix**

- Prevent running command cancel from branch main
	- Select branch to delete by index in interactive mode
	- Improve delete command
	- Checkout remote branches on interactive cancel
	- Allow specifying the branch to delete
	- Prevent running command cancel on main branch
- Fix variable referenced before assignment in wip command

**Structure**

- Rename new_branch command to wip

**Feature**

- Log categories based on branch prefix instead of directly use prefix
- Add new authorized branches prefixes (improve, improvement, enhancement)

## [0.0.5] - 2020-12-29

**Enhancement**

- Add github icons in commit depending on branch type
	- Append icon when merging a branch
	- Associate an icon to each category

## [0.0.7] - 2020-12-29

**Feature**

- Add 'save' command
	- Add command git-save as entrypoint
	- Save all changes on a single commit
	- Add save command parser

## [0.0.9] - 2020-12-30

**Feature**

- Add unrelease command to remove a tag
	- Add a simple 'unrelease' command to remove release
	- When deleting release, also remove section from changelog
	- Add parser for unrelease command
	- Add command to delete a release from changelog
	- Add a function to retrieve a version from changelog

**Bugfix**

- Reverse commits messages order in done command
- Don't add description on squash if only one commit

**Enhancement**

- Describe squash message using changelog instead of commits
	- Add a difference operation to compare releases
	- Compute difference in changelog after it was edited

## [0.0.10] - 2020-12-30

**Documentation**

- Document package on pypi

## [0.0.11] - 2020-12-31

**Documentation**

- Update roadmap
- Add commands documentation
	- Document cancel command
	- Document wip command
	- Document unrelease command
- Add killer feature to roadmap

**Structure**

- Move shell and git functions in their own files
- Create a command object to handle a command

**Bugfix**

- Fix mistakes due to new command structure
	- Fix wip command
	- Fix commands name in setup
	- Fix setup command
	- Fix release command

**Feature**

- Use a custom shell-menu to input in interactive mode
	- Add a 'menu' class that allow single or multiple selection in a shell
	- Use shell-menu to prompt branch to delete in cancel interactive mode
- Add interactive unrelease using new menu

