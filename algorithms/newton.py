import time

class NewtonInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = x_vals
        self.y_vals = y_vals
        self.divided_diffs = self._compute_divided_differences()
        
        start_time = time.perf_counter()
        self.polynomial_expression = self.compute_polynomial_expression()
        end_time = time.perf_counter()
        self.interpolation_time = end_time - start_time

    def _compute_divided_differences(self):
        n = len(self.x_vals)
        table = [[0 for _ in range(n)] for _ in range(n)]

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
        terms = [f"{self.divided_diffs[0]:.4f}"]
        for i in range(1, len(self.divided_diffs)):
            part = " * ".join([f"(x - {self.x_vals[j]:.4f})" for j in range(i)])
            coeff = f"{self.divided_diffs[i]:+.4f}"
            terms.append(f"{coeff} * {part}")

        expression = " + ".join(terms)
        return f"f(x) = {expression}"

    def get_polynomial_expression(self):
        return self.polynomial_expression

    def get_interpolation_time(self):
        return self.interpolation_time