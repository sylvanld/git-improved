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

## [Unreleased]

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

