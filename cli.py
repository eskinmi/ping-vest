import click
import detect


@click.command()
@click.option("--topic", default='sx')
@click.option("--query", default='ASML')
@click.option("--interval", default='60min')
def cli(topic, query, interval):
    detect.detect(topic, query, interval)


if __name__ == "__main__":
    cli()
