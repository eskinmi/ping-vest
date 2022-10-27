import pytest
import click
import sys
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler

from pingvest.utils import read_json
from pingvest.api.assets import AssetLoader
from pingvest.detection.detector import Detector
from pingvest.detection.response import save_response_to_txt


def _set_logger():
    log = logging.getLogger('app')
    log.setLevel(logging.DEBUG)
    fh = RotatingFileHandler('./logs.txt')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log


def _clean_output_content(path):
    f = open(path, 'r+')
    f.truncate(0)
    f.close()


def run_pipe(configs,
             out_path: str,
             include_negative_responses: bool = False,
             notify: bool = False
             ):
    asset_loader = AssetLoader()
    for config in configs:
        for strategy, run_configs in config.items():

            sym = run_configs['asset']
            asset_type = run_configs['asset_type']
            asset_params = run_configs.get('asset_params', {})

            asset = asset_loader.get(
                sym,
                asset_type,
                **asset_params
            )

            detector = Detector(sym=sym, name=strategy)
            response = detector.detect(
                asset.data,
                asset.data_keys,
                run_configs['params']
            )

            if include_negative_responses or response.rb:
                save_response_to_txt(
                    response,
                    out_path
                )
                if notify:
                    raise NotImplementedError


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    if debug:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)
        logger.addHandler(sh)


@cli.command()
@click.option("--save_path", default='./responses.txt')
@click.option("--conf_path", default='./app_config.json')
@click.pass_context
def run(ctx, save_path, conf_path):
    if ctx.obj['DEBUG']:
        click.echo('running ping-vest pipeline.')
    _clean_output_content(save_path)
    run_configurations = read_json(conf_path)
    if run_configurations:
        run_pipe(run_configurations, save_path)


@cli.command()
@click.pass_context
def run_tests(ctx):
    if ctx.obj['DEBUG']:
        click.echo('running ping-vest tests.')
    pytest.main(["tests"])


if __name__ == "__main__":
    logger = _set_logger()
    cli(obj={})
