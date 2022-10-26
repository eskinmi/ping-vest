import logging
from logging.handlers import RotatingFileHandler

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
                    pass


if __name__ == "__main__":

    save_path = './responses.txt'
    conf_path = './app_config.json'

    _set_logger()
    _clean_output_content(save_path)

    run_configurations = read_json(conf_path)
    run_pipe(run_configurations, save_path)
