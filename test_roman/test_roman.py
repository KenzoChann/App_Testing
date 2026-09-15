import re

import pytest


def convert(number: str) -> int:
    """Converts a Roman numeral string to an integer after validating input."""
    if not isinstance(number, str) or not number:
        raise ValueError("Input must be a non-empty string.")

    # Standardize to uppercase
    number = number.upper().strip()

    # Regex check: validates correct Roman numeral patterns and prevents illegal combinations (e.g., VV, VX, IL, XXC)
    valid_roman_pattern = (
        r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
    )
    if not re.match(valid_roman_pattern, number):
        raise ValueError(f"Invalid Roman numeral input: '{number}'")

    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    n = len(number)

    for i in range(n):
        current_val = values[number[i]]

        # Subtractive rule: subtract if next symbol is larger
        if i + 1 < n and current_val < values[number[i + 1]]:
            total -= current_val
        else:
            total += current_val

    return total


def test_single_symbols():
    assert convert("I") == 1
    assert convert("V") == 5
    assert convert("M") == 1000


def test_additive_combinations():
    assert convert("III") == 3
    assert convert("VI") == 6
    assert convert("XVI") == 16


def test_subtractive_combinations():
    assert convert("IV") == 4
    assert convert("IX") == 9
    assert convert("XL") == 40
    assert convert("XC") == 90


def test_complex_valid_inputs():
    assert convert("XIX") == 19
    assert convert("MCMXCIV") == 1994


def test_invalid_subtraction_and_repetition():
    with pytest.raises(ValueError):
        convert("VX")

    with pytest.raises(ValueError):
        convert("XXC")

    with pytest.raises(ValueError):
        convert("IIII")

    with pytest.raises(ValueError):
        convert("VV")


def test_invalid_characters():
    with pytest.raises(ValueError):
        convert("ABC")

    with pytest.raises(ValueError):
        convert("")


if __name__ == "__main__":
    print("Roman numeral converter. Press Ctrl + C to exit.")

    while True:
        try:
            roman_number = input("Enter a Roman numeral: ")
            print(convert(roman_number))
        except ValueError as error:
            print(error)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
