from pingvest.pipe import *


class NaiveDetector:

    def __init__(self, collector):
        self.collector = collector
        self.collector.get()

    def detect(self):
        return stats.outliers(
            self.collector.process()
        )


def detect(topic, query, interval):
    exc = StockExchange(query=query, interval=interval)
    det = NaiveDetector(collector=exc)
    alerts = det.detect()
    if alerts:
        notify(
            title=F"{topic.upper()} Exchange Alert! {query}",
            text=F"high fluctuations in value at : {' '.join(str(exc.keys[i]) for i in alerts)}"
        )
