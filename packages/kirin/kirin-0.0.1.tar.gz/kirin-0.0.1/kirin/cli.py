import click
from .__init__ import (
    append_release_notes,
    remove_release_notes,
    write_changelog,
    read_release_notes,
)
import os


@click.group()
def main():
    pass


@main.command()
def bumpversion():
    notes = read_release_notes()
    print(notes['release_type'])
    os.system(f"bumpversion {notes['release_type']}")


@main.command()
def update_changelog():
    data = append_release_notes()
    write_changelog(data)
    remove_release_notes()


@main.command()
def release():
    os.system("mkdir -p dist/")
    os.system("rm dist/*")
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")


if __name__ == "__main__":
    main()
