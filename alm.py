from typing import List
import typer
from dataclasses import dataclass
import re


@dataclass
class Alias:
    id: int = 0
    alias: str = ""
    command: str = ""
    description: str = ""
    tags: list = List[str]


# class Profile:
#     pass

# class Config:
#     pass


class AliasManager:
    def __init__(self) -> None:
        pass

    def readAliasFile(self, filepath: str) -> List[Alias]:
        """This function takes in a filepath, iterates through
        the file, and loads each alias string into an Alias
        object that is then added to a list and returned"""

        alias_list = []

        with open(filepath) as file:
            for line in file.readlines():
                try:
                    alias = self.unmarshalAlias(line)
                    alias_list.append(alias)
                    # self.printAlias(alias)
                except:
                    break

        return alias_list

    def unmarshalAlias(self, alias_str: str) -> Alias:
        """This Function unmarshals a string in alias file format and builds
        up an Alias Object and returns it"""

        try:

            alias_regex = re.compile(
                "^alias (?P<alias>\w*)='(?P<command>.*)' # (?P<id>\d*); (?P<description>.*); (?P<tags>.*)$"
            )
            result = alias_regex.match(alias_str)

            tags = result.group("tags").replace(" ", "").split(",")

            alias = Alias(
                id=result.group("id"),
                alias=result.group("alias"),
                command=result.group("command"),
                description=result.group("description"),
                tags=tags,
            )

            return alias

        except Exception as e:
            typer.echo(
                f"There was a problem with reading the aliases file. Error:\n{e}"
            )
            raise e

    def printAlias(self, alias: Alias) -> None:
        """This function pretty-prints an alias object to the console"""
        alias_print = f"alias: {alias.alias}\ncommand: {alias.command}\ndescription: {alias.description}\ntags: {alias.tags}"
        typer.echo(alias_print)


main = typer.Typer(help="Superpower Alias Management for the Modern Developer")


@main.command()
def enable(alias: str):
    typer.echo(f'"{alias}" has been enabled')


@main.command()
def disable(alias: str):
    typer.echo(f'"{alias}" has been disabled')


@main.command()
def list(tag: str = None, filename: str = "alm_aliases"):
    # typer.echo(filename)
    manager = AliasManager()
    alias_list = manager.readAliasFile(filepath=filename)

    if tag:
        for alias in alias_list:
            typer.echo(alias.tags)
            if tag in alias.tags:
                manager.printAlias(alias)

    else:
        for alias in alias_list:
            manager.printAlias(alias=alias)


if __name__ == "__main__":
    main()
