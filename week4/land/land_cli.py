from rectangular_land import RectangularLand


def prompt_positive_float(message: str) -> float:
    while True:
        raw = input(message).strip()
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if value <= 0:
            print("Please enter a number greater than 0.")
            continue
        return value


def main() -> None:
    print("=== Rectangular Land Calculator ===")
    length = prompt_positive_float("Enter the land length: ")
    width = prompt_positive_float("Enter the land width: ")

    land = RectangularLand(length=length, width=width)
    print(f"Area: {land.area()}")
    print(f"Perimeter: {land.perimeter()}")


if __name__ == "__main__":
    main()
