import click

from ..settings import DEFAULT_TIMEOUT

from .create_post import create_post
from .get_posts import get_posts
from .get_post import get_post
from .add_post import add_post
from .authenticate import authenticate
from .options import Options


@click.group()
@click.option("--url")
@click.option("--timeout", default=DEFAULT_TIMEOUT, required=False)
@click.pass_context
def main(ctx, url, timeout):
    ctx.obj = Options(url, timeout)


main.add_command(get_post)
main.add_command(get_posts)
main.add_command(create_post)
main.add_command(add_post)
main.add_command(authenticate)


if __name__ == "__main__":
    main()
