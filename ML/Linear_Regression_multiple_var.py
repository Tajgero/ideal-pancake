from matplotlib import pyplot as plt
import numpy as np


def compute_model_output(X, w, b):
    """Predicts output"""
    m = X.shape[0] # number of training examples
    f_wb = np.zeros(m)
    for i in range(m):
        f_wb[i] = np.dot(w, X[i]) + b
        
    return f_wb


def compute_cost(X, y, w, b):
    """Computes cost for linear regression"""
    m = X.shape[0] # number of training examples
    
    cost_sum = 0
    for i in range(m):
        f_wb = np.dot(w, X[i]) + b
        cost = (f_wb - y[i]) ** 2
        cost_sum += cost
    total_cost = (1 / (2 * m)) * cost_sum

    return total_cost


def compute_parameters(X, y, w, b, a=0.001):
    """Computes parameters inside for linear regression"""
    m, n = X.shape # m - parameters, n - features
    
    # X[i] - vector across all features
    # X[i, j] - scalar number in "j" feature
    # w - initiate vector of weights
    # b - scalar number of bias
    
    def der_sum_weight():
        dj_dw = np.zeros(n) # Make a new vector
        for i in range(m): # For each example
            error = np.dot(w, X[i]) + b - y[i]
            for j in range(n): # For each feature
                dj_dw[j] += error * X[i, j]
                
        return dj_dw / m
        
    def der_sum_bias():
        dj_db = 0
        for i in range(m):
            dj_db += np.dot(w, X[i]) + b - y[i]
            
        return dj_db / m
    
    new_w = w - a * der_sum_weight()
    new_b = b - a * der_sum_bias()
    
    return (new_w, new_b)


if __name__ == "__main__":
    """For some points it calculates best linear regression"""
    
    # Initialize a max iterations and minimum change to converge
    MAX_ITERATIONS = 100000
    MIN_ERROR_IMPROVEMENT = 1e-3
    
    # Points
    X = np.array([[2104, 5, 1, 45], [1416, 3, 2, 40], [852, 2, 1, 35]])
    y = np.array([460, 232, 178])
    
    # Starting point
    w = np.zeros(X.shape[1]) # Number of features
    b = 0
    error = np.inf
    
    # History
    J_history = []
    
    # Finding weight and bias
    for i in range(MAX_ITERATIONS):
        w, b = compute_parameters(X, y, w, b, a=5e-7)
        new_error = compute_cost(X, y, w, b)
        
        # Save cost J at each iteration
        if i % 10 == 0: # prevent resource exhaustion 
            J_history.append((i, new_error))
        
        if error - new_error < MIN_ERROR_IMPROVEMENT or new_error > error:
            print(f"Converged after {i+1} iterations.")
            break
        error = new_error
    else:
        print("Max iterations reached")
    
    # Solution
    w_print = [str(i) + '(x' + str(j) + ')' for j, i in enumerate(np.round(w, 3))]
    print(f"Regression: f(x) = {' + '.join(w_print)} + {b:.3f}")
    
    # Predict
    f_wb = np.round(compute_model_output(X, w, b))
    print("Predicted:", f_wb)
    print("Real:", y)
    print("Error:", np.round(compute_cost(X, y, w, b)))
    
    # Show learning curve
    fig, ax = plt.subplots()
    
    Jx = [x[0] for x in J_history]
    Jy = [y[1] for y in J_history]

    ax.set_title("Cost vs iterations")   
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Cost")
    ax.plot(Jx, Jy)
    
    plt.show()
