# from pingvest import assets
# from pingvest import detection
# from pingvest.utils import notify
#
#
# def detect(asset, strategy, query, interval='30min'):
#     det = detection.make(strategy)
#     exc = assets.make(asset, query, interval)
#     alerts = det.detect(exc)
#     if alerts:
#         notify(
#             title=F"{asset} alert! {query}",
#             text=F"high fluctuations in value at : {' '.join(str(exc.keys[i]) for i in alerts)}"
#         )
