import setuptools


def load_long_description():
    with open('README.md') as readme:
        return readme.read()


setuptools.setup(
    name='git-improved',
    description='Add commands to simplify release and publish operation from Git CLI.',
    version='0.0.10',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'git-setup=git_improved.commands.setup:setup_command',

            'git-wip=git_improved.commands.wip:create_wip_branch_command',
            'git-save=git_improved.commands.save:save_command',

            'git-cancel=git_improved.commands.cancel:CancelCommand',
            'git-done=git_improved.commands.done:DoneCommand',

            'git-release=git_improved.commands.release:ReleaseCommand',
            'git-unrelease=git_improved.commands.unrelease:unrelease_command'
        ]
    },
    install_requires=[
        'bump2version'
    ],
    long_description=load_long_description(),
    long_description_content_type="text/markdown"
)
