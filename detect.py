from pingvest.pipe import *


def serve_unit(topic, query, interval):
    if topic == 'fx':
        exc = ForeignExchange(query, interval)
    elif topic == 'sx':
        exc = StockExchange(query, interval)
    else:
        raise ValueError('topic should be one of the following : sx, fx')
    exc.get()
    series = exc.process()
    outliers = stats.outliers(series, 3)
    # FIND DATES OF OUTLIERS
    if outliers:
        notify(
            title=F"{topic.upper()} Exchange Alert! {query}",
            text=F"high fluctuations in value at : {' '.join(str(exc.keys[i]) for i in outliers)}"
        )

