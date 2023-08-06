"""
Kirin CLI.
"""
import yaml
import os
from datetime import date

__version__ = "0.0.1"

RELEASE_TYPES = ["major", "minor", "patch", "docs", "inf"]


def read_release_notes():
    """Read release notes YAML file."""
    with open("release.yaml", "r+") as f:
        notes = yaml.load(f)

    if notes["release_type"] not in RELEASE_TYPES:
        raise ValueError(f"Release type must be one of {RELEASE_TYPES}.")

    if notes["release_description"] is None:
        raise ValueError(f"Release notes must be specified.")

    return notes


def read_changelog():
    """Read changelog YAML file."""
    with open("changelog.yaml", "r+") as f:
        return yaml.load(f)


def write_changelog(data):
    """Write data to changelog."""
    with open("changelog.yaml", "w+") as f:
        yaml.dump(data, f, default_flow_style=False)


def append_release_notes():
    """Append release notes to changelog."""
    changelog = read_changelog()
    release_notes = read_release_notes()
    release_notes["date"] = date.today()
    changelog.append(release_notes)
    changelog = sorted(changelog, key=lambda x: x["date"], reverse=True)
    return changelog


def remove_release_notes():
    """Removes release notes from disk."""
    os.remove("release.yaml")
