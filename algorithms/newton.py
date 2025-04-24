import time
from collections import defaultdict
from fractions import Fraction

class NewtonInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = [Fraction(x) for x in x_vals]
        self.y_vals = [Fraction(y) for y in y_vals]
        self.divided_diffs = self._compute_divided_differences()

        start_time = time.perf_counter()
        self.polynomial_expression = self.compute_polynomial_expression()
        end_time = time.perf_counter()
        self.interpolation_time = end_time - start_time

    def _compute_divided_differences(self):
        n = len(self.x_vals)
        table = [[Fraction(0) for _ in range(n)] for _ in range(n)]

        for i in range(n):
            table[i][0] = self.y_vals[i]

        for j in range(1, n):
            for i in range(n - j):
                numerator = table[i + 1][j - 1] - table[i][j - 1]
                denominator = self.x_vals[i + j] - self.x_vals[i]
                table[i][j] = numerator / denominator

        return [table[0][j] for j in range(n)]

    def interpolate(self, x):
        result = self.divided_diffs[0]
        term = 1.0
        for i in range(1, len(self.divided_diffs)):
            term *= (x - self.x_vals[i - 1])
            result += self.divided_diffs[i] * term
        return result

    def compute_polynomial_expression(self):
        superscript_map = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

        def to_superscript(n):
            return str(n).translate(superscript_map)

        def format_fraction_unicode(frac):
            if frac.denominator == 1:
                return f"{frac.numerator}"
            return f"{frac.numerator}/{frac.denominator}"

        expression_terms = []
        for i, coeff in enumerate(self.divided_diffs):
            if coeff == 0:
                continue
            sign = "-" if coeff < 0 else "+"
            abs_coeff = abs(coeff)
            coeff_str = format_fraction_unicode(abs_coeff) if abs_coeff != 1 or i == 0 else ""

            term = coeff_str
            for j in range(i):
                xj = self.x_vals[j]
                term += f"(x - {format_fraction_unicode(xj)})"

            expression_terms.append((sign, term))

        if not expression_terms:
            return "N(x) = 0"

        result = expression_terms[0][1] if expression_terms[0][0] == "+" else f"-{expression_terms[0][1]}"
        for sign, term in expression_terms[1:]:
            result += f" {sign} {term}"

        return f"N(x) = {result}"

    def get_polynomial_expression(self):
        return self.polynomial_expression

    def get_interpolation_time(self):
        return self.interpolation_time
