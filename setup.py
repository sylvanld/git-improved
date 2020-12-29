import setuptools


setuptools.setup(
    name='git-improved',
    description='Add commands to simplify release and publish operation from Git CLI.',
    version='0.0.6',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'git-setup=git_improved.commands.setup:setup_command',

            'git-wip=git_improved.commands.wip:create_wip_branch_command',

            'git-cancel=git_improved.commands.cancel:cancel_command',
            'git-done=git_improved.commands.done:done_command',
            'git-release=git_improved.commands.release:release_command'
        ]
    },
    install_requires=[
        'bump2version'
    ]
)
