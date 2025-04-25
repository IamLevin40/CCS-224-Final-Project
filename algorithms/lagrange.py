import time
from collections import defaultdict
from fractions import Fraction
from sympy import symbols, expand, Rational, Poly

class LagrangeInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = [Fraction(x) for x in x_vals]
        self.y_vals = [Fraction(y) for y in y_vals]
        self.n = len(x_vals)
        self.interpolation_eval_time = 0

        start_time = time.perf_counter()
        self.polynomial_expression = self._compute_polynomial_expression()
        end_time = time.perf_counter()
        self.construction_time = end_time - start_time

    def _L(self, k, x):
        total = 1
        for i in range(self.n):
            if i != k:
                total *= (x - self.x_vals[i]) / (self.x_vals[k] - self.x_vals[i])
        return total

    def interpolate(self, x):
        start = time.perf_counter()
        
        result = 0
        for k in range(self.n):
            result += self.y_vals[k] * self._L(k, x)
        
        end = time.perf_counter()
        self.interpolation_eval_time += end - start

        return result

    def _compute_polynomial_expression(self):
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

        x = symbols("x")
        poly_expr = sum(Rational(coef.numerator, coef.denominator) * x**deg for deg, coef in final_poly.items())
        poly_expr = expand(poly_expr)

        def to_unicode_poly_string(expr):
            superscript_map = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

            def frac_to_str(frac):
                return f"{frac.numerator}/{frac.denominator}" if frac.denominator != 1 else f"{frac.numerator}"

            poly = Poly(expr, x)
            coeffs = poly.all_coeffs()
            deg = len(coeffs) - 1

            terms = []
            for i, coeff in enumerate(coeffs):
                power = deg - i
                if coeff == 0:
                    continue
                sign = "-" if coeff < 0 else "+"
                abs_frac = abs(Rational(coeff))
                coeff_str = "" if abs_frac == 1 and power != 0 else frac_to_str(abs_frac)

                if power == 0:
                    term = f"{coeff_str}"
                elif power == 1:
                    term = f"{coeff_str}x" if coeff_str else "x"
                else:
                    term = f"{coeff_str}x{str(power).translate(superscript_map)}" if coeff_str else f"x{str(power).translate(superscript_map)}"

                terms.append((sign, term))

            if not terms:
                return "0"

            result = terms[0][1] if terms[0][0] == "+" else f"-{terms[0][1]}"
            for sign, term in terms[1:]:
                result += f" {sign} {term}"

            return result

        return f"L(x) = {to_unicode_poly_string(poly_expr)}"

    def get_polynomial_expression(self):
        return self.polynomial_expression

    def get_interpolation_time(self):
        return self.construction_time + self.interpolation_eval_time
