import time

class BarycentricInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = x_vals
        self.y_vals = y_vals
        self.n = len(x_vals)
        self.weights = self._compute_weights()
        
        start_time = time.perf_counter()
        self.polynomial_expression = self.compute_polynomial_expression()
        end_time = time.perf_counter()
        self.interpolation_time = end_time - start_time

    def _compute_weights(self):
        w = [1.0] * self.n
        for j in range(self.n):
            for k in range(self.n):
                if j != k:
                    w[j] /= (self.x_vals[j] - self.x_vals[k])
        return w

    def interpolate(self, x):
        numerator = 0.0
        denominator = 0.0
        for j in range(self.n):
            if x == self.x_vals[j]:
                return self.y_vals[j]
            temp = self.weights[j] / (x - self.x_vals[j])
            numerator += temp * self.y_vals[j]
            denominator += temp
        return numerator / denominator if denominator != 0 else 0

    def compute_polynomial_expression(self):
        terms = []
        for j in range(self.n):
            numerators = []
            for m in range(self.n):
                if m != j:
                    numerators.append(f"(x - {self.x_vals[m]})")
            numerator_expr = " * ".join(numerators)
            term_expr = f"({self.weights[j]:.4f} * {self.y_vals[j]:.4f} * {numerator_expr})"
            terms.append(term_expr)
        return " + ".join(terms)

    def get_polynomial_expression(self):
        return self.polynomial_expression

    def get_interpolation_time(self):
        return self.interpolation_time