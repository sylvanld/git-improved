import re
import uuid
import argparse
import subprocess
from ..command import Command
from ..constants import BRANCHES_PREFIXES, CATEGORIES_ICONS
from ..changelog import Changelog
from ..git import (
    get_current_branch, merge_squash, get_current_branch_commits,
    ensure_git_initialized, ensure_working_tree_clean, ensure_branch_mergeable
)


class DoneCommand(metaclass=Command):
    def parser():
        parser = argparse.ArgumentParser('git done')
        return parser

    def run():
        ensure_git_initialized()
        #ensure_working_tree_clean()
        ensure_branch_mergeable()
        
        current_branch = get_current_branch()
        branch_type, branch_description = current_branch.split('/')

        change_category = BRANCHES_PREFIXES[branch_type]
        category_icon = CATEGORIES_ICONS[change_category]
        branch_description = branch_description.strip().replace('_', ' ')

        # sort commits from the oldest to the most recent
        commits = list(reversed(get_current_branch_commits()))

        # keep a track of original changelog
        original_changelog = Changelog.parse('docs/changelog.md')

        # parse changelog and add branch changes to [unreleased] appropriate section
        changelog = Changelog.parse('docs/changelog.md')
        changelog.add_change(change_category, branch_description, [commit['message'] for commit in commits])
        changelog.save('docs/changelog.md')

        # open changelog for editing
        subprocess.call(['code', 'docs/changelog.md'])
        input("Edit changelog if required. Then press [enter] to continue...")

        # parse changelog to ensure syntax is still valid after edition
        edited_changelog = Changelog.parse('docs/changelog.md')
        edited_changelog.save('docs/changelog.md')

        # workout changes added to changelog for this branch
        original_unreleased = original_changelog.get_unreleased()
        edited_unreleased = edited_changelog.get_unreleased()

        # Commit all changes
        subprocess.call(['git', 'add', '.'])
        subprocess.call(['git', 'commit', '-m', 'update changelog'])

        # workout squash commit message
        squash_description = category_icon + " " + branch_description

        changes_diff = edited_unreleased.difference(original_unreleased)
        if len(changes_diff.sections) > 0:
            changes = ["- %s"%change.description for change in changes_diff.sections[0].changes if change.indent > 0]
        
            # only add changes to description if more than one change was done
            # to keep description more readable
            if len(changes) > 1:
                squash_description +=  "\n" + "\n".join(changes)
        
        # merge-squash all commits from current branch in main branch
        merge_squash(current_branch, message=squash_description)
