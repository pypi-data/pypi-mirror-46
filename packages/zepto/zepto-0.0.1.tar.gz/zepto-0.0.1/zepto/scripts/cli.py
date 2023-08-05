import click


dry_run = False


@click.group()
@click.option('--dry-run', is_flag=True, default=False)
def cli(**kwargs):
    global dry_run
    dry_run = kwargs['dry_run']


@cli.command()
@click.option('--stage', default='dev', show_default=True)
@click.option('--region', default='ap-southeast-1', show_default=True)
def deploy(**opts):
    if dry_run:
        click.echo('Running in dry run mode.')


if __name__ == '__main__':
    cli(obj={})
