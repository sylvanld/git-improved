import setuptools


setuptools.setup(
    name='git-improved',
    description='Add commands to simplify release and publish operation from Git CLI.',
    version='0.0.2',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'git-setup=git_improved.commands.setup:setup_command',

            'git-feature=git_improved.commands.new_branch:new_feature_branch_command',
            'git-bugfix=git_improved.commands.new_branch:new_bugfix_branch_command',
            'git-doc=git_improved.commands.new_branch:new_doc_branch_command',

            'git-done=git_improved.commands.done:done_command',
            'git-release=git_improved.commands.release:release_command'
        ]
    },
    install_requires=[
        'bump2version'
    ]
)
