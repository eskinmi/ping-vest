import datetime as dt
from typing import List


NEGATIVE_MESSAGE_TEMPLATE = """
*PingVest Detection*
--------------------

SYMBOL: {sym}
{detector_name}:
    NOTHING IS DETECTED!

"""


POSITIVE_MESSAGE_TEMPLATE = """
*PingVest Detection*
--------------------
            
SYMBOL: {sym}
{detector_name}:
{detected_prices_with_timestamps}

"""


class DetectionResponse:

    def __init__(self,
                 sym: str,
                 strategy: str,
                 rb: bool,
                 prices: List[float],
                 timestamps: str = List[dt.time]
                 ):
        self.sym = sym
        self.strategy = strategy
        self.rb = rb
        self.prices = prices
        self.timestamps = timestamps
        if not self.rb:
            self.message = NEGATIVE_MESSAGE_TEMPLATE.format(
                sym=self.sym,
                detector_name=' '.join(i.upper() for i in self.strategy.split('-')),
            )
        else:
            self.message = POSITIVE_MESSAGE_TEMPLATE.format(
                sym=self.sym,
                detector_name=' '.join(i.upper() for i in self.strategy.split('-')),
                detected_prices_with_timestamps='\n\t' + '\n\t'.join(F'{str(t)} : {str(p)}' for t, p in zip(self.timestamps, self.prices))
            )

    def __repr__(self):
        return F"DetectionResponse({self.rb} ,{self.strategy})"

    def save(self, path):
        file = open(path, "a")
        file.write('\n' + self.message)
        file.close()
