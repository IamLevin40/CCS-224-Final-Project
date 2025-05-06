import time
from fractions import Fraction
from sympy import symbols, expand, Rational, Poly
from utils.string_manipulation import to_digit_superscript

class BarycentricInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = [Fraction(x) for x in x_vals]
        self.y_vals = [Fraction(y) for y in y_vals]
        self.n = len(x_vals)
        self.weights = self._compute_weights()
        self.interpolation_eval_time = 0

        start_time = time.perf_counter()
        self.coeffs = self._compute_polynomial_coeffs()
        self.polynomial_expression = self._format_polynomial_expression()
        end_time = time.perf_counter()
        self.construction_time = end_time - start_time

    def _compute_weights(self):
        w = [Fraction(1) for _ in range(self.n)]
        for j in range(self.n):
            for k in range(self.n):
                if j != k:
                    diff = self.x_vals[j] - self.x_vals[k]
                    if diff == 0:
                        raise ZeroDivisionError("Duplicate x-values encountered.")
                    w[j] /= diff
        return w

    def interpolate(self, x):
        start = time.perf_counter()
        
        x = Fraction(x)
        numerator = 0.0
        denominator = 0.0
        for j in range(self.n):
            if x == self.x_vals[j]:
                return self.y_vals[j]
            temp = self.weights[j] / (x - self.x_vals[j])
            numerator += temp * self.y_vals[j]
            denominator += temp

        end = time.perf_counter()
        self.interpolation_eval_time += end - start

        return numerator / denominator if denominator != 0 else 0.0

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
        x = symbols("x")
        degree = len(self.coeffs) - 1
        poly_expr = sum(Rational(coeff.numerator, coeff.denominator) * x**i for i, coeff in enumerate(self.coeffs))
        poly_expr = expand(poly_expr)

        def to_unicode_poly_string(poly):
            def frac_to_str(r):
                r = Rational(r).limit_denominator()
                return f"{r.numerator}" if r.denominator == 1 else f"{r.numerator}/{r.denominator}"

            terms = []
            poly = Poly(poly, x)
            coeffs = poly.all_coeffs()
            deg = len(coeffs) - 1

            for i, coeff in enumerate(coeffs):
                power = deg - i
                frac = Rational(coeff).limit_denominator()
                if frac == 0:
                    continue
                sign = "-" if frac < 0 else "+"
                abs_frac = abs(frac)
                coeff_str = frac_to_str(abs_frac)

                if abs_frac == 1 and power != 0:
                    coeff_str = ""

                if power == 0:
                    term = f"{coeff_str}"
                elif power == 1:
                    term = f"{coeff_str}x"
                else:
                    term = f"{coeff_str}x{to_digit_superscript(power)}"

                terms.append((sign, term))

            if not terms:
                return "0"

            result = terms[0][1] if terms[0][0] == "+" else f"-{terms[0][1]}"
            for sign, term in terms[1:]:
                result += f" {sign} {term}"

            return result

        return f"B(x) = {to_unicode_poly_string(poly_expr)}"

    def get_numerical_stability(self, perturbation=1e-5, num_samples=1000):
        perturbed_y_vals = [y + Fraction(perturbation) for y in self.y_vals]
        perturbed_interpolator = BarycentricInterpolator(self.x_vals, perturbed_y_vals)

        min_x = float(min(self.x_vals))
        max_x = float(max(self.x_vals))
        if len(self.x_vals) == 1:
            return 0.0

        max_relative_error = 0.0
        for i in range(num_samples):
            x_sample = min_x + i * (max_x - min_x) / (num_samples - 1)
            orig_val = float(self.interpolate(x_sample))
            perturbed_val = float(perturbed_interpolator.interpolate(x_sample))

            if orig_val != 0:
                rel_error = abs((perturbed_val - orig_val) / orig_val)
            else:
                rel_error = abs(perturbed_val - orig_val)

            max_relative_error = max(max_relative_error, rel_error)

        return max_relative_error

    def get_polynomial_expression(self):
        return self.polynomial_expression

    def get_interpolation_time(self):
        return self.construction_time + self.interpolation_eval_time
