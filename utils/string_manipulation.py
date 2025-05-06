def to_digit_subscript(n: int) -> str:
    subscript_digits = str.maketrans("0123456789-", "₀₁₂₃₄₅₆₇₈₉₋")
    return str(n).translate(subscript_digits)

def to_digit_superscript(n: int) -> str:
    superscript_digits = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
    return str(n).translate(superscript_digits)