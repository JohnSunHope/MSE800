from __future__ import annotations


class RectangularLand:
    def __init__(self, length: float, width: float) -> None:
        if length <= 0 or width <= 0:
            raise ValueError("Length and width must be positive numbers.")
        self.length = float(length)
        self.width = float(width)

    def area(self) -> float:
        return self.length * self.width

    def perimeter(self) -> float:
        return 2 * (self.length + self.width)
