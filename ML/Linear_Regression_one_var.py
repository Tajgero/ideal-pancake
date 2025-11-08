import matplotlib.pyplot as plt
import numpy as np
import math


def compute_model_output(x, w, b):
    m = x.shape[0]
    f_wb = np.zeros(m)
    for i in range(m):
        f_wb[i] = w * x[i] + b
        
    return f_wb


def compute_cost(x, y, w, b, reg=0):

    # number of training examples
    m = x.shape[0]
    
    cost_sum = 0
    for i in range(m):
        f_wb = w * x[i] + b
        cost = (f_wb - y[i]) ** 2
        cost_sum += cost
        
    # Total cost regularized at the end (one variable/feature)
    total_cost = (1 / (2 * m)) * cost_sum + (reg * w) / (2 * m)

    return total_cost


def compute_parameters(x, y, w, b, a=0.001, reg=0):
    m = x.shape[0]
    def der_sum_weight():
        total = 0
        for i in range(m):
            total += (w * x[i] + b - y[i]) * x[i]
        return total / m
        
    def der_sum_bias():
        total = 0
        for i in range(m):
            total += w * x[i] + b - y[i]
        return total / m
    
    # Added regularization at the end
    new_w = w - a * der_sum_weight() - a * (reg * w) / m
    new_b = b - a * der_sum_bias()
    
    return (new_w, new_b)


if __name__ == "__main__":
    """For some points it calculates best linear regression"""
    
    # Initialize a max iterations and minimum change to converge
    MAX_ITERATIONS = 100000
    MIN_ERROR_IMPROVEMENT = 1e-6
    
    # Points
    x = np.array([1.0, 1.2, 1.7, 2.0, 2.5, 3.0, 3.2])
    y = np.array([250, 280, 300, 480, 430, 630, 730])
    
    # Starting point
    w = 0
    b = 0
    alpha = 1e-5
    error = math.inf
    regularization = 0
    
    # Finding weight and bias
    for i in range(MAX_ITERATIONS):
        w, b = compute_parameters(x, y, w, b, alpha, regularization)
        new_error = compute_cost(x, y, w, b, regularization)
        
        if error - new_error < MIN_ERROR_IMPROVEMENT or new_error > error:
            print(f"Converged after {i+1} iterations.")
            break
        
        error = new_error
    
    # Solution
    print(f"Regression line: f(x) = {w:.2f}x + {b:.2f}")
    f_wb = compute_model_output(x, w, b)
    
    fig, ax = plt.subplots()
    
    ax.scatter(x, y)
    ax.plot(x, f_wb)
    
    ax.set_title("Points")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    
    plt.show()
    
