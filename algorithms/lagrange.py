import time

class LagrangeInterpolator:
    def __init__(self, x_vals, y_vals):
        self.x_vals = x_vals
        self.y_vals = y_vals
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
        terms = []
        for k in range(self.n):
            numerator_terms = []
            denominator = 1
            for i in range(self.n):
                if i != k:
                    numerator_terms.append(f"(x - {self.x_vals[i]})")
                    denominator *= (self.x_vals[k] - self.x_vals[i])

            numerator = " * ".join(numerator_terms)
            coeff = self.y_vals[k] / denominator

            if abs(coeff) == 1:
                coeff_str = "-" if coeff < 0 else ""
            else:
                coeff_str = f"{coeff:.2f}" if coeff % 1 else f"{int(coeff)}"

            term = f"{coeff_str} * {numerator}" if numerator else f"{coeff_str}"
            terms.append(term.strip())

        expression = " + ".join(terms)
        expression = expression.replace("+ -", "- ")
        return f"f(x) = {expression}"
    
    def get_polynomial_expression(self):
        return self.polynomial_expression
    
    def get_interpolation_time(self):
        return self.interpolation_time