#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Check the FIX Trading Community's repositories against the editions the schema models.

The schema models SBE 1.0 at a tag and SBE 2.0 RC3 at a commit, because no tag names RC3.
upstream/ holds those files and the conformance suite's schemas unchanged. These things can
change without any change in this repository:

- a new tag appears, or a new edition folder such as v2-0-STANDARD;
- a pinned tag moves, or a pinned file changes or goes, at the pinned place or on the
  default branch;
- a licence file on the default branch changes.

The script lists the repositories' trees through GitHub's API and compares git object hashes,
so it downloads no file. It reads nothing from fixtrading.org, whose terms bar automated
copying. scripts/upstream_pins.tsv holds each file's hash. The script prints a Markdown report
and exits 1 on any of the above, or when a check could not finish.

Text a server chose is quoted as code on one line in the report, so the issue the workflow
opens from it cannot mention anyone. A redirect is followed only to an https address on
api.github.com. Set ``GITHUB_TOKEN`` to raise the API's rate limit. Usage::

    python scripts/check_upstream_release.py [--report FILE]
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PINS = ROOT / "scripts" / "upstream_pins.tsv"
USER_AGENT = "lmodel-fix-sbe-upstream-check"
API = "https://api.github.com/repos/FIXTradingCommunity"
HOST = "api.github.com"

# The most the script reads of one answer. A recursive listing of a repository is about 1 MB.
MAX_BYTES = 20_000_000

SPEC = "fix-simple-binary-encoding"
SUITE = "fix-sbe-conformance"
BRANCH = "master"

# What the schema models. tests/test_upstream.py holds the schema headers and these pins
# equal. Move them together, with upstream/ and scripts/upstream_pins.tsv, for another edition.
V1_EDITION = "1.0"
V1_TAG = "v1.0-errata-Nov-2020"
V1_COMMIT = "6321e6b9bce5bc198f88f462054cbaf4f33d8f60"
V1_FOLDER = "v1-0-STANDARD"
V2_EDITION = "2.0-rc3"
V2_COMMIT = "418a8f6a8b93c65b308638dab2bc6a35dddcd864"
V2_FOLDER = "v2-0-RC3"
SUITE_TAG = "v1.0"
SUITE_COMMIT = "64558fbf331d7f1f4ff6bd297fbcdc466299f482"

# Everything the specification's repository held when the pins were read, so anything new
# stands out. The folder pattern finds an edition however it is spelled.
KNOWN_TAGS = ("v1.0", "v1.0-RC4", "v1.0-errata-Nov-2020", "v2.0-rc2")
KNOWN_FOLDERS = (
    "v1-0-RC1",
    "v1-0-RC2",
    "v1-0-RC3",
    "v1-0-RC4",
    "v1-0-STANDARD",
    "v2-0-RC1",
    "v2-0-RC2",
    "v2-0-RC3",
)
EDITION_FOLDER = re.compile(r"^v\d+-\d+-")


class _ApiRedirect(urllib.request.HTTPRedirectHandler):
    """Follow a redirect only to an https address on the API's host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parts = urllib.parse.urlsplit(newurl)
        if parts.scheme != "https" or parts.hostname != HOST:
            raise ValueError(f"a redirect leads off {HOST}, to {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


# An opener in place of urlopen's, whose redirect handler follows any address.
_open = urllib.request.build_opener(_ApiRedirect).open


def _get(path: str):
    """The JSON answer to one API path, read up to the cap."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{API}{path}", headers=headers)
    with _open(req, timeout=60) as resp:
        body = resp.read(MAX_BYTES + 1)
    if len(body) > MAX_BYTES:
        raise ValueError(f"the answer to {path} is larger than {MAX_BYTES} bytes")
    return json.loads(body)


def _code(text: object) -> str:
    """Text a server chose, as a code span on one line, so it cannot mention a person or add a
    link in the issue. A blank line would end the span, so every run of spaces and line breaks
    is one space."""
    return "`" + " ".join(str(text).replace("`", "'").split()) + "`"


def pins() -> dict[str, str]:
    """Each pinned path, under its repository's name, and its git object hash."""
    rows = (line.split("\t") for line in PINS.read_text(encoding="utf-8").splitlines())
    return {path: sha for path, sha in rows}


def _pins_of(repository: str) -> dict[str, str]:
    """The pins of one repository, by the path inside it."""
    prefix = f"{repository}/"
    return {
        path.removeprefix(prefix): sha
        for path, sha in pins().items()
        if path.startswith(prefix)
    }


def _blobs(repository: str, ref: str) -> dict[str, str]:
    """Each file of a repository at a ref. A listing GitHub cuts short cannot be compared."""
    answer = _get(f"/{repository}/git/trees/{ref}?recursive=1")
    if answer.get("truncated"):
        raise ValueError(f"GitHub cut short the listing of {repository} at {ref}")
    return {e["path"]: e["sha"] for e in answer["tree"] if e["type"] == "blob"}


def _tag_commit(repository: str, tag: str) -> str:
    """The commit a tag names, through its tag object when it has one."""
    target = _get(f"/{repository}/git/ref/tags/{tag}")["object"]
    if target["type"] == "tag":
        target = _get(f"/{repository}/git/tags/{target['sha']}")["object"]
    return target["sha"]


