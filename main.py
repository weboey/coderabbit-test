from simple_utils import celsius_to_fahrenheit

if __name__ == "__main__":
    celsius = 25
    if not isinstance(celsius, (int, float)):
        raise TypeError("celsius must be a number")
    fahrenheit = celsius_to_fahrenheit(celsius)
    print(f"{celsius}°C = {fahrenheit}°F")