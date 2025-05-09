import time
from sympy import symbols, expand, Poly
from utils.string_manipulation import to_digit_superscript

class BarycentricInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = list(map(float, x_vals))
        self.y_vals = list(map(float, y_vals))
        self.n = len(self.x_vals)
        self.weights = self._compute_weights()
        self.interpolation_eval_time = 0
        self.construction_time = 0

    def _compute_weights(self):
        w = [1.0] * self.n
        for j in range(self.n):
            xj = self.x_vals[j]
            for k in range(self.n):
                if j != k:
                    diff = xj - self.x_vals[k]
                    if diff == 0:
                        raise ZeroDivisionError("Duplicate x-values encountered.")
                    w[j] /= diff
        return w

    def interpolate(self, x):
        start = time.perf_counter()
        x = float(x)

        for j in range(self.n):
            if x == self.x_vals[j]:
                return self.y_vals[j]

        numerator = 0.0
        denominator = 0.0
        for j in range(self.n):
            temp = self.weights[j] / (x - self.x_vals[j])
            numerator += temp * self.y_vals[j]
            denominator += temp

        end = time.perf_counter()
        self.interpolation_eval_time += end - start

        return numerator / denominator if denominator != 0 else 0.0

    def _compute_polynomial_coefficients(self):
        poly = [0.0] * self.n

        for j in range(self.n):
            term_poly = [1.0]
            for m in range(self.n):
                if m != j:
                    next_term = [0.0] * (len(term_poly) + 1)
                    for i in range(len(term_poly)):
                        next_term[i] -= term_poly[i] * self.x_vals[m]
                        next_term[i + 1] += term_poly[i]
                    term_poly = next_term

            weight_y = self.weights[j] * self.y_vals[j]
            for i in range(len(term_poly)):
                poly[i] += weight_y * term_poly[i]

        return poly

    def _format_polynomial_expression(self, coefficients):
        x = symbols("x")
        poly_expr = sum(coeff * x**i for i, coeff in enumerate(coefficients))
        poly_expr = expand(poly_expr)

        def to_unicode_poly_string(poly):
            terms = []
            poly = Poly(poly, x)
            coeffs = poly.all_coeffs()
            deg = len(coeffs) - 1

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
        perturbed_y_vals = [y + perturbation for y in self.y_vals]
        perturbed_interpolator = BarycentricInterpolator(self.x_vals, perturbed_y_vals)

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
        coefficients = self._compute_polynomial_coefficients()
        polynomial_expression = self._format_polynomial_expression(coefficients)
        end_time = time.perf_counter()
        self.construction_time = end_time - start_time

        return polynomial_expression

    def get_interpolation_time(self):
        return self.construction_time + self.interpolation_eval_time

    def get_evaluation_only_time(self):
        return self.interpolation_eval_time
