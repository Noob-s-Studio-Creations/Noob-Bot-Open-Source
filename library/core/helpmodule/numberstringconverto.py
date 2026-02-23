def ConverToNumberThatAbleToRead(number: int) -> str:
    units = [
        "",
        "K",
        "M",
        "B",
        "T",
        "Q",
        "Qi",
        "Sx"
    ]

    if number < 1000:
        return str(number)

    index = 0
    value = float(number)

    while value >= 1000 and index < len(units) - 1:
        value /= 1000
        index += 1

    return f"{value:.1f}{units[index]}".rstrip("0").rstrip(".")