import time
from fractions import Fraction

class BarycentricInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = [Fraction(x) for x in x_vals]
        self.y_vals = [Fraction(y) for y in y_vals]
        self.n = len(x_vals)
        self.weights = self._compute_weights()

        start_time = time.perf_counter()
        self.coeffs = self._compute_polynomial_coeffs()
        self.polynomial_expression = self._format_polynomial_expression()
        end_time = time.perf_counter()
        self.interpolation_time = end_time - start_time

    def _compute_weights(self):
        w = [Fraction(1) for _ in range(self.n)]
        for j in range(self.n):
            for k in range(self.n):
                if j != k:
                    w[j] /= (self.x_vals[j] - self.x_vals[k])
        return w

    def interpolate(self, x):
        x = Fraction(x)
        numerator = Fraction(0)
        denominator = Fraction(0)
        for j in range(self.n):
            if x == self.x_vals[j]:
                return self.y_vals[j]
            temp = self.weights[j] / (x - self.x_vals[j])
            numerator += temp * self.y_vals[j]
            denominator += temp
        return numerator / denominator if denominator != 0 else 0

    def _compute_polynomial_coeffs(self):
        poly = [Fraction(0) for _ in range(self.n)]

        for j in range(self.n):
            term_poly = [Fraction(1)]
            for m in range(self.n):
                if m != j:
                    new_term = [Fraction(0)] * (len(term_poly) + 1)
                    for i in range(len(term_poly)):
                        new_term[i] -= term_poly[i] * self.x_vals[m]
                        new_term[i + 1] += term_poly[i]
                    term_poly = new_term

            weight_y = self.weights[j] * self.y_vals[j]
            for i in range(len(term_poly)):
                poly[i] += weight_y * term_poly[i]

        return poly

    def _format_polynomial_expression(self):
        def format_fraction(f):
            return f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)

        def superscript(n):
            superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
            return "".join(superscripts[int(d)] for d in str(n))

        terms = []
        degree = len(self.coeffs) - 1
        for i in range(degree, -1, -1):
            coeff = self.coeffs[i]
            if coeff == 0:
                continue

            sign = " + " if coeff > 0 and terms else (" - " if coeff < 0 else "")
            coeff_abs = abs(coeff)
            coeff_str = "" if coeff_abs == 1 and i != 0 else format_fraction(coeff_abs)

            if i == 0:
                term = f"{coeff_str}"
            elif i == 1:
                term = f"{coeff_str}x" if coeff_str else "x"
            else:
                term = f"{coeff_str}x{superscript(i)}" if coeff_str else f"x{superscript(i)}"

            terms.append(f"{sign}{term}")

        return "B(x) = " + "".join(terms)

    def get_polynomial_expression(self):
        return self.polynomial_expression

    def get_interpolation_time(self):
        return self.interpolation_time
