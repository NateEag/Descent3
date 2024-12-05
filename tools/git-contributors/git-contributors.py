#!/usr/bin/python3

# Descent 3
# Copyright (C) 2024 Descent Developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from git import Repo
import argparse
import re


def strip_comments(code):
    code = str(code)
    return re.sub(r'(#.*)?\n?', '', code)


def main():
    parser = argparse.ArgumentParser(
        prog="git-contributors.py",
        description="Script to generate contributors list from git history.",
    )
    parser.add_argument(
        "--output", "-o",
        required=False,
        default="../../scripts/data/fullhog/oscredits.txt",
        help="output file",
    )
    args = parser.parse_args()

    noadds = list()
    name_maps = dict()
    with open("no-add.txt") as noadd_file:
        for line in noadd_file:
            name = strip_comments(line)
            noadds.append(name.strip())
    with open("map-names.txt") as map_file:
        for line in map_file:
            (git_name, replace_name) = strip_comments(line.strip()).split(":")
            name_maps.update({git_name: replace_name})

    repo = Repo(search_parent_directories=True)
    commits = list(repo.iter_commits("main"))
    authors = set()

    for commit in commits:
        if commit.author.name not in noadds:
            if commit.author.name in name_maps.keys():
                authors.add(name_maps[commit.author.name])
            else:
                authors.add(commit.author.name)

    with open(args.output, "w") as result_file:
        result_file.write("; This file was autogenerated by git-contributors.py\n")
        result_file.write("\n")
        result_file.write("\n")
        result_file.write("*320 100 320 100 8\n")
        result_file.write("!OPEN SOURCE CONTRIBUTORS\n")
        result_file.write("\n")
        result_file.write("https://github.com/DescentDevelopers/Descent3\n")
        result_file.write("\n")

        for author in sorted(authors):
            result_file.write(f"{author}\n")

        result_file.write("\n")
        result_file.write("END\n")
    print("All done!")


if __name__ == "__main__":
    main()
