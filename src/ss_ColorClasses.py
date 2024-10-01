from __future__ import annotations
from enum import Enum, auto as enumAuto
from src.registration import SafeGlobals

class ColorCompareMode(Enum):
    RGB = enumAuto()
    HSV = enumAuto()

@SafeGlobals.register
class PixelColor:

    def __init__(
        self,
        color : tuple[int,int,int],
        tolerance : int,
        requirement : bool
    ) -> None:

        self.color = color
        self.requirement = requirement
        self.tolerance = tolerance
        self.startPixel = 0
        self.endPixel = 0

    def __str__(self) -> str:
        return f"Color: ({self.color[0]},{self.color[1]},{self.color[2]}), startPixel: {self.startPixel}, endPixel: {self.endPixel}"

    def clearColorScanPixels(self) -> None:
        self.startPixel = None
        self.endPixel = None

    def color_cmp(self, other_color : PixelColor, mode : ColorCompareMode = ColorCompareMode.RGB, tolerance : list[int] = [0,0,0]) -> bool:

        for c in range(3):
            if self.color[c] > other_color.color[c] + tolerance[c] or self.color[c] < other_color.color[c] - tolerance[c]:
                return False
        return True