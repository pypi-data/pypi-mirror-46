import click


@click.group()
def bash():
    """Bash Utilities."""
    pass


@click.group()
def odoo():
    """Odoo Utilities."""
    pass


@click.group()
def git():
    """Git Utilities."""
    pass
