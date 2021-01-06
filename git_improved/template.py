import os
import re
import json
import shutil
import requests
import argparse
import subprocess
import importlib.util
from getpass import getpass
from tqdm import tqdm
from jinja2 import Environment, PackageLoader, select_autoescape
from .shell import check_output
from .git import get_remote_origin


def load_environment(template_path):
    spec = importlib.util.spec_from_file_location("configure", os.path.join(template_path, "configure.py"))
    configure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(configure)
    return configure.environment


def setup_project(*, template, destination):
    template_root = 'templates/%s'%template
    templates_path = os.path.join(template_root, 'template')

    environment = load_environment(template_path=template_root)

    templating_engine = Environment(
        loader=PackageLoader(__name__, template_root),
        autoescape=select_autoescape(['py'])
    )

    # associate template file name to dest file name (name is templated)
    files = []

    for obj in os.walk(templates_path):
        source_folder = obj[0]
        
        # create directories that contains files
        for directory in obj[1]:
            source = os.path.join(source_folder, directory)
            dest = templating_engine.from_string(source.replace(templates_path, destination)).render(**environment)
            os.makedirs(dest, exist_ok=True)

        # create files in current directory
        for filename in obj[2]:
            source = os.path.join(source_folder, filename)
            dest = templating_engine.from_string(source.replace(templates_path, destination)).render(**environment)
            template = templating_engine.get_template(source.replace(template_root, ''))

            with open(dest, 'w') as file:
                file.write(template.render(**environment))


def parse_template_command():
    parser = argparse.ArgumentParser('git template')
    subparsers = parser.add_subparsers(dest="command")

    install_parser = subparsers.add_parser("install", help="install a template from a remote source")
    install_parser.add_argument("alias", help="the name you want to use locally to reference this template")
    install_parser.add_argument("origin", help="url of the repository where target template is hosted")
    install_parser.add_argument("--branch", default="main", help="branch of the repo containing the template (default: main)")
    install_parser.add_argument("--user", help="username used to autenticate if required")
    install_parser.add_argument("--token", help="pass a token or password to authenticate if required")

    update_parser = subparsers.add_parser("update", help="Update given templates (default to all).")
    update_parser.add_argument("templates", nargs="*", help="If you pass a list of templates, only these templates will be updated...")

    update_parser = subparsers.add_parser("list", help="List installed templates.")
    update_parser.add_argument("search", nargs="?", help="Python-style regex that can be used to filter output")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        exit(0)

    return args


class TemplateManifest:
    def __init__(self, templates_path):
        self.templates_path = templates_path
        self.path = os.path.join(templates_path, 'templates.json')
        self.__content = None

    def __open(self):
        try:
            return open(self.path)
        except FileNotFoundError:
            os.makedirs(self.templates_path, exist_ok=True)        
            with open(self.path, 'w') as manifest:
                json.dump({"templates": []}, manifest, indent=4)
            return open(self.path)

    def __save(self):
        content = self.content
        with open(self.path, 'w') as manifest:
            json.dump(content, manifest, indent=4)

    @property
    def content(self):
        if not self.__content:
            self.__content = json.load(self.__open())
        return self.__content

    def add_template(self, template:str):
        if template in self.templates:
            raise FileExistsError("A template named %s already exists in %s"%(template, self.templates_path))
        self.templates.append(template)
        self.__save()

    def remove_template(self, template:str):
        if template in self.templates:
            self.templates.remove(template)
            self.__save()

    @property
    def templates(self):
        return self.content["templates"]


REPO_URL_PATTERN = re.compile("(?P<protocol>\w+)\:\/\/(?:(?P<username>.+)\:(?P<token>.+)@)?(?P<domain>[^/]+)/")

