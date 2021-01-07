import setuptools
from git_improved.constants import GITHUB_ICONS_URLS


def load_long_description():
    with open('README.md') as readme:
        content = readme.read()
    
    for icon, icon_url in GITHUB_ICONS_URLS.items():
        content.replace(icon, f'<img src="{icon_url}">')

    return content


setuptools.setup(
    name='git-improved',
    description='Add commands to simplify release and publish operation from Git CLI.',
    version='0.1.3',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'git-setup=git_improved.commands.setup:SetupCommand',
            'git-template=git_improved.commands.template:TemplateCommand',

            'git-wip=git_improved.commands.wip:WipCommand',
            'git-save=git_improved.commands.save:SaveCommand',

            'git-cancel=git_improved.commands.cancel:CancelCommand',
            'git-done=git_improved.commands.done:DoneCommand',

            'git-release=git_improved.commands.release:ReleaseCommand',
            'git-unrelease=git_improved.commands.unrelease:UnreleaseCommand'
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