def _compare(found: dict[str, str], expected: dict[str, str], place: str) -> list[str]:
    """One line for each kind of difference between the pins and a listing."""
    lines = []
    gone = sorted(path for path in expected if path not in found)
    changed = sorted(
        path for path, sha in expected.items() if path in found and found[path] != sha
    )
    for label, paths in (("gone", gone), ("changed", changed)):
        if paths:
            shown = ", ".join(_code(path) for path in paths)
            lines.append(f"- **{len(paths)} pinned files {label} {place}:** {shown}.")
    return lines


def check_editions() -> tuple[list[str], bool]:
    """Report any tag or edition folder the pins did not know."""
    tags = {entry["name"] for entry in _get(f"/{SPEC}/tags?per_page=100")}
    root = _get(f"/{SPEC}/git/trees/{BRANCH}")["tree"]
    folders = {
        entry["path"]
        for entry in root
        if entry["type"] == "tree" and EDITION_FOLDER.match(entry["path"])
    }
    lines = []
    new_tags = sorted(tags - set(KNOWN_TAGS))
    new_folders = sorted(folders - set(KNOWN_FOLDERS))
    if new_tags:
        shown = ", ".join(_code(tag) for tag in new_tags)
        lines.append(f"- **New tags in the specification's repository:** {shown}.")
    if new_folders:
        shown = ", ".join(_code(folder) for folder in new_folders)
        lines.append(f"- **New edition folders:** {shown}.")
    if lines:
        lines.append(
            "- Read what changed, decide whether the schema moves to it, and move upstream/, "
            "the pins and the schema headers together."
        )
        return lines, True
    return ["- No new tag or edition folder in the specification's repository."], False


def check_v1() -> tuple[list[str], bool]:
    """Report whether SBE 1.0's tag still names the pinned commit and files."""
    commit = _tag_commit(SPEC, V1_TAG)
    lines = []
    if commit != V1_COMMIT:
        lines.append(
            f"- **The tag {V1_TAG} moved to {_code(commit)}.** Find out why a published "
            "edition moved before trusting the copy in upstream/."
        )
    expected = {
        path: sha
        for path, sha in _pins_of(SPEC).items()
        if path.startswith(f"{V1_FOLDER}/")
    }
    lines += _compare(_blobs(SPEC, commit), expected, f"at {V1_TAG}")
    lines += _compare(_blobs(SPEC, BRANCH), expected, f"on {BRANCH}")
    if lines:
        return lines, True
    return [f"- SBE {V1_EDITION}'s {len(expected)} pinned files are unchanged."], False


def check_v2() -> tuple[list[str], bool]:
    """Report whether SBE 2.0 RC3's files are the pinned ones, on the branch and the commit."""
    expected = {
        path: sha
        for path, sha in _pins_of(SPEC).items()
        if path.startswith(f"{V2_FOLDER}/")
    }
    lines = _compare(_blobs(SPEC, V2_COMMIT), expected, f"at {V2_COMMIT[:7]}")
    lines += _compare(_blobs(SPEC, BRANCH), expected, f"on {BRANCH}")
    if lines:
        return lines, True
    return [f"- SBE {V2_EDITION}'s {len(expected)} pinned files are unchanged."], False


def check_suite() -> tuple[list[str], bool]:
    """Report whether the conformance suite's tag still names the pinned commit and files."""
    commit = _tag_commit(SUITE, SUITE_TAG)
    lines = []
    if commit != SUITE_COMMIT:
        lines.append(f"- **The suite's tag {SUITE_TAG} moved to {_code(commit)}.**")
    expected = {path: sha for path, sha in _pins_of(SUITE).items() if path != "LICENSE"}
    lines += _compare(_blobs(SUITE, commit), expected, f"at {SUITE_TAG}")
    lines += _compare(_blobs(SUITE, BRANCH), expected, f"on {BRANCH}")
    if lines:
        return lines, True
    return [f"- The suite's {len(expected)} pinned schemas are unchanged."], False


def check_licences() -> tuple[list[str], bool]:
    """Report whether each licence on the default branch is the pinned file."""
    lines = []
    for repository in (SPEC, SUITE):
        root = {
            e["path"]: e["sha"]
            for e in _get(f"/{repository}/git/trees/{BRANCH}")["tree"]
        }
        if root.get("LICENSE") != pins()[f"{repository}/LICENSE"]:
            lines.append(
                f"- **The LICENSE of {repository} changed on the default branch.** Read what "
                "changed, and update NOTICE if the licence moved."
            )
    if lines:
        return lines, True
    return ["- Both licences on the default branch are the pinned files."], False


# Each check, by the name the report gives it when it cannot finish.
CHECKS = (
    ("new editions", check_editions),
    ("SBE 1.0", check_v1),
    ("SBE 2.0 RC3", check_v2),
    ("conformance suite", check_suite),
    ("licences", check_licences),
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--report", type=Path, help="Also write the Markdown report to this file"
    )
    args = parser.parse_args(argv)
    lines = [
        f"- Pinned editions: SBE {V1_EDITION} at {V1_TAG}, and SBE {V2_EDITION} at "
        f"{V2_COMMIT[:7]}."
    ]
    attention = False
    for label, check in CHECKS:
        try:
            found, needs = check()
        # OSError covers a refused or failed request and a timeout, HTTPException and EOFError
        # a connection cut off mid-answer, LookupError and ValueError an answer of another
        # shape or too large.
        except (
            OSError,
            http.client.HTTPException,
            EOFError,
            LookupError,
            ValueError,
        ) as err:
            found = [f"- **The {label} check could not finish: {_code(err)}.**"]
            needs = True
        lines += found
        attention = attention or needs
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    return 1 if attention else 0


if __name__ == "__main__":
    sys.exit(main())