class GitCredentials:
    def __init__(self):
        self.path = os.path.expanduser("~/.git-credentials")
        self.__credentials = None


    def __save(self):
        content = ""
        for credential in self.credentials:
            content += f"{credential['protocol']}://{credential['username']}:{credential['token']}@{credential['domain']}\n"
        
        with open(self.path, "w") as credentials_file:
            credentials_file.write(content)


    def has_credentials(self, *, repository=None, domain=None):
        if (repository is None) == (domain is None):
            raise IOError("Either repository or domain must be passed. (not both)")

        if domain is not None:
            for credential in self.credentials:
                if domain in credential["domain"]:
                    return True
            return False

        if repository is not None:
            match = REPO_URL_PATTERN.match(repository)

            if not match:
                raise ValueError("%s does not look like a valid repository URL."%repository)

            info = match.groupdict()
            if info["username"] and info["token"]:
                return True

        return False

    
    def require_credentials(self, *, repository=None, domain=None):
        
        if not self.has_credentials(repository=repository, domain=domain):
            if repository is not None:
                response = requests.get(repository)
                if response.status_code >= 200 and response.status_code < 300:
                    return "This repo does not requires authentication"
                
                match = REPO_URL_PATTERN.match(repository)

                if not match:
                    raise ValueError("%s does not look like a valid repository URL."%repository)

                scope = match.groupdict()
            else:
                scope = {"domain": domain}
            
            self.authenticate(**scope)


    def authenticate(self, *, domain, username=None, token=None, protocol="https"):
        if self.has_credentials(domain=domain):
            print("Already authenticated")
            return

        if not username or not token:
            print("Authentication required for %s"%domain)
        
        self.credentials.append({
            "protocol": protocol,
            "username": username if username else input("username: "),
            "token": token if token else getpass(),
            "domain": domain
        })
        self.__save()

    @property
    def credentials(self):
        if not self.__credentials:
            credential_pattern = re.compile("(?P<protocol>\w+)\:\/\/(?P<username>.+)\:(?P<token>.+)@(?P<domain>.+)")
            try:
                with open(self.path) as credentials_file:
                    content = credentials_file.read()
                self.__credentials = [m.groupdict() for m in credential_pattern.finditer(content)]
            except FileNotFoundError:
                self.__credentials = {}
        return self.__credentials


def log_update(template, status):
    if status == "updated":
        status_message = "\033[33m[updated]\033[00m  "
    elif status == "unchanged":
        status_message = "\033[32m[unchanged]\033[00m"
    elif status == "failed":
        status_message = "\033[31m[failed]\033[00m   "
    else:
        raise ValueError("Unknown update status received: %s"%status)
    print("%s  %s"%(status_message.ljust(10), template))


class Template:
    def __init__(self):
        self.templates_directory = os.path.expanduser("~/.git-templates")
        self.manifest = TemplateManifest(self.templates_directory)

    def search(self, *, query=None, abspath=False):
        return [
            os.path.join(self.templates_directory, template) if abspath else template
            for template in self.manifest.templates
            if not query or query in template
        ]
    
    def install(self, *, template, origin, user=None, token=None, branch='main'):
        self.manifest.add_template(template)
        template_path = os.path.join(self.templates_directory, template)
        os.makedirs(template_path)
        os.chdir(template_path)

        # retrieve project in .git-templates/ folder
        subprocess.call(['git', 'init'])
        subprocess.call(['git', 'remote', 'add', 'origin', origin])
        subprocess.call(['git', 'checkout', '-b', branch])
        subprocess.call(['git', 'pull', 'origin', branch])
        subprocess.call(['git', 'branch', '--set-upstream-to=origin/%s'%branch, branch])

    def update(self, template, verbose=False):        
        template_path = os.path.join(self.templates_directory, template)
        update_target = template

        try:
            os.chdir(template_path)
            if verbose: # workout additionals infos in verbose mode
                update_target += "\t(%s)"%get_remote_origin()
        
            fetch_output = check_output("git", "fetch", "--dry-run")
            if fetch_output:
                subprocess.check_call(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                log_update(update_target, status="updated")
            else:
                log_update(update_target, status="unchanged")
        except Exception:
            log_update(update_target, status="failed")

    def remove(self, template):
        try:
            template_path = os.path.join(self.templates_directory, template)
            self.manifest.remove_template(template)
            shutil.rmtree(template_path)
        except FileNotFoundError as e:
            print("[Warning] %s not found!"%template_path)
        print('template removed:', template)
            

if __name__ == '__main__':
    args = parse_template_command()
    git_template = Template()

    if args.command == "install":
        # ensure that user can read this repository (=> public repo or proper authentication)
        GitCredentials().require_credentials(repository=args.origin)
        git_template.install(template=args.alias, origin=args.origin, branch=args.branch)
    elif args.command == "update":
        templates = args.templates if args.templates else git_template.search(abspath=False)
        git_template.update(template)
    elif args.command == "list":
        templates = git_template.search(query=args.search)
