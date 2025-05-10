import click
from .monitor import run_monitor

VERSION = "0.1.1"

@click.group()
def cli():
    """Uptime Monitor CLI Tool"""
    pass


@cli.command()
def start():
    """Start the uptime monitor service."""
    run_monitor()


@cli.command()
def version():
    """Display the version."""
    click.echo(f"Uptime Monitor version {VERSION}")


def main():
    cli()


if __name__ == "__main__":
    main()
