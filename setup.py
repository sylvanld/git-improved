import setuptools
from src.git_improved.constants import GITHUB_ICONS_URLS


def load_long_description():
    with open('README.md') as readme:
        content = readme.read()
    
    for icon, icon_url in GITHUB_ICONS_URLS.items():
        content = content.replace(icon, f'<img style="max-height: 1.5em" src="{icon_url}">')

    return content


setuptools.setup(
    name='git-improved',
    description='Add commands to simplify release and publish operation from Git CLI.',
    version='0.1.5',
    packages=setuptools.find_packages(exclude=("tests")),
    entry_points={
        'console_scripts': [
            #'git-setup=git_improved.commands.setup:SetupCommand',
            #'git-template=git_improved.commands.template:TemplateCommand',

            'git-wip=git_improved.workflow.commands.wip:WipCommand',
            'git-save=git_improved.workflow.commands.save:SaveCommand',

            'git-cancel=git_improved.workflow.commands.cancel:CancelCommand',
            'git-done=git_improved.workflow.commands.done:DoneCommand',

            'git-release=git_improved.workflow.commands.release:ReleaseCommand',
            'git-unrelease=git_improved.workflow.commands.unrelease:UnreleaseCommand'
        ]
    },
    install_requires=[
        'bump2version',
        'jinja2',
        'requests'
    ],
    long_description=load_long_description(),
    long_description_content_type="text/markdown"
)
