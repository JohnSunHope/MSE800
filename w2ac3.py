import math
from typing import Union

Numeric = Union[int, float, complex]

class AdvancedCalculator:
    """
    A class to perform advanced mathematical operations using OOP principles.
    """
    def __init__(self):
        self.history = []

    def add(self, a: Numeric, b: Numeric) -> Numeric:
        """Method 1: Performs addition, supporting complex numbers."""
        result = a + b
        self.history.append(f"Add: {a} + {b} = {result}")
        return result

    def multiply(self, a: Numeric, b: Numeric) -> Numeric:
        """Method 2: Performs multiplication, supporting complex numbers."""
        result = a * b
        self.history.append(f"Multiply: {a} * {b} = {result}")
        return result

    def factorial(self, n: int) -> int:
        """Method 3: Calculates factorial for non-negative integers."""
        if not isinstance(n, int) or n < 0:
            raise ValueError("Factorial is only defined for non-negative integers.")
        result = math.factorial(n)
        self.history.append(f"Factorial: {n}! = {result}")
        return result
    
    def clear_history(self) -> None:
        """Method 4: Clears the Sessfion calculation history."""
        self.history.clear()
        print("Session calculation history cleared.")

def format_result(label: str, result: Numeric) -> None:
    """Function 1: Formats and prints the calculation results."""
    print(f"[RESULT] {label}: {result}")

def run_calculator_demo() -> None:
    """Function 2: Main logic to demonstrate the calculator capabilities."""
    calc = AdvancedCalculator()

    res_add = calc.add(10, 5.5)
    format_result("Addition (Real)", res_add)
    
    res_complex_add = calc.add(2 + 3j, 1 - 1j)
    format_result("Addition (Complex)", res_complex_add)

    res_mul = calc.multiply(4, 2.5)
    format_result("Multiplication", res_mul)

    try:
        res_fact = calc.factorial(5)
        format_result("Factorial of 5", res_fact)
    except ValueError as e:
        print(f"Error: {e}")

    print("\n--- Session History ---")
    for entry in calc.history:
        print(f"  > {entry}")

if __name__ == "__main__":
    run_calculator_demo()
