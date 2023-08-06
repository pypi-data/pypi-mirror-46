# thoth-build-analysers
# Copyright(C) 2018, 2019 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Parse packages installed using pip3."""

import logging
import re
import typing

import attr

from .base import HandlerBase

_RE_PACKAGE_NAME = re.compile(r"[a-zA-Z0-9_]")
_RE_COLLECTING_DEPENDENCY = re.compile(r'Collecting ([+a-zA-Z_\-.():/0-9>=<;,"]+)')  # Ignore PycodestyleBear (E501)
_RE_COLLECTING_DEPENDENCY_FROM = re.compile(
    r'Collecting ([+a-zA-Z_\-.():/0-9>=<;,"]+) '  # Ignore PycodestyleBear (E501)
    r"\(from ([a-zA-Z_\-.():/0-9>=<, ]+)\)"
)  # Ignore PycodestyleBear (E501)
_RE_COLLECTING_DEPENDENCY_REMOTE = re.compile(
    r'Collecting ([+a-zA-Z_\-.():/0-9>=<;,"]+) ' r"from ([a-zA-Z_\-.():/0-9>=<, ]+)"  # Ignore PycodestyleBear (E501)
)  # Ignore PycodestyleBear (E501)
_RE_DOWNLOADING_ARTIFACT = re.compile(
    r'  Downloading ([+a-zA-Z_\-.:/0-9>=<;,"]+)( \(([a-zA-Z.,0-9]+)\))?'
)  # Ignore PycodestyleBear (E501)
_RE_ALREADY_SATISFIED = re.compile(
    r'Requirement already satisfied: ([+a-zA-Z_\-.():/0-9>=<;,"]+) in '  # Ignore PycodestyleBear (E501)
    r'([+a-zA-Z_\-.():/0-9>=<;,"]+) \(from ([a-zA-Z_\-.():/0-9>=<, ]+)\)'
)  # Ignore PycodestyleBear (E501)
_RE_ESCAPE_SEQ = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]")

_LOG = logging.getLogger("thoth.build_analysers.parsing.handlers.pip3")


