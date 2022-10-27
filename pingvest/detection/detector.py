import numpy as np
from pingvest.detection import strategy as dts
from pingvest.detection.response import DetectionResponse


class Detector:

    def __init__(self, sym: str, name: str):
        self.sym = sym
        self.name = name
        self.method = getattr(dts, name)

    def detect(self, data: np.array, timestamps: np.array, **params):
        rb, prices, times = self.method(data, timestamps, **params)
        return DetectionResponse(sym=self.sym,
                                 strategy=self.name,
                                 rb=rb,
                                 prices=prices,
                                 timestamps=times
                                 )




