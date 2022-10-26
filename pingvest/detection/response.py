import datetime as dt
from typing import List


NEGATIVE_COMMON_MESSAGE_TEMPLATE = """
*PingVest Detection*
--------------------

SYMBOL: {sym}
{detector_name}:
    NOTHING IS DETECTED!

"""


POSITIVE_COMMON_MESSAGE_TEMPLATE = """
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
            self.message = NEGATIVE_COMMON_MESSAGE_TEMPLATE.format(
                sym=self.sym,
                detector_name=' '.join(i.upper() for i in self.strategy.split('-')),
            )
        else:
            self.message = POSITIVE_COMMON_MESSAGE_TEMPLATE.format(
                sym=self.sym,
                detector_name=' '.join(i.upper() for i in self.strategy.split('-')),
                detected_prices_with_timestamps='\n\t' + '\n\t'.join(F'{str(t)} : {str(p)}' for t, p in zip(self.timestamps, self.prices))
            )

    def __repr__(self):
        return F"DetectionResponse({self.rb} ,{self.strategy})"

    def save_txt(self, path):
        file = open(path, "a")
        file.write('\n' + self.message)
        file.close()


def save_response_to_txt(response, path):
    file = open(path, "a")
    file.write('\n' + response.message)
    file.close()