@attr.s
class PIP3(HandlerBase):
    """Handle extracting packages from build logs - pip3 installer."""

    @staticmethod
    # Ignore PycodestyleBear (E501)
    def _do_parse_package(package_specifier: str) -> typing.Tuple[str, typing.Optional[str]]:
        """Parse packages from a report line.

        Parsing the packages and return them in a
        tuple describing also version, version specifier.
        """
        if package_specifier.startswith("git+"):
            _LOG.warning(
                "Detected installing a Python package from a git repository: %r", package_specifier
            )  # Ignore PycodestyleBear (E501)
            package_name = package_specifier
            version = "master"

            # Try to find branch or commit specification.
            split_result = package_specifier.rsplit("@", maxsplit=1)
            if len(split_result) == 2:
                package_name = split_result[0]
                version = split_result[1]

            return package_name, version

        # See https://www.python.org/dev/peps/pep-0440/#version-specifiers for
        # all possible values.  # Ignore PycodestyleBear (E501)
        version_start_idx = None
        for ver_spec in ("~=", "!=", "===", "==", "<=", ">=", ">", "<"):
            try:
                found_idx = package_specifier.index(ver_spec)
                if version_start_idx is None or found_idx < version_start_idx:
                    version_start_idx = found_idx
            except ValueError:
                pass

        if version_start_idx:
            # Ignore PycodestyleBear (E501)
            return package_specifier[:version_start_idx], package_specifier[version_start_idx:]

        return package_specifier, None

    @classmethod
    # Ignore PycodestyleBear (E501)
    def _parse_package(cls, package_specifier: str, is_from: bool = False) -> dict:
        """Parse packages and return them in a dictionary."""
        result = []
        if not is_from:
            parsed_package = cls._do_parse_package(package_specifier)
            result = {
                "package": parsed_package[0],
                "version_specified": parsed_package[1],
                "version_installed": None,
                "already_satisfied": None,
            }
        else:
            for package in package_specifier.split("->"):
                parsed_package = cls._do_parse_package(package)
                result.append({"package": parsed_package[0], "version_specified": parsed_package[1]})

        return result or None

    @staticmethod
    def _check_entry(result, package_name, package_version):
        """Check parsed entries against reported installed entries.

        Check the parsed entries after pip installed them successful.
        """
        matched = [entry for entry in result if entry["package"] == package_name]  # Ignore PycodestyleBear (E501)

        if len(matched) > 1:
            _LOG.warning(
                "Package %r was installed multiple times in versions %s",
                package_name,  # Ignore PycodestyleBear (E501)
                tuple(entry["version_specified"] for entry in matched),
            )  # Ignore PycodestyleBear (E501)

        if not matched:
            _LOG.error(
                "Package %r was not parsed in the output - detected installed version %r, error is not fatal",  # Ignore PycodestyleBear (E501)
                package_name,
                package_version,
            )

        # Ignore PycodestyleBear (E501)
        if package_version not in (entry["version_specified"] for entry in matched):
            _LOG.debug(
                "Installation of Python package %r using pip with version specifiers %s installed version %s",  # Ignore PycodestyleBear (E501)
                package_name,
                [entry["version_specified"] for entry in matched],
                package_version,
            )  # Ignore PycodestyleBear (E501)

        # Assign installed version.
        for entry in matched:
            entry["version_installed"] = package_version

    @staticmethod
    def _parse_artifact(line: str) -> typing.Optional[dict]:
        match_result = _RE_DOWNLOADING_ARTIFACT.fullmatch(line)
        if not match_result:
            _LOG.warning("Unable to parse downloaded artifact from line %r", line)
            return None

        size = match_result.group(2)
        return {
            "name": match_result.group(1),
            # Omit braces and preceding space.
            "size": size[2:-1] if size else None,
        }

    @staticmethod
    def _remove_escape_seq(line: str) -> str:
        """Remove escape characters that can occur on stdout (e.g. colored output)."""  # Ignore PycodestyleBear (E501)
        # TODO: move to some utils module
        return _RE_ESCAPE_SEQ.sub("", line)

    def run(self, input_text: str) -> list:
        """Find and parse installed packages and their versions from a build log."""  # Ignore PycodestyleBear (E501)
        result = []
        index = 0
        lines = input_text.split("\n")
        while index < len(lines):
            line = self._remove_escape_seq(lines[index])
            match_result = _RE_COLLECTING_DEPENDENCY_FROM.fullmatch(line)
            if match_result:
                dependency = self._parse_package(match_result.group(1))
                dependency["from"] = self._parse_package(match_result.group(2), is_from=True)
                dependency["artifact"] = self._parse_artifact(lines[index + 1])
                result.append(dependency)
                index += 1
                continue

            match_result = _RE_COLLECTING_DEPENDENCY.fullmatch(line)
            if match_result:
                dependency = self._parse_package(match_result.group(1))
                dependency["from"] = None
                dependency["artifact"] = self._parse_artifact(lines[index + 1])
                result.append(dependency)
                index += 1
                continue

            match_result = _RE_ALREADY_SATISFIED.fullmatch(line)
            if match_result:
                dependency = self._parse_package(match_result.group(1))
                dependency["from"] = self._parse_package(match_result.group(3), is_from=True)
                dependency["already_satisfied"] = match_result.group(2)
                result.append(dependency)

            match_result = _RE_COLLECTING_DEPENDENCY_REMOTE.fullmatch(line)
            if match_result:
                dependency = self._parse_package(match_result.group(1))
                dependency["artifact"] = self._parse_artifact(lines[index + 1])
                # The 'from' part is not reported - it looks
                # same as dependency['artifact']['name'].
                result.append(dependency)
                index += 1
                continue

            if line.startswith("Successfully installed "):
                packages = line[len("Successfully installed ") :].split(" ")  # Ignore PycodestyleBear (E203)
                for package in packages:
                    package_name, version = package.rsplit("-", maxsplit=1)
                    self._check_entry(result, package_name, version)
                index += 1
                continue

            index += 1

        return result


HandlerBase.register(PIP3)
