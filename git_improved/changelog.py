import re
import os
from datetime import datetime


def sentence(text):
    return text[0].upper() + text[1:]


class SectionChange:
    def __init__(self, description, indent=1):
        self.description = description
        self.indent = indent


class ReleaseSection:
    def __init__(self, *, title, changes=None):
        self.title = title
        self.changes = changes or []

    def add_change(self, change, indent=1):
        self.changes.append(SectionChange(change, indent=indent))

    def contains_change(self, searched_change):
        for change in self.changes:
            if change.description == searched_change.description:
                return True
        return False

    def difference(self, section):
        if section is None:
            return None
        
        if self.title != section.title:
            raise ValueError("Can't compare different sections...")

        changes = []
        for change in self.changes:
            if not section.contains_change(change):
                changes.append(change)
        
        if len(changes) == 0:
            return None
        
        return ReleaseSection(title=self.title, changes=changes)
            

    def render(self):
        rendered = "**%s**\n\n"%sentence(self.title)
        
        for change in self.changes:
            rendered += "\t"*change.indent + "- %s\n"%sentence(change.description)

        rendered += "\n"

        return rendered


class Release:
    """
    Abstraction used to document release in a changelog.
    """
    def __init__(self, *, version, date, sections=None):
        self.version = version
        self.date = date
        self.sections = sections or []


    def add_section(self, section):
        """
        Add a section at the end of this release.
        """
        self.sections.append(section)


    def get_section(self, title):
        """
        Extract a section from this release given its title.
        """
        for section in self.sections:
            if section.title.lower() == title.lower():
                return section
        
        section = ReleaseSection(title=title)
        self.sections.append(section)
        return section


    def difference(self, release):
        """
        Workout a release that is the difference between this release and another.
        """
        sections = []
        for section in self.sections:
            existing_section = release.get_section(section.title)
            diff = section.difference(existing_section)
            if diff is not None:
                sections.append(diff)    

        return Release(version=self.version, date=self.date, sections=sections)


    def describe(self):
        """
        Standalone description used to document releases on github.
        """
        rendered = "*Release [%s] - %s*\n\n"%(self.version, datetime.now().strftime("%Y-%m-%d"))

        for section in self.sections:
            rendered += section.render()

        return rendered

    def render(self, *, level=1):
        """
        Return a markdown description of this release.
        """
        rendered = "#"*level + " [%s]"%self.version

        if self.date:
            rendered += " - %s"%self.date

        rendered += "\n\n"

        for section in self.sections:
            rendered += section.render()

        return rendered


class ChangelogParser:
    @classmethod
    def __open(cls, filename):
        try:
            return open(filename)
        except FileNotFoundError:
            with open(filename, 'w') as file:
                file.write('# Changelog\n\n## [Unreleased]\n\n**Structure**\n\n- Initialize project structure')
            print('Changelog initialized in:', filename)
            return open(filename)
    
    @classmethod
    def parse(cls, filename, level=1):
        with cls.__open(filename) as file:
            rows = file.read().split('\n')

        title_pattern = re.compile("^" + level*"#" + "\s+(?P<title>.*changelog.*)", re.IGNORECASE)
        release_pattern = re.compile("^" + (level+1)*"#" + "\s+\[(?P<version>.+)\](?: - (?P<date>\d{4}-\d{2}-\d{2}))?")
        section_pattern = re.compile("\*\*(?P<title>.+)\*\*")
        change_pattern = re.compile("^(?P<indentation>\t*)-\s(?P<description>.*)")

        changelog_start = -1

        title = None
        description = None
        releases = []

        current_release = None
        current_section = None

        for i in range(len(rows)):
            changelog_title_match = title_pattern.match(rows[i])
            release_match = release_pattern.match(rows[i])
            section_match = section_pattern.match(rows[i])
            change_match = change_pattern.match(rows[i])
            
            if changelog_title_match:
                title = changelog_title_match.groupdict()['title']
            elif release_match:
                if current_release:
                    if current_section:
                        current_release.add_section(current_section)
                        current_section = None
                    releases.append(current_release)
                    current_release = None
                release = release_match.groupdict()
                current_release = Release(version=release['version'], date=release.get('date'))
            elif section_match and current_release:
                if current_section:
                    current_release.add_section(current_section)
                    current_section = None

                section = section_match.groupdict()
                current_section = ReleaseSection(title=section['title'])
            elif change_match and current_section:
                change = change_match.groupdict()
                current_section.add_change(change['description'], indent=len(change['indentation']))
        
        if current_release:
            if current_section:
                current_release.add_section(current_section)
            releases.append(current_release)

        return Changelog(title=title, description=description, releases=releases)


class Changelog:
    def __init__(self, *, title, description=None, releases=None):
        self.title = title
        self.description = description
        self.releases = releases or []

    def get_unreleased(self):
        for release in self.releases:
            if release.version.lower() == 'unreleased' or not release.date:
                return release
        
        unreleased = Release(version='Unreleased', date=None)
        self.releases.append(unreleased)
        return unreleased

    def get_release(self, version):
        for release in self.releases:
            if release.version.lower() == version:
                return release

        raise KeyError("Version not found in changelog")

    def delete_release(self, version):
        try:
            release = self.get_release(version)
            self.releases.remove(release)
        except KeyError:
            print("[Warning] Can't delete version %s from changelog"%version)

        try:
            os.remove("docs/releases/%s.md"%version)
        except FileNotFoundError:
            print("[Warning] Can't delete 'docs/releases/%s.md': file not found"%version)


    def add_change(self, section, description, changes=None):
        unreleased = self.get_unreleased()
        section = unreleased.get_section(section)
        section.add_change(description, indent=0)

        changes = changes or []
        for change in changes:
            section.add_change(change, indent=1)

    def render(self, *, level=1):
        rendered = "#"*level + " %s"%self.title + "\n\n"

        if self.description:
            rendered += self.description + "\n\n"

        for release in self.releases:
            rendered += release.render(level=level+1)
        
        return rendered

    def save(self, filename):
        with open(filename, 'w') as file:
            file.write(self.render())

    def create_release(self, version, release_file=None):
        release = self.get_unreleased()
        release.version = version
        release.date = datetime.now().strftime('%Y-%m-%d')
        if release_file:
            with open(release_file, 'w') as release_file:
                release_file.write(release.describe())

    @classmethod
    def parse(self, filename):
        return ChangelogParser.parse(filename)
