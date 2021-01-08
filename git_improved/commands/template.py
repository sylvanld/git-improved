import argparse

from ..exceptions import ValidationError
from ..command import Command
from ..template import Template, GitCredentials
from ..shell import display_table


class TemplateCommand(metaclass=Command):
    def parser():
        parser = argparse.ArgumentParser('git template')
        subparsers = parser.add_subparsers(dest="command")

        install_parser = subparsers.add_parser("install", help="install a template from a remote source")
        install_parser.add_argument("alias", help="the name you want to use locally to reference this template")
        install_parser.add_argument("origin", help="url of the repository where target template is hosted")
        install_parser.add_argument("--branch", default="main", help="branch of the repo containing the template (default: main)")
        install_parser.add_argument("--user", help="username used to autenticate if required")
        install_parser.add_argument("--token", help="pass a token or password to authenticate if required")

        local_install_parser = subparsers.add_parser("local", help="install a template from a local source")
        local_install_parser.add_argument("alias", help="the name you want to use locally to reference this template")
        local_install_parser.add_argument("source", help="local path where target template is located")
        local_install_parser.add_argument("-u", "--upgrade", action="store_true", help="update the given template")

        update_parser = subparsers.add_parser("update", help="update given templates (default to all).")
        update_parser.add_argument("templates", nargs="*", help="if you pass a list of templates, only these templates will be updated...")
        update_parser.add_argument("-v", "--verbose", action="store_true", help="(verbose) display additional informations...")

        update_parser = subparsers.add_parser("list", help="list installed templates.")
        update_parser.add_argument("search", nargs="?", help="python-style regex that can be used to filter output")

        remove_parser = subparsers.add_parser("rm", help="remove installed templates.")
        remove_parser.add_argument("templates", nargs="+", help="alias(es) of the template(s) to remove")

        return parser

    def validate(args):
        if not args.command:
            raise ValidationError('You must specify a command')

    def run(*, command, alias=None, search=None, branch=None, user=None, token=None, origin=None, source=None, upgrade=None, templates=None, verbose=False):
        git_template = Template()

        if command == "install":
            # ensure that user can read this repository (=> public repo or proper authentication)
            GitCredentials().require_credentials(repository=origin)
            git_template.install(template=alias, origin=origin, branch=branch)
        elif command == "local":
            git_template.local_install(template=alias, source=source, upgrade=upgrade)
        elif command == "update":
            templates = templates if templates else git_template.search()
            for template in templates:
                git_template.update(template, verbose=verbose)
        elif command == "list":
            templates = git_template.search(query=search)
            if len(templates) == 0:
                print("no templates available")
            else:
                display_table(templates)
        elif command == "rm":
            for template in templates:
                git_template.remove(template)
