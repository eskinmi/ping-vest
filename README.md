# pingvest

Alerting algorithm for fluctuations and strategy building (not yet
implemented) for stock / foreign exchange equities.


## example use

There are two main assets; forex and stock.

Terminal:
```cli
python cli.py --asset stock --query ASML --strategy naive --interval 15min 
```
or
```cli
python cli.py --asset forex --query EUR-TRY --strategy naive --interval 60min 
```

Console:
```py
from pingvest.assets import *
from pingvest.detector import *

det = NaiveDetector()
exc = ForeignExchange('EUR-TRY', '30min')
alerts = det.detect(exc)
```