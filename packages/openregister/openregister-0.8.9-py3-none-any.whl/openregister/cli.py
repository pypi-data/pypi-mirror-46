import click
from click_default_group import DefaultGroup
from .server import RegisterServer


@click.group(cls=DefaultGroup, default="serve", default_if_no_args=True)
@click.version_option()
def cli():
    """
    OpenRegister:  publishing tools for GOV.UK style registers.
    """


@cli.command()
@click.option(
    "-h", "--host", default="127.0.0.1", help="host for server, defaults to 127.0.0.1"
)
@click.option(
    "-r",
    "--register",
    default=None,
    help="Serve a single register, otherwise serve all know registers as a catalog",
)
@click.option("-p", "--port", default=8088, help="port for server, defaults to 8088")
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="More verbose logging and automatically reload on changes",
)
def serve(host, port, debug, register):

    server = RegisterServer(config=None, register=register)

    click.echo("Serving on port {}".format(port))

    server.server().run(host=host, port=port, debug=debug)
