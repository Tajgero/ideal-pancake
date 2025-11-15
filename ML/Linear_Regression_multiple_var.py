import numpy as np


def compute_model_output(X, w, b):
    """Predicts output"""
    m = X.shape[0] # number of training examples
    f_wb = np.zeros(m)
    for i in range(m):
        f_wb[i] = np.dot(w, X[i]) + b
        
    return f_wb


def compute_cost(X, y, w, b, lambda_=0):
    """Computes cost for linear regression"""
    m, n = X.shape # number of training examples and features

    cost_sum = 0
    for i in range(m):
        f_wb = np.dot(w, X[i]) + b
        cost = (f_wb - y[i]) ** 2
        cost_sum += cost
    total_cost = (1 / (2 * m)) * cost_sum
    
    if lambda_: # Changes cost for regularization
        total_cost += lambda_ * np.sum(w ** 2)
        total_cost /= (2 * m)

    return total_cost


def compute_gradient(X, y, w, b):
    """Computes parameters inside for linear regression"""
    m, n = X.shape # m - parameters, n - features
    
    # X[i] - vector across all features
    # X[i, j] - scalar number in "j" feature
    # w - initiate vector of weights
    # b - scalar number of bias
    
    dj_dw = np.zeros(n) # Make a new vector
    dj_db = 0
    
    for i in range(m): # For each example
        error = np.dot(w, X[i]) + b - y[i]
        dj_db += error
        for j in range(n): # For each feature
            dj_dw[j] += error * X[i, j]
            
    return (dj_dw / m, dj_db / m)


def gradient_descent(
    X, y, w_in, b_in, alpha=1e-7, num_iters=1e+4, erg_eval=1e-3, lambda_=0
):
    """
    Performs batch gradient descent
    
    Args:
        X (ndarray_like)  : Input train data array
        y (array_like)    : Input train target data
        w_in (array_like) : Initialize weights at start
        b_in (int)        : Initialize bias at start
        alpha (float, optional)     : Learning rate
        num_iters (int, optional)   : Number of iterations to run gradient descent
        erg_eval (float, optional)  : Minimum error improvement
        lambda_ (None or float)     : Regularize complexity of a function for weights

    Returns:
        w (ndarray)       : Updated values of parameters
        b (int)           : Updated value of parameter
        J_history (list)  : List of cost evaluations
    """
    from copy import deepcopy
    # Hyperparameters
    a = alpha
    w = deepcopy(w_in)
    b = b_in
    error = np.inf

    # History
    J_history = []
    
    # Finding weight and bias
    for i in range(num_iters):
        dj_dw, dj_db = compute_gradient(X, y, w, b)
        
        # Added regularization at the end
        w = w - a * dj_dw - a * (lambda_ * w) / X.shape[0]
        b = b - a * dj_db
        
        new_error = compute_cost(X, y, w, b, lambda_)
        
        # Save cost J at each iteration
        if i % 10 == 0: # prevent resource exhaustion 
            J_history.append((i, new_error))
        
        if error - new_error < erg_eval: #or new_error > error:
            print(f"Converged after {i+1} iterations.")
            break
        error = new_error
    else:
        print("Max iterations reached")
    
    return w, b, J_history


if __name__ == "__main__":
    """For some points it calculates best linear regression"""
    
    # Initialize a max iterations and minimum change to converge
    MAX_ITERATIONS = 100000
    MIN_ERROR_IMPROVEMENT = 1e-3
    
    # Points
    X_train = np.array([[2104, 5, 1, 45], [1416, 3, 2, 40], [852, 2, 1, 35]])
    y_train = np.array([460, 232, 178])
    
    # Hyperparameters
    a = 1e-7
    w = np.zeros_like(X_train[0])
    b = 0
    lambda_ = 0
    
    w, b, history = gradient_descent(
        X_train, y_train, w, b, a, MAX_ITERATIONS, MIN_ERROR_IMPROVEMENT, lambda_
    )
    
    # Solution
    w_print = [str(i) + '(x' + str(j) + ')' for j, i in enumerate(np.round(w, 3))]
    print(f"Regression: f(x) = {' + '.join(w_print)} + {b:.3f}")
    
    # Predict
    f_wb = np.round(compute_model_output(X_train, w, b))
    print("Predicted:", f_wb)
    print("Real:", y_train)
    print("Error:", np.round(compute_cost(X_train, y_train, w, b)))
    
    from matplotlib import pyplot as plt
    # Show learning curve
    fig, ax = plt.subplots()
    
    Jx = [x[0] for x in history]
    Jy = [y[1] for y in history]

    ax.set_title("Cost vs iterations")   
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Cost")
    ax.plot(Jx, Jy)
    
    plt.show()
