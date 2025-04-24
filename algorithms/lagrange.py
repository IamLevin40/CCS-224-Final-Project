import time
from collections import defaultdict
from fractions import Fraction

class LagrangeInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = [Fraction(x) for x in x_vals]
        self.y_vals = [Fraction(y) for y in y_vals]
        self.n = len(x_vals)

        start_time = time.perf_counter()
        self.polynomial_expression = self.compute_polynomial_expression()
        end_time = time.perf_counter()
        self.interpolation_time = end_time - start_time

    def _L(self, k, x):
        total = 1
        for i in range(self.n):
            if i != k:
                total *= (x - self.x_vals[i]) / (self.x_vals[k] - self.x_vals[i])
        return total

    def interpolate(self, x):
        result = 0
        for k in range(self.n):
            result += self.y_vals[k] * self._L(k, x)
        return result

    def compute_polynomial_expression(self):
        def poly_mul(p1, p2):
            result = defaultdict(Fraction)
            for deg1, coef1 in p1.items():
                for deg2, coef2 in p2.items():
                    result[deg1 + deg2] += coef1 * coef2
            return result

        final_poly = defaultdict(Fraction)

        for k in range(self.n):
            term_poly = {0: Fraction(1)}
            denom = Fraction(1)
            for i in range(self.n):
                if i != k:
                    term_poly = poly_mul(term_poly, {1: Fraction(1), 0: -self.x_vals[i]})
                    denom *= self.x_vals[k] - self.x_vals[i]
            for deg in term_poly:
                term_poly[deg] *= self.y_vals[k] / denom
            for deg in term_poly:
                final_poly[deg] += term_poly[deg]

        superscript_map = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

        def to_superscript(n):
            return str(n).translate(superscript_map)

        def format_fraction_unicode(frac):
            if frac.denominator == 1:
                return f"{frac.numerator}"
            return f"{frac.numerator}/{frac.denominator}"

        terms = []
        for deg in sorted(final_poly.keys(), reverse=True):
            coef = final_poly[deg]
            if coef == 0:
                continue
            sign = "-" if coef < 0 else "+"
            abs_coef = abs(coef)

            if deg == 0:
                term = f"{format_fraction_unicode(abs_coef)}"
            elif deg == 1:
                coef_str = "" if abs_coef == 1 else format_fraction_unicode(abs_coef)
                term = f"{coef_str}x"
            else:
                coef_str = "" if abs_coef == 1 else format_fraction_unicode(abs_coef)
                term = f"{coef_str}x{to_superscript(deg)}"

            terms.append((sign, term))

        if not terms:
            return "L(x) = 0"

        expression = terms[0][1] if terms[0][0] == "+" else f"-{terms[0][1]}"
        for sign, term in terms[1:]:
            expression += f" {sign} {term}"

        return f"L(x) = {expression.strip()}"

    def get_polynomial_expression(self):
        return self.polynomial_expression

    def get_interpolation_time(self):
        return self.interpolation_time
