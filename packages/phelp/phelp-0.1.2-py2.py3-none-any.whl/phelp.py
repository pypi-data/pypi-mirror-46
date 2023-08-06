import click
from lib.search_replace import SearchReplace
from lib.search import Search


@click.group()
def cli():
    pass


@click.command()
@click.argument('search_directory')
@click.argument('search_text')
@click.argument('replace_text')
def search_replace(search_directory, search_text, replace_text):
    SearchReplace(search_directory, search_text, replace_text)


@click.command()
@click.argument('search_directory')
@click.argument('search_text')
def search(search_directory, search_text):
    Search(search_directory, search_text)


cli.add_command(search_replace)
cli.add_command(search)

if __name__ == '__main__':
    cli()
