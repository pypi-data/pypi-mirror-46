import click

from ..utils import make_url, make_request, read_credentials
from ..settings import POSTS_SUFFIX


@click.command()
@click.option("--date")
@click.option("--date_gmt")
@click.option("--slug")
@click.option("--status")
@click.option("--password")
@click.option("--title")
@click.option("--content")
@click.option("--author")
@click.option("--excerpt")
@click.option("--featured_media")
@click.option("--comment_status")
@click.option("--ping_status")
@click.option("--format")
@click.option("--meta")
@click.option("--sticky")
@click.option("--template")
@click.option("--categories")
@click.option("--tags")
@click.pass_obj
def create_post(options, date, date_gmt, slug, status, password, title,
                content, author, excerpt, featured_media, comment_status,
                ping_status, format, meta, sticky, template, categories,
                tags):
    url = make_url(options.url, POSTS_SUFFIX)
    data = {
        "url": url,
        "date": date,
        "date_gmt": date_gmt,
        "slug": slug,
        "status": status,
        "password": password,
        "title": title,
        "content": content,
        "author": author,
        "excerpt": excerpt,
        "featured_media": featured_media,
        "comment_status": comment_status,
        "ping_status": ping_status,
        "format": format,
        "meta": meta,
        "sticky": sticky,
        "template": template,
        "categories": categories,
        "tags": tags,
    }
    headers = {}
    click.echo(make_request(
        method="post",
        url=url,
        data=data,
        timeout=options.timeout,
        headers=headers,
    ))
