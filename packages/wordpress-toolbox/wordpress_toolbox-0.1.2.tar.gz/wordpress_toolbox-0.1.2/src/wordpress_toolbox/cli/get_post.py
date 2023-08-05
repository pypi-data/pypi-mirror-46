import click

from ..utils import make_request, make_url, read_credentials
from ..settings import POSTS_SUFFIX


@click.command()
@click.argument("id")
@click.pass_obj
def get_post(options, id):
    headers = {}
    click.echo(make_request(
        method="get",
        url=make_url(options.url, POSTS_SUFFIX, id),
        timeout=options.timeout,
        headers=headers,
    ))
