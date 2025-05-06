from utils.string_manipulation import to_digit_subscript

def validate_data(x_vals, y_vals):
    if not x_vals or not y_vals:
        return False, "Please enter some data points."

    for i, x1 in enumerate(x_vals):
        for j, x2 in enumerate(x_vals):
            if i != j and x1 == x2:
                return False, f"Duplicate x-values: x₍{to_digit_subscript(i+1)}₎ and x₍{to_digit_subscript(j+1)}₎ = {x1}"

    return True, ""
