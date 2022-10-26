# pingvest

PingVest is an application for users who would like to get notified about the stocks and forex that they have interest in.
It implements multiple strategies to detect the type of strategy user needs to get notified, e.g.:
* price hit
* trend anomaly
* dip / peak prices

PingVest uses [alphavantage](https://www.alphavantage.co/documentation/) API resources to collect data in different intervals and analyzes it.
This project is written using `python=3.8`. 

## usage

There are two main assets; forex and stock. In order to run the app one can take the following steps:

* get your alphavantage api key
* save the api key to the root directory, with name: `alphavantage_apikey.txt`
* add your run configurations on `app_config.json` file.
* install poetry: `pip install poetry` 
* install dependencies: `poetry install`

To run the app:

#### Terminal:

Running with given configurations in `app_config.json`: 

```cli
python app.py 
```

Or if you haven't installed the dependencies yet:

```cli
poetry run python app.py
```

## modules

### assets

For specific assets:

```py
from pingvest.api.assets import StockExchangeDaily

asset = StockExchangeDaily(query='ASML')
asset.get()
```

For generic asset loader:

```py
from pingvest.api.assets import AssetLoader

asset_loader = AssetLoader()
asset_params = {}
asset = asset_loader.get(
    sym='ASML',
    asset_type='stock-intraday',
    **asset_params
)
```
### detectors

For a specific detector:

```py
from pingvest.detection.strategy.peakdip import peak_detector

asset = ...

peak_detector(
    asset.data,
    asset.data_keys,
    w=3,
    quant=0.05
)
```

### pipeline

```py

from pingvest.api.assets import AssetLoader
from pingvest.detection.strategy.peakdip import peak_detector
from pingvest.detection.response import save_response_to_txt

asset_loader = AssetLoader()
asset_params = {'interval': '30min'}
asset = asset_loader.get(
    sym='ASML',
    asset_type='stock-intraday',
    **asset_params
)

asset.get()

response = peak_detector(
    asset.data,
    asset.data_keys,
    w=3,
    quant=0.05
)

msg = response.message

save_response_to_txt(response, './responses.txt')
```