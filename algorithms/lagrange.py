import time
from collections import defaultdict
from sympy import symbols, expand, Poly
from utils.string_manipulation import to_digit_superscript

class LagrangeInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = [float(x) for x in x_vals]
        self.y_vals = [float(y) for y in y_vals]
        self.n = len(x_vals)
        self.interpolation_eval_time = 0

    def _L(self, k, x):
        total = 1.0
        for i in range(self.n):
            if i != k:
                total *= (x - self.x_vals[i]) / (self.x_vals[k] - self.x_vals[i])
        return total

    def interpolate(self, x):
        start = time.perf_counter()

        result = 0.0
        for k in range(self.n):
            result += self.y_vals[k] * self._L(k, x)

        end = time.perf_counter()
        self.interpolation_eval_time += end - start

        return result

    def _format_polynomial_expression(self):
        def poly_mul(p1, p2):
            result = defaultdict(float)
            for deg1, coef1 in p1.items():
                for deg2, coef2 in p2.items():
                    result[deg1 + deg2] += coef1 * coef2
            return result

        final_poly = defaultdict(float)

        for k in range(self.n):
            term_poly = {0: 1.0}
            denom = 1.0
            for i in range(self.n):
                if i != k:
                    term_poly = poly_mul(term_poly, {1: 1.0, 0: -self.x_vals[i]})
                    denom *= self.x_vals[k] - self.x_vals[i]
            for deg in term_poly:
                term_poly[deg] *= self.y_vals[k] / denom
            for deg in term_poly:
                final_poly[deg] += term_poly[deg]

        x = symbols("x")
        poly_expr = sum(coef * x**deg for deg, coef in sorted(final_poly.items()))
        poly_expr = expand(poly_expr)

        def to_unicode_poly_string(expr):
            poly = Poly(expr, x)
            coeffs = poly.all_coeffs()
            deg = len(coeffs) - 1

            terms = []
            for i, coeff in enumerate(coeffs):
                power = deg - i
                if coeff == 0:
                    continue
                sign = "-" if coeff < 0 else "+"
                abs_coeff = abs(coeff)
                coeff_str = f"{abs_coeff:.4f}".rstrip("0").rstrip(".") if abs_coeff != 1 or power == 0 else ""

                if power == 0:
                    term = f"{coeff_str}"
                elif power == 1:
                    term = f"{coeff_str}x" if coeff_str else "x"
                else:
                    term = f"{coeff_str}x{to_digit_superscript(power)}" if coeff_str else f"x{to_digit_superscript(power)}"

                terms.append((sign, term))

            if not terms:
                return "0"

            result = terms[0][1] if terms[0][0] == "+" else f"-{terms[0][1]}"
            for sign, term in terms[1:]:
                result += f" {sign} {term}"

            return result

        return f"L(x) = {to_unicode_poly_string(poly_expr)}"

    def get_numerical_stability(self, perturbation=1e-5, num_samples=1000):
        perturbed_y_vals = [y + perturbation for y in self.y_vals]
        perturbed_interpolator = LagrangeInterpolator(self.x_vals, perturbed_y_vals)

        min_x = min(self.x_vals)
        max_x = max(self.x_vals)
        if self.n == 1:
            return 0.0

        max_relative_error = 0.0
        for i in range(num_samples):
            x_sample = min_x + i * (max_x - min_x) / (num_samples - 1)
            orig_val = self.interpolate(x_sample)
            perturbed_val = perturbed_interpolator.interpolate(x_sample)

            if orig_val != 0:
                rel_error = abs((perturbed_val - orig_val) / orig_val)
            else:
                rel_error = abs(perturbed_val - orig_val)

            max_relative_error = max(max_relative_error, rel_error)

        return max_relative_error

    def get_polynomial_expression(self):
        start_time = time.perf_counter()
        polynomial_expression = self._format_polynomial_expression()
        end_time = time.perf_counter()
        self.construction_time = end_time - start_time
        
        return polynomial_expression

    def get_interpolation_time(self):
        return self.construction_time + self.interpolation_eval_time

    def get_evaluation_only_time(self):
        return self.interpolation_eval_time
