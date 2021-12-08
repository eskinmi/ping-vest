import click
import detect


@click.command()
@click.option("--asset", default='stock')
@click.option("--strategy", default='naive')
@click.option("--query", default='ASML')
@click.option("--interval", default='30min')
def cli(asset, strategy, query, interval):
    detect.detect(asset, strategy, query, interval)


if __name__ == "__main__":
    cli()
