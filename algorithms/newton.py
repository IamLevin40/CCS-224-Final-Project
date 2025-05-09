import time
from sympy import symbols, expand, Poly
from utils.string_manipulation import to_digit_superscript

class NewtonInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = [float(x) for x in x_vals]
        self.y_vals = [float(y) for y in y_vals]
        self.divided_diffs = self._compute_divided_differences()
        self.interpolation_eval_time = 0

    def _compute_divided_differences(self):
        n = len(self.x_vals)
        table = [[0.0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            table[i][0] = self.y_vals[i]

        for j in range(1, n):
            for i in range(n - j):
                numerator = table[i + 1][j - 1] - table[i][j - 1]
                denominator = self.x_vals[i + j] - self.x_vals[i]
                table[i][j] = numerator / denominator

        return [table[0][j] for j in range(n)]

    def interpolate(self, x):
        start = time.perf_counter()

        result = self.divided_diffs[0]
        term = 1.0
        for i in range(1, len(self.divided_diffs)):
            term *= (x - self.x_vals[i - 1])
            result += self.divided_diffs[i] * term

        end = time.perf_counter()
        self.interpolation_eval_time += end - start

        return result

    def _format_polynomial_expression(self):
        x = symbols('x')
        n = len(self.divided_diffs)
        polynomial = 0
        term = 1

        for i in range(n):
            coeff = self.divided_diffs[i]
            polynomial += coeff * term
            if i < n - 1:
                term *= (x - self.x_vals[i])

        polynomial = expand(polynomial)

        def to_unicode_poly_string(poly_expr):
            poly = Poly(poly_expr, x)
            coeffs = poly.all_coeffs()
            degree = len(coeffs) - 1

            terms = []
            for i, coeff in enumerate(coeffs):
                power = degree - i
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

        return f"N(x) = {to_unicode_poly_string(polynomial)}"

    def get_numerical_stability(self, perturbation=1e-5, num_samples=1000):
        perturbed_y_vals = [y + perturbation for y in self.y_vals]
        perturbed_interpolator = NewtonInterpolator(self.x_vals, perturbed_y_vals)

        min_x = min(self.x_vals)
        max_x = max(self.x_vals)
        if len(self.x_vals) == 1:
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
